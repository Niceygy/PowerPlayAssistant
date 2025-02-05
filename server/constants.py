DATABASE_CONNECTION_STRING = "mysql+pymysql://assistant:6548@10.0.0.52/elite"

ITEMS_TO_RETURN = 15
"""
How many items to return in a list.
Used in megaships and rare goods 
"""


TASKNAMES = [
    "Bounty hunting",
    "Collect Escape Pods",
    "Holoscreen Hacking",
    "Power Kills",
    "Scan Megaship Datalinks",
    "Sell for large profits",
    "Sell mined resources",
    "Sell rare goods",
    "Transport Powerplay commodities",
    "Complete aid and humanitarian missions",
    "Flood markets with low value goods",
    "Scan ships and wakes",
    "Hand in biological research samples",
    "Hand in cartography data",
    "Hand in salvage",
    "Reboot mission completion",
    "Commit crimes",
    # ODY
    "Retrieve specific goods",
    "Transfer Power classified data",
    "Transfer Power association and political data",
    "Transfer Power research and Industrial data",
    "Upload Powerplay Malware",
]
"""
Task Names in an array
"""


TASKSHORTCODES = {
    "BTHT": "Bounty hunting",
    "CEPD": "Collect Escape Pods",
    "HSHK": "Holoscreen Hacking",
    "PKLS": "Power Kills",
    "SDLK": "Scan Megaship Datalinks",
    "SLFP": "Sell for large profits",
    "SMNR": "Sell mined resources",
    "SRGD": "Sell rare goods",
    "TPCD": "Transport Powerplay commodities",
    "CAHM": "Complete aid and humanitarian missions",
    "FMLV": "Flood markets with low value goods",
    "SSWK": "Scan ships and wakes",
    "HBRS": "Hand in biological research samples",
    "HICD": "Hand in cartography data",
    "HISV": "Hand in salvage",
    "RMCP": "Reboot mission completion",
    "CMCR": "Commit crimes",
    # ODY
    "RSGD": "Retrieve specific goods",
    "TPCL": "Transfer Power classified data",
    "TPAD": "Transfer Power association and political data",
    "TPRD": "Transfer Power research and Industrial data",
    "UPMW": "Upload Powerplay Malware",
}
"""
Task shortcodes and their names
"""

TASKTYPES = {
    "Combat": ["BTHT", "PKLS", "CMCR"],
    "Trading": ["SLFP", "SRGD", "FMLV", "TPCD"],
    "Mining": ["SMNR"],
    "Scanning": ["SSWK", "HICD", "SDLK"],
    "Exploration": ["HICD", "HBRS"],
    "Odyssey": ["RSGD", "TPCL", "TPAD", "TPRD", "UPMW"],
    "Aid": ["CAHM", "CEPD"],
    "Illegal": ["CMCR", "HSHK", "PKLS", "UPMW"],
}


POWERWEAKNESSES = {
    "ALD": ["CMCR", "SDLK"],
    "ARD": ["BTHT", "PKLS"],
    "ASD": ["HSHK", "TPCD"],
    "DPT": ["CMCR", "SDLK"],
    "EMH": ["FMLV", "HSHK"],
    "FLW": ["RSGD", "FMLV"],
    "JRA": ["CMCR", "RSGD"],
    "LYR": ["UPMW", "FMLV"],
    "NAK": ["HSHK", "FMLV"],
    "PRA": ["TPCD", "FMLV"],
    "YRG": ["CMCR", "UPMW"],
    "ZMT": ["RSGD", "SMNR"],
}

POWERS = {
    "ALD": "Arissa Lavingy-Duval",
    "ARD": "Archon Delane",
    "ASD": "Aisling Duval",
    "DPT": "Denton Patrus",
    "EMH": "Edmund Mahon",
    "FLW": "Felicia Winters",
    "JRA": "Jerome Archer",
    "LYR": "Li Yong-Rui",
    "NAK": "Nakato Kaine",
    "PRA": "Prantav Antal",
    "YRG": "Yuri Grom",
    "ZMT": "Zemina Torval",
}

HOMESYSTEMS = {
    "Kamadhenu": "ALD",
    "Achenar": "ARD",
    "Cubeo": "ASD",
    "Eotienses": "DPT",
    "Gateway": "EMH",
    "Rhea": "FLW",
    "Nanomam": "JRA",
    "Lembava": "LYR",
    "Tionisla": "NAK",
    "Polevnic": "PRA",
    "Clayakarma": "YRG",
    "Synteini": "ZMT",
}


"""
Permit locked systems
"""
PERMITLOCKED = [
    # independent
    "Shinrarta Dezhra",
    "Sirius",
    "van Maanen's Star",
    "Mbooni",
    "CD-43 11917",
    # federation
    "Sol",
    "Beta Hydri",
    "Vega",
    "PLX 695",
    "Ross 128",
    "Exbeur",
    "Hors",
    # empire
    "Achenar",
    "Facece",
    "Summerland",
    # alliance
    "Alioth",
]

POWERNAMES = [
    "Arissa Lavingy-Duval",
    "Archon Delane",
    "Aisling Duval",
    "Denton Patrus",
    "Edmund Mahon",
    "Felicia Winters",
    "Jerome Archer",
    "Li Yong-Rui",
    "Nakato Kaine",
    "Prantav Antal",
    "Yuri Grom",
    "Zemina Torval",
]

"""
Activities that this power really likes.
Uses shortcodes
"""
POWERRENFORCEACTIVITIES = {
    "ALD": ["BTHT", "CEPD", "HSHK"],
    "ARD": ["BTHT", "PKLS", "RSGD"],
    "ASD": ["BTHT", "PKLS", "RSGD"],
    "DPT": ["BTHT", "CEPD", "HSHK"],
    "EMH": ["SLFP", "SMNR", "CAHM"],
    "FLW": ["CEPD", "CAHM", "UPMW"],
    "JRA": ["BTHT", "CEPD", "HSHK"],
    "LYR": ["SLFP", "SMNR", "CAHM"],
    "NAK": ["CEPD", "CAHM", "UPMW"],
    "PRA": ["CEPD", "CAHM", "UPMW"],
    "YRG": ["BTHT", "CEPD", "HSHK"],
    "ZMT": ["SLFP", "SMNR", "CAHM"],
}

POWERCOMMODITIES = {
    # power: aquire, reinforce, undermine
    "ALD": [
        "Lavingy Corruption Reports",
        "Lavingy Garrison Supplies",
        "Lavingy Strategic Reports",
    ],
    "ARD": ["Kumo Contraband Packages", "Unmarked Military Supplies", "Marked Slaves"],
    "ASD": [
        "Aisling Media Material",
        "Aisling Sealed Contract",
        "Aisling Programme Material",
    ],
    "DPT": [
        "Marked Military Arms",
        "Patrus field supplies",
        "Patrus Garrison Supplies",
    ],
    "EMH": [
        "Alliance Trade Agreements",
        "Alliance Legislative Contract	",
        "Alliance Legislative Records",
    ],
    "FLW": ["Liberal Federal Aid", "Liberal Federal Packages", "Liberal Propaganda"],
    "JRA": [
        "Archer's Restricted Intel",
        "Archer's Field Supplies",
        "Archer's Garrison Supplies",
    ],
    "LYR": [
        "Sirius Franchise Package",
        "Sirius Industrial Equipment",
        "Sirius Corporate Contract",
    ],
    "NAK": ["Kaine Lobbying Material", "Kaine Aid Supplies", "Kaine Misinformation"],
    "PRA": ["Utopian Publicity", "Utopian Supplies", "Utopian Dissident"],
    "YRG": [
        "Grom Underground Support",
        "Grom Military Supplies",
        "Grom Counter Intelligence",
    ],
    "ZMT": ["Torval Trade Agreements", "Torval Deeds", "Torval Political Servants"],
}

POWERDATA = [
    "POWER TRACKER MALWARE", #undermine
    "POWER INJECTION MALWARE" #reinforce
]