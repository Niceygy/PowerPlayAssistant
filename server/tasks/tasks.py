from server.powers import power_full_to_short, get_system_power_info
from server.constants import CRIMINALTASKS, POWERRENFORCEACTIVITIES, TASKSHORTCODES, TASKTYPES, POWERWEAKNESSES, HOMESYSTEMS, PERMITLOCKED, TASKDESCRIPTIONS
from server.tasks.commodites import what_commodity_action
from server.database.database import StarSystem 
from server.tasks.odyssey import retrieve_specific_goods

def getTaskType(task_name):
    """
    Get the type of a task based on its full name.

    Args:
        task_name (str): The full name of the task.

    Returns:
        str: The type of the task (e.g., "Illegal", "Legal").
    """
    taskShortCode = None
    for key, value in TASKSHORTCODES.items():
        if task_name == value:
            taskShortCode = key
    for taskType, tasks in TASKTYPES.items():
        if taskShortCode in tasks:
            return taskType
    return None

def isPowersWeakness(power_name, task_name):
    """
    Check if a task is the weakness of a power.

    Args:
        power_name (str): The full name of the power.
        task_name (str): The full name of the task.

    Returns:
        str: "is" if the task is the power's weakness, otherwise "is not".
    """
    power_shortcode = power_full_to_short(power_name)
    taskShortCode = None
    try:
        for key, value in TASKSHORTCODES.items():
            if task_name == value:
                taskShortCode = key
        if taskShortCode in POWERWEAKNESSES[power_shortcode]:
            return "is"
        return "is not"
    except Exception as e:
        return "is not"

    
def isHomeSystem(system_name):
    """
    Check if a system is a home system.

    Args:
        system_name (str): The name of the system.

    Returns:
        bool: True if the system is a home system, otherwise False.
    """
    return system_name in HOMESYSTEMS
    
def isPermitLocked(system_name):
    """
    Check if a system is permit locked.

    Args:
        system_name (str): The name of the system.

    Returns:
        bool: True if the system is permit locked, otherwise False.
    """
    return system_name in PERMITLOCKED
    
def systemNotes(powerFullName, system_name, database):
    """
    Get notes about a system.

    Args:
        powerFullName (str): The full name of the power.
        system_name (str): The name of the system.

    Returns:
        str: Notes about the system.
    """
    
    controllingPower = get_system_power_info(system_name, database)[1]
    message = ""
    if (isHomeSystem(system_name)):
        message += f"This is the home system of {controllingPower}. It cannot be undermined or reinforced. "
    if (isPermitLocked(system_name)):
        message += f"This system is permit locked. "
    if (hasResSite(system_name, database)):
        message += f"This system has a resource extraction site. "
    if get_system_power_info(system_name, database)[0] == "Stronghold":
        message += " Warning, this system is a stronghold. Opposing powers will not be welcome here"
    if message == "":
        return "N/A"
    else:
        return message
    
def task_description(task_name: str, power_name: str, system_name: str, system_power_info, database, extraInfo=""):
    """
    Get the description of a task.

    Expects:
        - [String] task_name: The full name of the task.
        - [String] power_name: The full name of the power.
        - [String] system_name: The system it is being completed in.
        - [Array[String]] system_power_info: Powerplay info for that system.
        - [Object] database: Database connection

    Returns:
        str: Description of the task.
    """
    if task_name == None:
        return ""
    #a crime?
    result = ""
    # if isTaskACrime(task_name, is_system_anarchy(system_name, database)):
    #     result += "This task is illegal in non-anarchy systems. "

    taskShortCode = None
    for key, value in TASKSHORTCODES.items():
        if task_name == value:
            taskShortCode = key
    # with open("./static/conf/Descriptions.txt", "r") as f:
    #     for line in f:
    #         if line.startswith("#"):
    #             continue
    #         if str(line).startswith(str(taskShortCode)):
    #             result += line.split("=")[1]
    result += TASKDESCRIPTIONS[taskShortCode]
    if task_name == "Transport Powerplay commodities":
        result += f". You will need the commodity '{what_commodity_action(power_name, system_name, database)}'."
    if task_name == "Upload Powerplay Malware":
        result += f"You will need '{retrieve_specific_goods(power_name, system_name, database)}'. "
    if extraInfo != None:
        result += extraInfo
    return result

def hasResSite(system_name: str, database):
    """
    Check if a system has a resource extraction site.

    Args:
        - [String] system_name: The name of the system.

    Returns:
        bool: True if the system has a resource extraction site, otherwise False.
    """
    return False
    try:
        result = database.session.query(StarSystem).filter(StarSystem.system_name == system_name).first()
        return result.has_res_sites
    except Exception as e:
        return False
    
def isTaskACrime(task_name: str, isAnarchy: bool):
    """
    Checks if a task is a crime.

    Expects:
        - [String] task_name: The full name of the task
        - [Bool] isAnarchy: Is the system the task is being done in anarchy?

    Returns:
        - [bool] isACrime: True if it is illegal, false if not.
    """

    if isAnarchy:
        return False

    #task name to shortcode
    taskShortCode = ""

    for key, data in TASKSHORTCODES.items():
        if data == task_name:
            taskShortCode = key

    #task in crime list?
    
    if taskShortCode in CRIMINALTASKS:
        return True
    else:
        return False
    
def is_task_own_strength(taskFullName: str, powerFullName: str):
    """
    Is this task really good for this power?
    """
    try:
        taskShortCode = None
        for key, value in TASKSHORTCODES.items():
            if taskFullName == value:
                taskShortCode = key
        powerShortCode = power_full_to_short(powerFullName)
        if taskShortCode in POWERRENFORCEACTIVITIES[powerShortCode]:
            return True
        else:
            return False
    except Exception:
        return False
    