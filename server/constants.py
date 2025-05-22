ITEMS_TO_RETURN = 15
"""
How many items to return in a list.
Used in megaships and rare goods 
"""

TASKDESCRIPTIONS = {
    "BTHT": "Hunt pirates with bounties in-system. These can be found at resource extraction sites & at navigation beacons. Not applicable in anarchy systems.",
    "CEPD": "Collect Escape Pods: Collect escape pods (occupied or damaged) from signal sources or destroyed ships. Can be paired with bounty hunting.",
    "HSHK": "Use a recon limpet to hack holoads. Note that holoads in your own power's system may only be hacked if they are showing an ad for an opposing power. This does not apply for ads in enemy & uncontrolled systems.",
    "PKLS": "Kill members of opposing powers. Will incur bounties & fines. Works best in anarchy systems.",
    "SDLK": "First Find a megaship (as listed below) and scan it with the datalink scanner. Then find the 'Megaship Log Uplink' and scan that too.",
    "SLFP": "Trade commodites across systems for a large profit. Merits apply to destination system. Tools like Inara.cz can help with this.",
    "SMNR": "Sell mined resources in a system you wish to influence. For undermining they have to be mined in-system. If reinforcing, it does not matter where they have been mined.",
    "SRGD": "Sell rare goods to the target system. Most efficient when the rare good comes form 200LY away. Merits earned depends on profit.",
    "TPCD": "First go to a Stronghold or Fortified system nearby. Stronghold systems have a range of 30LY, and Fortified have one of 20LY. Take the commodity to a target system within range, and hand it in at any port",
    "CAHM": "Complete missions that provide aid and humanitarian support to systems. E.G Donation Missions.",
    "FMLV": "Sell low value goods in large quantities to flood the market. Biowaste seems to work well with this.",
    "SSWK": "Scan ships in supercruse or around a point of interest (E.G Station, Nav Beacon). Scanning FSD wakes also works.",
    "HBRS": "Collect and hand in exobio data at vista genomics.",
    "HICD": "Hand in cartography data: Collect and hand in cartography data.",
    "HISV": "Hand in salvage: Collect and hand in salvage from signal sources or destroyed ships.",
    "RMCP": "Reboot mission completion: Complete missions that involve rebooting systems or equipment.",
    "CMCR": "Commit crimes: Engage in criminal activities (E.G Murder, other crimes do not seem to count as much)",
    "TPPC": "Transport power-spesific commodities. These can be aquired from a power contact in a stronghold or foritified system.",
    # ODY
    "RSGD": "Retrieve specific goods from powerplay containers in settlements. Hand into the power contact in a station.",
    "TPCL": "Download 'Power classified data' from odyssey settlements, and return it to a power contact in-system.",
    "TPAD": "Download 'Power Political Data' & 'Power Association Data' from odyssey settlements, and return it to a power contact in a system your power controls.",
    "TPRD": "Download 'Power research data' & 'Power Industrial data' from odyssey settlements, and return it to a power contact in a system your power controls.",
    "UPMW": "Get Powerplay malware from your local power contact, and upload it to a settlement data point in the target system. Note: This may trigger the alarms!",
}


TASKNAMES = [
    "Bounty hunting",
    "Collect Escape Pods",
    "Holoscreen Hacking",
    "Power Kills",
    "Scan Megaship Datalinks",
    "Sell for large profits",
    "Sell Mined Resources",
    "Sell rare goods",
    "Deliver PowerPlay Commodities",
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
    # not sure
    "notsure",
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
    "TPCD": "Deliver PowerPlay Commodities",
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
"""
Task types: e.g trading or combat
"""

CRIMINALTASKS = ["CMCR", "PKLS", "UPMW", "TPRD", "TPCL", "TPAD"]
"""
Tasks that incur a bounty or fine.
"HSHK" is removed
"""

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
"""
Tasks powers are weak to
"""

POWERS = {
    "ALD": 'A. Lavigny-Duval',
    "ARD": 'Archon Delaine',
    "ASD": "Aisling Duval",
    "DPT": 'Denton Patreus',
    "EMH": "Edmund Mahon",
    "FLW": "Felicia Winters",
    "JRA": "Jerome Archer",
    "LYR": "Li Yong-Rui",
    "NAK": "Nakato Kaine",
    "PRA": 'Pranav Antal',
    "YRG": "Yuri Grom",
    "ZMT": "Zemina Torval",
}
"""
The powers and their shortcodes
"""


HOMESYSTEMS = {
    "Kamadhenu": "ALD",
    "Harma": "ARD",
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
Powers home systems
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
"""
Permit locked systems
"""

POWERNAMES = [
    "A. Lavingy-Duval",
    "Archon Delaine",
    "Aisling Duval",
    "Denton Patreus",
    "Edmund Mahon",
    "Felicia Winters",
    "Jerome Archer",
    "Li Yong-Rui",
    "Nakato Kaine",
    "Pranav Antal",
    "Yuri Grom",
    "Zemina Torval",
]
"""
Power's names
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
"""
Activities that this power really likes.
Uses shortcodes
"""

POWER_ABOUT = {
    "ALD": "Arissa Lavingy-Duval is the current Emperor, and leader of the imperial senate. Her political platform is built on honour, and she has a focus on tackling corruption.",
    "ARD": "Archon Delane is the king of the Kumo Crew, one of the most influetial crime synicates of the core systems. He is known for his ruthlessness and strict enforcement to moral codes.",
    "ASD": "Aisling Duval is a imperial princess, most known for her popularity amoungst the younger memebers of imperial society. Known as the 'People's Princess', she is firmly against imperial slaves",
    "DPT": "Denton Patrus is the leader of the imperial navy. He is well-liked in imperial circles, but resented elsewhere across the galaxy for his ruthless use of loans to force whole star systems into debt.",
    "EMH": "Edmund Mahon is the current prime minister of the Alliance, from the Diso system. He is from a strong academic background, with a thorough knowledge of alliance law and politics.",
    "FLW": "Felicia Winters is the current federal president. She became the leader of the federal party when the then-president jasmina halsey disapeared. ",
    "JRA": "Jerome Archer is the shadow federal president and sucsessor of zachary hudson. Formely the Director of the Federal Intelligence Agency, and had a long career in law enforcement.",
    "LYR": "Li Yong-Rui is the owner & CEO of the Sirius Corporation. He is a member of the prestigious Li dynasty, a pillar of Sirius Corporation for centuries, and holds doctorates in physics, politics, and economics.",
    "NAK": "Nakato Kaine is the alliance councillor for Tionisla. She has strong support among the Old Worlds, and is known for her forceful speeches before the Assembly.",
    "PRA": "Pranav Antal is the leader of the Utopia movement, which seeks to elevate humanity by embracing technology. He is the guru of the Utopia Sim-Archive, a project dedicated to storing the memories of those who have died.",
    "YRG": "Yuri Grom is the self-proclaimed Dictator of the EG Pilots, an independent faction based out of Euryale that formed from breakaway elements of the Federation. He was formally the leader of the federal navy.",
    "ZMT": "Zemina Torval is the matriarch of the Torval family & the Imperial Senator of Synteini. She is one of the Empire's most powerful and wealthy figures and splits her time between business and politics.",
}
"""
Powers descriptions
"""

POWER_PERKS = {
    "ALD": "+100% Bounty Payouts, -30% Weapon Costs",
    "ARD": f"+30% black market profits, -100% reduced value on bounties placed on you",
    "ASD": f"+100% minor faction rep gain, +200% search & rescue payout",
    "DPT": f"+80% bounty payouts, -90% rearm prices & -40% weapon cost",
    "EMH": f"+100% minor faction gain, +50% bonds for rare goods & +25% trade bonds",
    "FLW": f"+60% food & medicine profits, +100% minor faction gain & +100% salvage profits",
    "JRA": f"+100% bounty payouts & -30% weapon costs",
    "LYR": f"-100% R/R/R costs, +25% trade bonds",
    "NAK": f"+50% mining profits, +150% minor faction rep gain & +120% S&R profits",
    "PRA": f"+30& exobio profits, +150% minor faction rep gain & +50% tech trade profits",
    "YRG": f"",
    "ZMT": f"Zemina Torval",
}
"""
Perks that powers offer
"""

POWER_BEST_FOR = {
    "ALD": "Bounty Hunters",
    "ARD": "Smugglers",
    "ASD": "Background Simulation Players",
    "DPT": "Bounty Hunters",
    "EMH": "Traders",
    "FLW": "Search & Rescue",
    "JRA": "Bounty Hunters",
    "LYR": "Explorers",
    "NAK": "Search & Rescue",
    "PRA": "Exobiologists",
    "YRG": "Bounty Hunters",
    "ZMT": "Miners",
}
"""
The powers and their shortcodes
"""

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
    "POWER TRACKER MALWARE",  # undermine
    "POWER INJECTION MALWARE",  # reinforce
]
