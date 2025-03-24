from server.constants import POWERDATA
from server.database.database import PowerData
from server.powers import power_full_to_short

def retrieve_specific_goods(powerFullName: str, system_name: str, database):
    #what commodities
    powershortcode = power_full_to_short(powerFullName)
    result = database.session.query(PowerData).filter(PowerData.system_name == system_name).first()
    if result is None:
        #no data, assume unoccupied
        return POWERDATA[0]
    elif result.shortcode == powershortcode:
        #reinforce 
        return POWERDATA[0]
    elif result.shortcode == "" or result.shortcode is None:
        #not occupied
        return POWERDATA[0]
    else:
        #undermine
        return POWERDATA[1]
    
def find_nearby_stronghold(powerFullName: str, system_name: str):
    powerShortCode = power_full_to_short(powerFullName)
    
