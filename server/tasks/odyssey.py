from server.constants import POWERDATA
from server.database.database import PowerData, StarSystem
from server.powers import power_full_to_short


def retrieve_specific_goods(powerFullName: str, system_name: str, database):
    # what commodities
    powershortcode = power_full_to_short(powerFullName)
    result = (
        database.session.query(PowerData)
        .filter(PowerData.system_name == system_name)
        .first()
    )
    if result is None:
        # no data, assume unoccupied
        return POWERDATA[0]
    elif result.shortcode == powershortcode:
        # reinforce
        return POWERDATA[0]
    elif result.shortcode == "" or result.shortcode is None:
        # not occupied
        return POWERDATA[0]
    else:
        # undermine
        return POWERDATA[1]


def find_goods_system(powerFullName: str, system_name: str, action: str, database):
    systems_query = (
        database.session.query(StarSystem)
        .join(
            PowerData, StarSystem.system_name == PowerData.system_name
        )
        .filter(PowerData.shortcode != power_full_to_short(powerFullName))
        .filter(PowerData.state == "Stronghold")
        
        .limit(50)
    )
