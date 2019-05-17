sample = """Not enough materials. Missing:
 6 x Bone
 64 x Pelt"""

resources_dict = {
    1: 'Thread',
    2: 'Stick',
    3: 'Pelt',
    4: 'Bone'}

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
