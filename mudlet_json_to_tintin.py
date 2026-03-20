#!/usr/bin/env python3
"""
Mudlet Native JSON to TinTin++ Map Converter for NyyMap from TorilMud
Converts Mudlet's native JSON map export to TinTin++ commands
"""

import json
import sys
import re

# Embedded area list - extracted from arealist.tin
# This can be overridden by providing an arealist.tin file as an argument
AREALIST = {
    '0': 'God Rooms',
    '1': 'Misc Code Items/Mobs',
    '2': 'The Day/Night Load Zone',
    '3': 'The Quests Zone',
    '4': 'Misc Code Items/Mobs 2',
    '5': 'Kobold Settlement',
    '6': 'None of Your Business',
    '7': 'Ako Village',
    '8': 'The High Road',
    '9': 'The Troll Hills',
    '10': 'Valley of Crushk',
    '11': 'RP ZONE - Annam',
    '12': 'The Day/Night Load Zone 2',
    '13': 'The Conquered Village',
    '14': 'The Long Delay Zone',
    '15': 'the Deep Jungle',
    '16': 'Southern Waterdeep Main City',
    '17': 'Northern Waterdeep Main City',
    '18': 'Central Waterdeep Main City',
    '19': 'Wilderness Roads',
    '20': 'Waterdeep Trails',
    '21': 'The Scardale Sewers',
    '22': 'The Elemental Groves',
    '23': 'Caves of Mt. Skelenak',
    '24': 'The Underworld',
    '25': 'Alterian Region - Wilderness',
    '26': 'Alterian Region - Mountains',
    '27': 'Labyrinth of No Return',
    '28': 'The Great Harbor of Waterdeep',
    '29': 'The Guilds of Waterdeep',
    '30': 'The Ashstone Trail',
    '31': 'The Western Realms',
    '32': 'The Chionthar Ferry',
    '33': 'Scornubel',
    '34': 'Mithril Hall - City of Dwarves',
    '35': 'The Tunnel to Ardn\'ir',
    '36': 'Bloodstone Keep',
    '37': 'Distro Rooms/Generic Objects',
    '38': 'Leuthilspar - City of Elves',
    '39': 'Ribcage: Gate Town to Baator',
    '40': 'Keprum Vhai\'rels Design',
    '41': 'The Dark Gate',
    '42': 'Keprum Vhai\'rels Test',
    '43': 'Keprum - Captain Quest',
    '44': 'The Lost Treasure of Zaor',
    '45': 'Klauthen Vale',
    '46': 'Great Northern Road',
    '47': 'Village of Split Shield',
    '48': 'Griffon\'s Nest',
    '49': 'The Valley of Graydawn',
    '50': 'The Realms Master - Ship',
    '51': 'The Silver Lady - Ship',
    '52': 'IX Curtain',
    '53': 'Ghore - City of Trolls',
    '54': 'Lava Tubes One',
    '55': 'Lava Tubes Two',
    '56': 'Herd Island Chasm',
    '57': 'Ixarkon Prison',
    '58': 'The Temple of Baphomet',
    '59': 'Lake Skeldrach Island',
    '60': 'Lake Skeldrach Shore',
    '61': 'Lake Skeldrach',
    '62': 'The Citadel',
    '63': 'The Adamantite Mine',
    '64': 'The Lurkwood',
    '65': 'The Evermoors',
    '66': 'Talthalra Haszakkin',
    '67': 'Faerie Realm',
    '68': 'Wilderness Near Waterdeep',
    '69': 'The Waterdeep Coast Road',
    '70': 'Evermeet Bay',
    '71': 'The_Wildland_Trails',
    '72': 'Southern Forest',
    '73': 'Tower of High Sorcery One',
    '74': 'New Cavecity',
    '75': 'Faang - City of Ogres',
    '76': 'The Ice Prison',
    '77': 'Beluir - City of Halflings',
    '78': 'The Keep of Finn McCumhail',
    '79': 'The Sunken Slave City',
    '80': 'The Ant Farm',
    '81': 'The Blood Bayou',
    '82': 'Earth Plane',
    '83': 'The Dread Mist',
    '84': 'Ashstone Keep Road',
    '85': 'Ashstone',
    '86': 'The Nightwood',
    '87': 'Nightwood Border',
    '88': 'Ashstone Refugee Camp',
    '89': 'The Astral Plane - Main Grid',
    '90': 'The Astral Plane - Side Areas',
    '91': 'The Astral Plane - Tiamat',
    '92': 'Pirate Isles',
    '93': 'Stronghold of Trahern Oakvale',
    '94': 'New Nhavan Island',
    '95': 'The Calimshan Desert',
    '96': 'Viperstongue Outpost',
    '97': 'The Roads of the Heartland',
    '98': 'The Roads of the Heartland 2',
    '99': 'Shaman Quest/Spirit World',
    '100': 'Dobluth Kyor - Main City',
    '101': 'The Forest of Mir',
    '102': 'Rimi Greatoath dagger quest',
    '103': 'Barnabas dagger quest',
    '104': 'Conquest Armor Quest',
    '105': 'The Marching Mountains',
    '106': 'The Zone of Many Invasions',
    '107': 'Bloodstone Keep II',
    '108': 'Bloodstone Keep III',
    '109': 'The Ethereal Plane',
    '110': 'Deep Within the Toadsquat Mnts',
    '111': 'Tiamat - The Pillar of Skulls',
    '112': 'Tiamat - The Lair',
    '113': 'Beneath the Ancient Pyramid',
    '114': 'The Plane of Air Part One',
    '115': 'The Plane of Fire Part One',
    '116': 'The Plane of Fire Part Two',
    '117': 'The Plane of Fire -Planar Grid-',
    '118': 'Cityguard\'s Armoury',
    '119': 'The Pit of Souls',
    '120': 'The Shadow Swamp',
    '121': 'Troll King',
    '122': 'New Moonshae Island I',
    '123': 'The Ancient Oak',
    '124': 'Myrloch Vale',
    '125': 'The Headquarters of the Twisted Rune',
    '126': 'The New Trackless Sea',
    '127': 'The Nine Hells - Avernus',
    '128': 'The Nine Hells - Avernus - Bronze Citadel',
    '129': 'Bryn Shander',
    '130': 'The Eastway',
    '131': 'The Elemental Plane of Magma',
    '132': 'The Basin Wastes',
    '133': 'Gloomhaven',
    '134': 'The Derro Pit',
    '135': 'The Tunnel of Dread',
    '136': 'The Gloomhaven Barge',
    '137': 'Ruins of Yath Oloth',
    '138': 'The Jungle City of Hyssk',
    '139': 'The River Trail to Hyssk',
    '140': 'The Necromancer\'s Laboratory',
    '141': 'Randars Hideout',
    '142': 'The Orcish Hall of Plunder',
    '143': 'Rurrgr T\'ohrr',
    '144': 'The Sylvan Glades',
    '145': 'The Shining Sea One',
    '146': 'Desert City of Nizari',
    '147': 'The Sedawi Mountain Village',
    '148': 'The Elder Anthology',
    '149': 'The High Road - Side Areas',
    '150': 'Dark Forest',
    '151': 'Rogath Swamp',
    '152': 'The Comarian Mines',
    '153': 'The Temple of Blipdoolpoolp',
    '154': 'The Temple of the Moon',
    '155': 'The Elder Forest',
    '156': 'Demiplane of Artimus Nevarlith',
    '157': 'Ophidian Jungle',
    '158': 'Hive of the Manscorpions',
    '159': 'Lost Library of the Seer Kings',
    '160': 'The Temple of Twisted Flesh',
    '161': 'Mosswood Village',
    '162': 'Calimport the City',
    '163': 'Calimport the Sewers',
    '164': 'Calimport the Docks',
    '165': 'Calimport the Palace',
    '166': 'Calimport The Sea Sprite',
    '167': 'Pirate Ship Captain\'s Fancy',
    '168': 'Calimport The Barracuda',
    '169': 'Hyssk Ship/Dragon Turtle Path',
    '170': 'Hyssk Ship/Dragon Turtle Stuff',
    '171': 'Thunderhead Peak',
    '172': 'The Darktree',
    '173': 'Caravan Trail to the Ten Towns',
    '174': 'Calimport Palace Vault',
    '175': 'Acheron 1 Avalas',
    '176': 'Acheron 2 Thuldanin',
    '177': 'Acheron 3 Tintibulus',
    '178': 'Acheron 4 Ocanthus',
    '179': 'Arnd\'ir',
    '181': 'Neshkal - The Dragon Trail',
    '182': 'Hulburg Trail',
    '183': 'The Onyx Tower of Illusion',
    '184': 'Druids Grove',
    '185': 'The Curse of Newhaven',
    '186': 'The Curse of Newhaven_II',
    '187': 'The Llyrath Forest',
    '188': 'Choking Palace',
    '189': 'The Swamps of Meilech',
    '190': 'The Jungles of Ssrynss',
    '191': 'Trollbark',
    '192': 'A Halruaan Airship 1',
    '193': 'A Halruaan Airship 2',
    '194': 'The Floating Fortress of Izan Frosteyes',
    '195': 'The Lost Pyramid',
    '196': 'The Sewers of Waterdeep',
    '197': 'The Blackwood',
    '198': 'Cursed Cemetery',
    '199': 'The Seven Heavens - Lunia',
    '200': 'Bahamut\'s Palace',
    '201': 'The Plane of Smoke',
    '202': 'Cloud Realms of Arlurrium',
    '203': 'Muspelhiem',
    '204': 'Hulburg',
    '205': 'The Minotaur Outpost',
    '206': 'A\'Quarthus Velg\'Larn',
    '207': 'The Para-Elemental Plane of Ice',
    '208': 'Ashgorrock the Gargoyle City',
    '209': 'Tower of the Elementalist',
    '210': 'The Druid Forest',
    '211': 'Seelie Faerie Court',
    '212': 'Yggdrasil',
    '213': 'Scardale',
    '214': 'Abandoned Temple',
    '215': 'Soulprison of Bhaal',
    '216': 'The Golem Forge',
    '217': 'Ashrumite_Village',
    '218': 'The Neverwinter Wood Beta',
    '219': 'Jungle Village of the Batiri',
    '220': 'The Drider Cavern',
    '221': 'Unseelie Faerie Court',
    '222': 'Skullport Port of Shadows',
    '223': 'Skullport Helper Zonelet',
    '224': 'Wyllowwood',
    '225': 'The Dwarven Mining Settlement',
    '226': 'Spiderhaunt Woods',
    '227': 'Farm of the Undead',
    '228': 'Fire Giants Village',
    '229': 'Temple of Dumathoin',
    '230': 'Zhentil Keep',
    '231': 'Lair of the Deep Dragon',
    '232': 'UnderDark River Ruins',
    '233': 'Myth Drannor-Eastern City',
    '234': 'Roads of Cormanthor',
    '235': 'Myth Drannor-Central City',
    '236': 'Myth Drannor-Western City',
    '237': 'Silverymoon Gem of the North',
    '238': 'Veldrin Z\'har',
    '239': 'Dragonsfall Forest',
    '240': 'Menden-on-the-Deep',
    '241': 'The Defense of Longhollow',
    '242': 'The Cursed City of West Falls',
    '243': 'The Bandit Hideout',
    '244': 'Scornubel Ferry',
    '245': 'Calimshan Beach',
    '246': 'The Tarsellian Forest',
    '247': 'The Dusk Road',
    '248': 'The Fog Enshrouded Wood',
    '249': 'The Northern High Road',
    '250': 'The Northern High Road-2',
    '251': 'The Northern Caravan Trail',
    '252': 'The Mirar Ferry',
    '253': 'The Abandoned Monastery',
    '254': 'Baldur\'s Gate - Main City',
    '255': 'Baldur\'s Gate - Docks',
    '256': 'Baldur\'s Gate - Harbor',
    '257': 'Baldur\'s Gate - Wave Dancer',
    '258': 'The Ruins of Undermountain I',
    '259': 'Myth Unnohyr',
    '260': 'The Ruins of Undermountain II',
    '261': 'The Trader\'s Road',
    '262': 'The Reaching Woods - Part I',
    '263': 'Darkhold Castle',
    '264': 'Bloodtusk',
    '265': 'Mistywood',
    '266': 'Castle Drulak',
    '267': 'Jotunheim',
    '268': 'Talenrock',
    '269': 'Ixarkon - City of Mindflayers',
    '270': 'The Greycloak Hills',
    '271': 'The Brain Stem Tunnel',
    '272': 'IceCrag Castle',
    '273': 'IceCrag Castle - Lower Level',
    '274': 'Swift-Steel Company',
    '275': 'Havenport',
    '276': 'The Spirit Raven',
    '277': 'Skerttd-Gul',
    '278': 'Trade',
    '279': 'Shadow Dimension Rooms',
    '280': 'Guildhalls-Triterium',
    '281': 'Imphras Guild Hall',
    '282': 'Tooth and Maw - Grilled Grawl',
    '283': 'Pride of the Sabertooth Guildhall',
    '284': 'Valkurian Blades Guildhall',
    '285': 'Guildhalls - Warder\'s Vault',
    '286': 'Kingdoms and Houses',
    '287': 'The Questbuilding Zone',
    '288': 'Lizard Marsh',
    '289': 'The Ruined Keep',
    '290': 'The Stag Forest',
    '291': 'The Stump Bog',
    '292': 'The Way Inn',
    '293': 'Evermeet- Elven Settlement',
    '294': 'The Evermoor Way',
    '295': 'The Rauvin Ride',
    '296': 'Ogre Lair',
    '297': 'Fire Giant Lair',
    '298': 'Ancient Mines',
    '299': 'Evermeet- Rogue\'s Lair',
    '300': 'Kobold Caverns',
    '301': 'Evermeet- Hidden Mine',
    '302': 'Dragonspear Castle',
    '303': 'Alabaster Caverns',
    '304': 'Crystal Caverns',
    '305': 'Seaweed Tribe',
    '306': 'The Dark Dominion',
    '307': 'Underdark Tunnels',
    '308': 'The Luskan Outpost',
    '309': 'The Dragonspine Mountains Trail',
    '310': 'Darklake',
    '311': 'The Trade Way',
    '312': 'Illithid Enclave',
    '313': 'The Labyrinth',
    '314': 'The Tower of Kenjin',
    '315': 'Settlestone',
    '316': 'Wormwrithings',
    '317': 'Menzoberranzan',
    '318': 'Water Plane',
    '319': 'The Temple of Ghaunadaur',
    '320': 'The Fortress of the Dragon Cult',
    '321': 'Evermeet- Scorched Forest',
    '322': 'Evermeet- Serene Forest',
    '323': 'Amenth\'G\'narr',
    '324': 'Elg\'cahl Niar',
    '325': 'The Rat Hills',
    '326': 'Mithril Hall Palace',
    '327': 'Barbarian Encampment',
    '328': 'Evermeet- Main Road',
    '329': 'Evermeet- East Coast Road North',
    '330': 'Evermeet- West Coast Road North',
    '331': 'Evermeet- Ancient Forest-1',
    '332': 'Evermeet- Misc. Rooms/Mobs',
    '333': 'Evermeet- Road to Elven Settlement',
    '334': 'The Underdark Trade Route',
    '335': 'Grid-Desert-Calimport1',
    '336': 'Grid-Desert-Calimport2',
    '337': 'Grid-Forest-Bloodtusk',
    '338': 'Grid-Hills-Bloodtusk',
    '339': 'Grid-Hills-Bloodtusk2',
    '340': 'Grid-Arctic-MH',
    '341': 'Grid-Arctic-MH2',
    '342': 'Grid-Arctic-GN',
    '343': 'Grid-Hills-WD',
    '344': 'Grid-Hills-Ashrumite',
    '345': 'Grid-Hills-GN',
    '346': 'Grid-Jungle-Hyssk',
    '347': 'Grid-Jungle-Hyssk2',
    '348': 'Grid-UD-Ixarkon',
    '349': 'Grid-UD-GH',
    '350': 'Grid-UD-Mir',
    '351': 'Grid-Forest-WD',
    '352': 'Grid-Forest-Faang',
    '353': 'Grid-Forest-Leuthilspar',
    '354': 'Grid-Forest-Leuthilspar2',
    '355': 'The End of the World',
    '356': 'Westgate',
    '357': 'Crypt of Dragons',
    '358': 'Nine Hells - Dis',
}

def load_arealist(filename=None):
    """Load area list from file, or use embedded AREALIST if no file provided"""
    if filename is None:
        print(f"#nop Using embedded arealist ({len(AREALIST)} areas)", file=sys.stderr)
        return AREALIST
    
    arealist = {}
    try:
        with open(filename, 'r') as f:
            content = f.read()
            # Parse the TinTin++ variable format
            # Looking for lines like: {222} {Skullport Port of Shadows}
            pattern = r'\{(\d+)\}\s*\{([^}]+)\}'
            matches = re.findall(pattern, content)
            for zone_id, area_name in matches:
                arealist[zone_id] = area_name
        print(f"#nop Loaded {len(arealist)} areas from {filename}", file=sys.stderr)
        return arealist
    except FileNotFoundError:
        print(f"#nop Warning: {filename} not found, using embedded arealist", file=sys.stderr)
        return AREALIST

def get_short_dir(direction):
    """Convert long direction to short form"""
    dir_map = {
        'north': 'n', 'south': 's', 'east': 'e', 'west': 'w',
        'northeast': 'ne', 'northwest': 'nw', 
        'southeast': 'se', 'southwest': 'sw',
        'up': 'u', 'down': 'd'
    }
    return dir_map.get(direction, direction)

def is_standard_direction(exit_name):
    """Check if exit is a standard direction"""
    standard_dirs = ['north', 'south', 'east', 'west', 
                     'northeast', 'northwest', 'southeast', 'southwest',
                     'up', 'down']
    return exit_name in standard_dirs

def escape_braces(text):
    """Escape braces and backslashes for TinTin++"""
    if text is None:
        return ''
    # Escape backslashes first, then braces
    text = text.replace('\\', '\\\\')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    return text

def parse_exit_names(exit_names_str):
    """Parse the exitNames JSON string from userData"""
    if not exit_names_str:
        return {}
    try:
        # The exitNames is stored as escaped JSON string
        # Example: "{\"west\":\"secret\"}"
        exit_names_dict = json.loads(exit_names_str)
        return exit_names_dict
    except:
        return {}

def convert_map(json_file, arealist):
    """Convert Mudlet JSON map to TinTin++ commands"""
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    stats = {
        'rooms': 0,
        'exits': 0,
        'special_exits': 0,
        'doors': 0,
        'locked_doors': 0,
        'passwords': 0,
        'infos': 0,
        'custom_exit_names': 0
    }
    
    # Output TinTin++ header
    print("#nop ========================================================================;")
    print("#nop Auto-generated TinTin++ map from Mudlet JSON export;")
    print("#nop ========================================================================;")
    print()
    print("#map create 100000;")
    print()
    
    # Find rooms in the JSON structure
    rooms = []
    if 'areas' in data and isinstance(data['areas'], list):
        # Multiple areas format
        for area in data['areas']:
            if 'rooms' in area:
                rooms.extend(area['rooms'])
    elif 'rooms' in data:
        # Single area format
        rooms = data['rooms']
    
    # First pass: Create all rooms with basic info
    for room in rooms:
        room_id = room.get('id')
        if room_id is None:
            continue
            
        stats['rooms'] += 1
        
        # Go to/create room
        print(f"#map goto {{{room_id}}} {{dig}};")
        
        # Set room name
        room_name = room.get('name', '')
        if room_name:
            room_name_escaped = escape_braces(room_name)
            print(f"#map set roomname {{{room_name_escaped}}};")
        
        # Set room description
        user_data = room.get('userData', {})
        description = user_data.get('description', '')
        if description:
            # Escape braces first
            desc_escaped = escape_braces(description)
            # Then replace actual newlines with \n (without re-escaping)
            desc_escaped = desc_escaped.replace('\n', r'\n')
            print(f"#map set roomdesc {{{desc_escaped}}};")
        
        # Set room area
        zone_id = user_data.get('zoneid', '')
        if zone_id:
            area_name = arealist.get(zone_id, zone_id)
            area_name_escaped = escape_braces(area_name)
            print(f"#map set roomarea {{{area_name_escaped}}};")
        
        # Build roomnote by combining password and infos
        roomnote_parts = []
        
        password = user_data.get('password', '')
        if password:
            roomnote_parts.append(f"Password: {password}")
            stats['passwords'] += 1
        
        infos = user_data.get('infos', '')
        if infos:
            roomnote_parts.append(infos)
            stats['infos'] += 1
        
        # Only set roomnote if we have something to add
        if roomnote_parts:
            combined_note = ' | '.join(roomnote_parts)
            combined_note_escaped = escape_braces(combined_note)
            print(f"#map set roomnote {{{combined_note_escaped}}};")
        
        print()  # Blank line between rooms
    
    # Second pass: Create exits and links
    for room in rooms:
        room_id = room.get('id')
        if room_id is None:
            continue
        
        user_data = room.get('userData', {})
        password = user_data.get('password', '')
        
        # Parse custom exit names
        exit_names_str = user_data.get('exitNames', '')
        custom_exit_names = parse_exit_names(exit_names_str)
        
        exits = room.get('exits', [])
        
        for exit_data in exits:
            exit_name = exit_data.get('name', '')
            exit_id = exit_data.get('exitId')
            door_status = exit_data.get('door')
            is_locked = exit_data.get('locked', False) or door_status == 'locked'
            
            if not exit_name or exit_id is None:
                continue
            
            # Determine if standard direction or special exit
            if is_standard_direction(exit_name):
                # Standard directional exit
                stats['exits'] += 1
                short_dir = get_short_dir(exit_name)
                
                print(f"#map goto {{{room_id}}};")
                print(f"#map link {{{short_dir}}} {{{exit_id}}};")
                
                # Check for custom exit name
                custom_name = custom_exit_names.get(exit_name, '')
                
                # Handle doors
                if door_status:
                    stats['doors'] += 1
                    
                    if is_locked:
                        stats['locked_doors'] += 1
                        
                        if password:
                            # Locked with password - create command with password
                            if custom_name:
                                # Custom door name: "say password;open customname direction;direction"
                                print(f"#map exit {{{short_dir}}} command {{say {password};open {custom_name} {exit_name};{short_dir}}};")
                            else:
                                # Standard door: "say password;open door direction;direction"
                                print(f"#map exit {{{short_dir}}} command {{say {password};open door {exit_name};{short_dir}}};")
                        else:
                            # Locked without password - mark as avoid
                            print(f"#map exitflag {{{short_dir}}} avoid;")
                    
                    elif door_status == 'closed':
                        # Just closed, not locked
                        if custom_name:
                            # Custom door name: "open customname direction;direction"
                            print(f"#map exit {{{short_dir}}} command {{open {custom_name} {exit_name};{short_dir}}};")
                        else:
                            # Standard door: "open door direction;direction"
                            print(f"#map exit {{{short_dir}}} command {{open door {exit_name};{short_dir}}};")
                
                elif custom_name:
                    # No door but has custom name - just track it
                    stats['custom_exit_names'] += 1
                    # Could optionally set custom exit name here if TinTin++ supports it
                
                print()
            
            else:
                # Special exit (portal, command, etc)
                stats['special_exits'] += 1
                
                # Take everything before the | if present
                special_command = exit_name.split('|')[0] if '|' in exit_name else exit_name
                special_command_escaped = escape_braces(special_command)
                
                print(f"#map goto {{{room_id}}};")
                print(f"#map dig {{{special_command_escaped}}} {{{exit_id}}};")
                print()
    
    # Output statistics
    print()
    print("#nop ========================================================================;")
    print("#nop Conversion Statistics;")
    print("#nop ========================================================================;")
    for key, value in stats.items():
        print(f"#nop {key}: {value};")
    print("#nop ========================================================================;")
    
    return stats

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 mudlet_json_to_tintin.py <mudlet_map.json> [arealist.tin]", file=sys.stderr)
        print("", file=sys.stderr)
        print("The arealist.tin file is OPTIONAL. If not provided, the script uses", file=sys.stderr)
        print("an embedded arealist with 358 zones from your MUD.", file=sys.stderr)
        sys.exit(1)
    
    json_file = sys.argv[1]
    arealist_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Load area list (uses embedded AREALIST if no file provided)
    arealist = load_arealist(arealist_file)
    
    # Convert the map
    convert_map(json_file, arealist)
