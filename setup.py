from setuptools import setup

dependencies = [
    "blspy==1.0.2",  # Signature library
    "chiavdf==1.0.1",  # timelord and vdf verification
    "chiabip158==1.0",  # bip158-style wallet filters
    "chiapos==1.0.2",  # proof of space
    "clvm==0.9.6",
    "clvm_rs==0.1.7",
    "clvm_tools==0.4.3",
    "aiohttp==3.7.4",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.7",  # Binary data management library
    "colorlog==5.0.1",  # Adds color to logs
    "concurrent-log-handler==0.9.19",  # Concurrently log and rotate logs
    "cryptography==3.4.7",  # Python cryptography library for TLS - keyring conflict
    "keyring==23.0.1",  # Store keys in MacOS Keychain, Windows Credential Locker
    "keyrings.cryptfile==1.3.4",  # Secure storage for keys on Linux (Will be replaced)
    #  "keyrings.cryptfile==1.3.8",  # Secure storage for keys on Linux (Will be replaced)
    #  See https://github.com/frispete/keyrings.cryptfile/issues/15
    "PyYAML==5.4.1",  # Used for config file format
    "setproctitle==1.2.2",  # Gives the chiadoge processes readable names
    "sortedcontainers==2.3.0",  # For maintaining sorted mempools
    "websockets==8.1.0",  # For use in wallet RPC and electron UI
    "click==7.1.2",  # For the CLI
    "dnspython==2.1.0",  # Query DNS seeds
]

upnp_dependencies = [
    "miniupnpc==2.1",  # Allows users to open ports on their router
]

dev_dependencies = [
    "pytest",
    "pytest-asyncio",
    "flake8",
    "mypy",
    "black",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
]

kwargs = dict(
    name="chiadoge-blockchain",
    author="Chia Doge",
    author_email="admin@chiadoge.co",
    description="Chiadoge blockchain full node, farmer, timelord, and wallet.",
    url="https://chiadoge.co/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="chiadoge blockchain node",
    install_requires=dependencies,
    setup_requires=["setuptools_scm"],
    extras_require=dict(
        uvloop=["uvloop"],
        dev=dev_dependencies,
        upnp=upnp_dependencies,
    ),
    packages=[
        "build_scripts",
        "chiadoge",
        "chiadoge.cmds",
        "chiadoge.consensus",
        "chiadoge.daemon",
        "chiadoge.full_node",
        "chiadoge.timelord",
        "chiadoge.farmer",
        "chiadoge.harvester",
        "chiadoge.introducer",
        "chiadoge.plotting",
        "chiadoge.protocols",
        "chiadoge.rpc",
        "chiadoge.server",
        "chiadoge.simulator",
        "chiadoge.types.blockchain_format",
        "chiadoge.types",
        "chiadoge.util",
        "chiadoge.wallet",
        "chiadoge.wallet.puzzles",
        "chiadoge.wallet.rl_wallet",
        "chiadoge.wallet.cc_wallet",
        "chiadoge.wallet.did_wallet",
        "chiadoge.wallet.settings",
        "chiadoge.wallet.trading",
        "chiadoge.wallet.util",
        "chiadoge.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "chiadoge = chiadoge.cmds.chiadoge:main",
            "chiadoge_wallet = chiadoge.server.start_wallet:main",
            "chiadoge_full_node = chiadoge.server.start_full_node:main",
            "chiadoge_harvester = chiadoge.server.start_harvester:main",
            "chiadoge_farmer = chiadoge.server.start_farmer:main",
            "chiadoge_introducer = chiadoge.server.start_introducer:main",
            "chiadoge_timelord = chiadoge.server.start_timelord:main",
            "chiadoge_timelord_launcher = chiadoge.timelord.timelord_launcher:main",
            "chiadoge_full_node_simulator = chiadoge.simulator.start_simulator:main",
        ]
    },
    package_data={
        "chiadoge": ["pyinstaller.spec"],
        "chiadoge.wallet.puzzles": ["*.clvm", "*.clvm.hex"],
        "chiadoge.util": ["initial-*.yaml", "english.txt"],
        "chiadoge.ssl": ["chiadoge_ca.crt", "chiadoge_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    use_scm_version={"fallback_version": "unknown-no-.git-directory"},
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)


if __name__ == "__main__":
    setup(**kwargs)
