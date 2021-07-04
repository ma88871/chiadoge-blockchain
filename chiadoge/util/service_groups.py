from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "chiadoge_harvester chiadoge_timelord_launcher chiadoge_timelord chiadoge_farmer chiadoge_full_node chiadoge_wallet".split(),
    "node": "chiadoge_full_node".split(),
    "harvester": "chiadoge_harvester".split(),
    "farmer": "chiadoge_harvester chiadoge_farmer chiadoge_full_node chiadoge_wallet".split(),
    "farmer-no-wallet": "chiadoge_harvester chiadoge_farmer chiadoge_full_node".split(),
    "farmer-only": "chiadoge_farmer".split(),
    "timelord": "chiadoge_timelord_launcher chiadoge_timelord chiadoge_full_node".split(),
    "timelord-only": "chiadoge_timelord".split(),
    "timelord-launcher-only": "chiadoge_timelord_launcher".split(),
    "wallet": "chiadoge_wallet chiadoge_full_node".split(),
    "wallet-only": "chiadoge_wallet".split(),
    "introducer": "chiadoge_introducer".split(),
    "simulator": "chiadoge_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
