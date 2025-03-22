import random

import yaml

with open("../configs/entities.yml", "r") as ymlfile:
	config = yaml.safe_load(ymlfile)

print(config.get('entities', {}))
print(config.get('entities', {}).get('Users', {}))
print(config.get('entities', {}).get('Users', {}).get('path', {}))
print(config.get('entities', {}).get('Users', {}).get('fields', {}))
print(config.get('entities', {}).get('Users', {}).get('fields', {}).get('PhoneNumber', {}))
print(config.get('entities', {}).get('Users', {}).get('fields', {}).get('PhoneNumber', {}).get('unique', {}))
print(config.get('entities', {}).get('Users', {}).get('fields', {}).get('PhoneNumber', {}).get('range', {})[0])

print(chr(random.randint(65, 123)))

