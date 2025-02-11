from server.constants import POWERDATA
from server.database.database import StarSystem
from server.powers import power_full_to_short

def retrieve_specific_goods(powerFullName, system_name, database):
    #what commodities
    powershortcode = power_full_to_short(powerFullName)
    result = database.session.query(StarSystem).filter(StarSystem.system_name == system_name).first()
    if result.shortcode == powershortcode:
        #reinforce 
        return POWERDATA[0]
    elif result.shortcode == "":
        #not occupied
        return POWERDATA[0]
    else:
        #undermine
        return POWERDATA[1]
    
def find_anarchy_settlement():
    i = 0

