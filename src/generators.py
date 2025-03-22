import random
import hashlib
from datetime import datetime, timedelta
import yaml


class Generator:
	def __init__(self):
		pass
	
	def get_random(self, conf_options: dict):
		pass


class EmailGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, conf_options: dict):
		email = 'DW'
		
		r_name = ''.join([chr(random.randint(65, 123)) for _ in range(random.randint(8, 16))])
		email = '-'.join([email, r_name])
		
		email = '-'.join([email, ''.join([str(random.randint(0, 10)) for _ in range(4)])])
		email = '@'.join([email, random.choice(['gmail.com', 'wp.pl'])])
		return email


class NameGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, conf_options: dict):
		names = ['Steve', 'Alex']
		return random.choice(names)


class SurnameGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, conf_options: dict):
		surnames = ['Kowalski', 'Bond']
		return random.choice(surnames)


class HashGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, conf_options: dict):
		password = ''.join([chr(random.randint(65, 123)) for _ in range(random.randint(8, 16))])
		return hashlib.sha256(password.encode()).hexdigest()


class NumberGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, conf_options: dict):
		range_ = conf_options.get('range', [0, 100])
		return random.randint(*range_)


class ChoiceGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, conf_options: dict):
		return random.choices(conf_options.get('values', [None]), weights=conf_options.get('weights', [1]), k=1)[0]


class DateGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, conf_options: dict):
		start_date, end_date = conf_options.get('range', ["01-01-2023", "18-03-2024"])
		start_date = datetime.strptime(start_date, "%d-%m-%Y")
		end_date = datetime.strptime(end_date, "%d-%m-%Y")
		
		delta = end_date - start_date
		random_days = random.randint(0, delta.days)
		return (start_date + timedelta(days=random_days)).strftime("%d-%m-%Y")


GENERATORS = {
	"email": EmailGen,
	"name": NameGen,
	"surname": SurnameGen,
	"hash": HashGen,
	"number": NumberGen,
	"choice": ChoiceGen,
	"date": DateGen,
}


def create_new_instance(table_conf: dict):
	new_row = []
	for field, options in table_conf['fields'].items():
		generator = GENERATORS.get(options['generator'])()
		new_row.append(generator.get_random(options))
	return new_row


if __name__ == '__main__':
	with open("../configs/tables.yml", 'r') as ymlfile:
		config = yaml.safe_load(ymlfile)
	ins = create_new_instance(config.get("tables").get("Users"))
	print(ins)
