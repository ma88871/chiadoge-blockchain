#!/bin/bash
pip install setuptools_scm
# The environment variable CHIADOGE_INSTALLER_VERSION needs to be defined.
# If the env variable NOTARIZE and the username and password variables are
# set, this will attempt to Notarize the signed DMG.
CHIADOGE_INSTALLER_VERSION=$(python installer-version.py)

if [ ! "$CHIADOGE_INSTALLER_VERSION" ]; then
	echo "WARNING: No environment variable CHIADOGE_INSTALLER_VERSION set. Using 0.0.0."
	CHIADOGE_INSTALLER_VERSION="0.0.0"
fi
echo "Chiadoge Installer Version is: $CHIADOGE_INSTALLER_VERSION"

echo "Installing npm and electron packagers"
npm install electron-installer-dmg -g
npm install electron-packager -g
npm install electron/electron-osx-sign -g
npm install notarize-cli -g

echo "Create dist/"
sudo rm -rf dist
mkdir dist

echo "Create executables with pyinstaller"
pip install pyinstaller==4.2
SPEC_FILE=$(python -c 'import chiadoge; print(chiadoge.PYINSTALLER_SPEC_PATH)')
pyinstaller --log-level=INFO "$SPEC_FILE"
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "pyinstaller failed!"
	exit $LAST_EXIT_CODE
fi
cp -r dist/daemon ../chiadoge-blockchain-gui
cd .. || exit
cd chiadoge-blockchain-gui || exit

echo "npm build"
npm install
npm audit fix
npm run build
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "npm run build failed!"
	exit $LAST_EXIT_CODE
fi

electron-packager . Chiadoge --asar.unpack="**/daemon/**" --platform=darwin \
--icon=src/assets/img/Chiadoge.icns --overwrite --app-bundle-id=net.chiadoge.blockchain \
--appVersion=$CHIADOGE_INSTALLER_VERSION
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-packager failed!"
	exit $LAST_EXIT_CODE
fi

if [ "$NOTARIZE" ]; then
  electron-osx-sign Chiadoge-darwin-x64/Chiadoge.app --platform=darwin \
  --hardened-runtime=true --provisioning-profile=chiadogeblockchain.provisionprofile \
  --entitlements=entitlements.mac.plist --entitlements-inherit=entitlements.mac.plist \
  --no-gatekeeper-assess
fi
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-osx-sign failed!"
	exit $LAST_EXIT_CODE
fi

mv Chiadoge-darwin-x64 ../build_scripts/dist/
cd ../build_scripts || exit

DMG_NAME="Chiadoge-$CHIADOGE_INSTALLER_VERSION.dmg"
echo "Create $DMG_NAME"
mkdir final_installer
electron-installer-dmg dist/Chiadoge-darwin-x64/Chiadoge.app Chiadoge-$CHIADOGE_INSTALLER_VERSION \
--overwrite --out final_installer
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-installer-dmg failed!"
	exit $LAST_EXIT_CODE
fi

if [ "$NOTARIZE" ]; then
	echo "Notarize $DMG_NAME on ci"
	cd final_installer || exit
  notarize-cli --file=$DMG_NAME --bundle-id net.chiadoge.blockchain \
	--username "$APPLE_NOTARIZE_USERNAME" --password "$APPLE_NOTARIZE_PASSWORD"
  echo "Notarization step complete"
else
	echo "Not on ci or no secrets so skipping Notarize"
fi

# Notes on how to manually notarize
#
# Ask for username and password. password should be an app specific password.
# Generate app specific password https://support.apple.com/en-us/HT204397
# xcrun altool --notarize-app -f Chiadoge-0.1.X.dmg --primary-bundle-id net.chiadoge.blockchain -u username -p password
# xcrun altool --notarize-app; -should return REQUEST-ID, use it in next command
#
# Wait until following command return a success message".
# watch -n 20 'xcrun altool --notarization-info  {REQUEST-ID} -u username -p password'.
# It can take a while, run it every few minutes.
#
# Once that is successful, execute the following command":
# xcrun stapler staple Chiadoge-0.1.X.dmg
#
# Validate DMG:
# xcrun stapler validate Chiadoge-0.1.X.dmg
