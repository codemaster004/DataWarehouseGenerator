import random

import yaml

with open("../config.yml", "r") as ymlfile:
	config = yaml.safe_load(ymlfile)

print(config.get('tables', {}))
print(config.get('tables', {}).get('Users', {}))
print(config.get('tables', {}).get('Users', {}).get('path', {}))
print(config.get('tables', {}).get('Users', {}).get('fields', {}))
print(config.get('tables', {}).get('Users', {}).get('fields', {}).get('PhoneNumber', {}))
print(config.get('tables', {}).get('Users', {}).get('fields', {}).get('PhoneNumber', {}).get('unique', {}))
print(config.get('tables', {}).get('Users', {}).get('fields', {}).get('PhoneNumber', {}).get('range', {})[0])

print(chr(random.randint(65, 123)))

