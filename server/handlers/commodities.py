from server.powers import get_system_power_info
from server.tasks.commodites import is_system_in_range

def handle_commodites(request, power, system, database):
    
    task = "Deliver PowerPlay Commodities"
    
    powerInfo = get_system_power_info(system, database)
    
    system_in_range, supply_system = is_system_in_range(power, system, database)
    
    return f"{system_in_range}, {supply_system}"