import random
import hashlib
from datetime import datetime, timedelta

import pandas as pd
import yaml
import math


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
		if 'weights' in conf_options:
			result = random.choices(conf_options.get('values', [None]), weights=conf_options['weights'], k=1)[0]
		else:
			result = random.choice(conf_options.get('values', [None]))
		return result


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


def create_new_instance(ins_conf: dict, population: pd.DataFrame, variant: str | None, references: dict | None) -> dict:
	new_ins = {}
	for field, options in ins_conf['fields'].items():
		if variant is not None:
			options.update(ins_conf['variants'][variant].get(field, {}))
		
		if 'autoIncrement' in options.keys():
			attribute = population[field].max()
			if math.isnan(attribute):
				attribute = options['autoIncrement'] - 1
			new_ins[field] = attribute + 1
			continue
		
		if 'reference' in options.keys():
			entity, attribute = options['reference'].split('+')
			new_ins[field] = references[entity][attribute]  # todo: try catch...
			continue
		
		generator = GENERATORS.get(options['generator'])()
		new_ins[field] = generator.get_random(options)
	return new_ins


def handle_unique_values(population: pd.DataFrame, new_instance: dict, table_conf: dict) -> dict:
	return new_instance  # todo: implement


def add_instance_to_population(
		population: pd.DataFrame,
		instance_conf: dict,
		variant: str = None,
		ref_entities: dict = None
) -> dict:
	dependencies = instance_conf.get('dependsOn', [])
	if dependencies and ref_entities is None:
		print("WARNING: No references specified")
		return {}
	for dependency in dependencies:
		if dependency not in ref_entities:
			print(f"WARNING: Dependency '{dependency}' not found")
			return {}
	new_instance = create_new_instance(instance_conf, population, variant=variant, references=ref_entities)
	new_instance = handle_unique_values(population, new_instance, instance_conf)
	population.loc[len(population)] = new_instance
	return new_instance


if __name__ == '__main__':
	with open("../configs/entities.yml", 'r') as ymlfile:
		config = yaml.safe_load(ymlfile)
	ins = create_new_instance(config.get("entities").get("User"), 0, None, None)
	print(ins)
	ins = create_new_instance(config.get("entities").get("User"), 0, variant='Users', references=None)
	print(ins)
