from server.possibleTasks import isAnarchy, power_full_to_short, get_system_power_info
from server.constants import TASKSHORTCODES, TASKTYPES, POWERWEAKNESSES, HOMESYSTEMS, PERMITLOCKED
from server.commodites import what_commodity_action
from server.database.database import StarSystem 

def getTaskType(taskFullName):
    """
    Get the type of a task based on its full name.

    Args:
        taskFullName (str): The full name of the task.

    Returns:
        str: The type of the task (e.g., "Illegal", "Legal").
    """
    taskShortCode = None
    for key, value in TASKSHORTCODES.items():
        if taskFullName == value:
            taskShortCode = key
    for taskType, tasks in TASKTYPES.items():
        if taskShortCode in tasks:
            return taskType
    return None

def isPowersWeakness(powerFullName, taskFullName):
    """
    Check if a task is the weakness of a power.

    Args:
        powerFullName (str): The full name of the power.
        taskFullName (str): The full name of the task.

    Returns:
        str: "is" if the task is the power's weakness, otherwise "is not".
    """
    power_shortcode = power_full_to_short(powerFullName)
    taskShortCode = None
    try:
        for key, value in TASKSHORTCODES.items():
            if taskFullName == value:
                taskShortCode = key
        if taskShortCode in POWERWEAKNESSES[power_shortcode]:
            return "is"
        return "is not"
    except Exception as e:
        return "is not"

    
def isHomeSystem(systemname):
    """
    Check if a system is a home system.

    Args:
        systemname (str): The name of the system.

    Returns:
        bool: True if the system is a home system, otherwise False.
    """
    return systemname in HOMESYSTEMS
    
def isPermitLocked(systemName):
    """
    Check if a system is permit locked.

    Args:
        systemName (str): The name of the system.

    Returns:
        bool: True if the system is permit locked, otherwise False.
    """
    return systemName in PERMITLOCKED
    
def systemNotes(powerFullName, systemName, database):
    """
    Get notes about a system.

    Args:
        powerFullName (str): The full name of the power.
        systemName (str): The name of the system.

    Returns:
        str: Notes about the system.
    """
    
    controllingPower = get_system_power_info(systemName, database)[1]
    message = ""
    if (isHomeSystem(systemName)):
        message += f"This is the home system of {controllingPower}. It cannot be undermined or reinforced. "
    if (isPermitLocked(systemName)):
        message += f"This system is permit locked."
    if (hasResSite(systemName, database)):
        message += f"This system has a resource extraction site."
    if message == "":
        return "N/A"
    else:
        return message
    
def TaskDescription(taskFullName, powerFullName, systemName, systemPowerInfo, database, extraInfo=""):
    """
    Get the description of a task.

    Args:
        taskFullName (str): The full name of the task.
        isAnarchy (function): Function to check if a system is anarchy.
        systemPowerInfo (array): Power info for the selected system.

    Returns:
        str: Description of the task.
    """
    if taskFullName == None:
        return ""
    result = ""
    if isTaskACrime(taskFullName, isAnarchy(systemName, database)):
        result += "This task is illegal in non-anarchy systems. "
    # else:
    #     result += "This task is legal in all systems. "
    taskShortCode = None
    for key, value in TASKSHORTCODES.items():
        if taskFullName == value:
            taskShortCode = key
    with open("./static/conf/Descriptions.txt", "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            if str(line).startswith(str(taskShortCode)):
                result += line.split("=")[1]
    if taskFullName == "Transport Powerplay commodities":
        result += f". You will need the commodity '{what_commodity_action(powerFullName, systemName, database)}'."
    if systemPowerInfo[0] == "Stronghold":
        result += " Warning, this system is a stronghold. Opposing powers will not be welcome here"
    if extraInfo != None:
        result += extraInfo
    return result

def hasResSite(systemName, database):
    """
    Check if a system has a resource extraction site.

    Args:
        systemName (str): The name of the system.

    Returns:
        bool: True if the system has a resource extraction site, otherwise False.
    """
    try:
        result = database.session.query(StarSystem).filter(StarSystem.system_name == systemName).first()
        return result.has_res_sites
    except Exception as e:
        return False
    
def isTaskACrime(taskName, isAnarchy):
    """
    Checks if a task is a crime.

    Expects:
        - [String] taskName: The full name of the tasl

    Returns:
        - [bool] isACrime: True if it is illegal, false if not.
    """

    if isAnarchy:
        return False

    #task name to shortcode
    taskShortCode = ""

    for key, data in TASKSHORTCODES.items():
        if data == taskName:
            taskShortCode = key
    
    if taskShortCode in TASKTYPES["Illegal"]:
        return True
    else:
        return False