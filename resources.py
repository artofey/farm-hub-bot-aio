sample = """Not enough materials. Missing:
 6 x Bone
 64 x Pelt"""

resources_dict = {
    1: 'Thread',
    2: 'Stick',
    3: 'Pelt',
    4: 'Bone',
    5: 'Coal',
    6: 'Charcoal',
    7: 'Powder',
    8: 'Iron Ore',
    9: 'Cloth',
    10: 'Silver Ore',
    11: 'Bauxite',
    12: 'Cord',
    13: 'Magic Stone',
    14: 'Wooden Shaft',
    15: 'Sapphire',
    16: 'Solvent',
    17: 'Ruby',
    18: 'Hardener',
    19: 'Steel',
    20: 'Leather',
    21: 'Bone Powder',
    22: 'String',
    23: 'Coke',
    24: 'Purified Powder',
    25: 'Silver Alloy',
    27: 'Steel Mold',
    28: 'Silver Mold',
    29: 'Blacksmith Frame',
    30: 'Artisan Frame',
    31: 'Rope',
    32: 'Silver Frame',
    33: 'Metal Plate',
    34: 'Metallic Fiber',
    35: 'Crafted Leather',
    36: 'Quality Cloth',
    37: 'Blacksmith Mold',
    38: 'Artisan Mold'
}

resource_name_to_id = {}

for id, name in resources_dict.items():
    resource_name_to_id[name] = id


class Resource:
    def __init__(self, name, quantity=0):
        self.name = name
        if resource_name_to_id[name] <= 9:
            self.id = '0' + str(resource_name_to_id[name])
        else:
            self.id = str(resource_name_to_id[name])
        self.quantity = quantity


def parse_message(message):
    resources = []
    for line in message.splitlines()[1:]:
        q, name = line.lstrip(' ').split(' x ')
        resources.append(Resource(name, q))
    return resources


def withdraw(resources):
    command = '/g_withdraw'
    for resource in resources:
        command += f" {resource.id} {resource.quantity}"
    return command


def missing_to_withdraw(message):
    parsed = parse_message(message)
    return withdraw(parsed)
