from resources_dict import resources_dict

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


def parse_message(lines):
    resources = []
    for line in lines:
        q, name = line.lstrip(' ').split(' x ')
        resources.append(Resource(name.lower(), q))
    return resources


def withdraw(resources):
    command = '/g_withdraw'
    if len(resources) <= 8:
        for resource in resources:
            command += f" {resource.id} {resource.quantity}"
        return [command]
    else:
        return withdraw(resources[:7]) + withdraw(resources[8:])


def missing_to_withdraw(message):
    parsed = parse_message(filter(lambda line: line.startswith(' '), message.splitlines()))
    return withdraw(parsed)
