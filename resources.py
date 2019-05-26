sample = """Not enough materials. Missing:
 6 x Bone
 64 x Pelt
 2 x Iron ore"""

resources_dict = {
    1: 'Thread',
    2: 'Stick',
    3: 'Pelt',
    4: 'Bone',
    5: 'Coal',
    6: 'Charcoal',
    7: 'Powder',
    8: 'Iron ore',
    9: 'Cloth',
    10: 'Silver ore',
    11: 'Bauxite',
    12: 'Cord',
    13: 'Magic stone',
    14: 'Wooden shaft',
    15: 'Sapphire',
    16: 'Solvent',
    17: 'Ruby',
    18: 'Hardener',
    19: 'Steel',
    20: 'Leather',
    21: 'Bone powder',
    22: 'String',
    23: 'Coke',
    24: 'Purified powder',
    25: 'Silver alloy',
    27: 'Steel mold',
    28: 'Silver mold',
    29: 'Blacksmith frame',
    30: 'Artisan frame',
    31: 'Rope',
    32: 'Silver frame',
    33: 'Metal plate',
    34: 'Metallic fiber',
    35: 'Crafted leather',
    36: 'Quality cloth',
    37: 'Blacksmith mold',
    38: 'Artisan mold'
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
