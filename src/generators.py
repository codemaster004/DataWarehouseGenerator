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
		
		r_name = ''.join(
			[chr(random.choice(list(range(65, 91)) + list(range(97, 123)))) for _ in range(random.randint(8, 16))])
		email = '-'.join([email, r_name])
		
		email = '-'.join([email, ''.join([str(random.randint(0, 9)) for _ in range(4)])])
		email = '@'.join([email, random.choice([
			'gmail.com', 'wp.pl', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com', 'aol.com', 'protonmail.com',
			'zoho.com', 'gmx.com',
			'mail.com', 'yandex.com', 'tutanota.com', 'live.com', 'me.com', 'inbox.lv', 'o2.pl', 'onet.pl',
			'interia.pl', 'op.pl'])])
		return email


class NameGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, conf_options: dict):
		names = [
			'Steve', 'Alex', 'John', 'Michael', 'David', 'James', 'Robert', 'William', 'Joseph', 'Daniel',
			'Matthew', 'Andrew', 'Joshua', 'Christopher', 'Brian', 'Kevin', 'Thomas', 'Jonathan', 'Nicholas', 'Anthony',
			'Ryan', 'Jason', 'Jacob', 'Eric', 'Brandon', 'Tyler', 'Ethan', 'Benjamin', 'Noah', 'Samuel',
			'Henry', 'Nathan', 'Christian', 'Adam', 'Patrick', 'Richard', 'Logan', 'Zachary', 'Charles', 'Aaron',
			'Kyle', 'Sean', 'Dylan', 'Luke', 'Isaac', 'Gabriel', 'Owen', 'Mason', 'Eli', 'Connor'
		]
		return random.choice(names)


class SurnameGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, conf_options: dict):
		surnames = [
			'Kowalski', 'Bond', 'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia',
			'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor',
			'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez',
			'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen',
			'Hill', 'Flores', 'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell'
		]
		return random.choice(surnames)

class StreetGen:
	def __init__(self):
		super().__init__()

	def get_random(self, conf_options: dict):
		street_names = [
			"Marszalkowska", "Krucza", "Jana Pawla II", "Nowowiejska", "Koszykowa", "Targowa", "Pulawska",
			"Zielona", "Sloneczna", "Dluga", "Krotka", "Polna", "Lesna", "Lakowa", "Szkolna", "Koscielna",
			"Dworcowa", "Parkowa", "Swierkowa", "Brzozowa", "Topolowa", "Jasna", "Cicha", "Spokojna",
			"Kwiatowa", "Sosnowa", "Wesola", "Gorna", "Dolna", "Szeroka", "Waska", "Rynek", "Kosciuszki",
			"Mickiewicza", "Sienkiewicza", "Reymonta", "Chopina", "Moniuszki", "Norwida", "Zeromskiego",
			"Wyspianskiego", "Orzeszkowej", "Prusa", "Konopnickiej", "Slowackiego", "Krasinskiego",
			"Witosa", "Pilsudskiego", "Jagiellonska", "Sobieskiego", "Wladyslawa IV", "Brzozowa", "Dabrowska",
			"Lipowa", "Jesionowa", "Modrzewiowa", "Bukowa", "Kasztanowa", "Klonowa", "Jodlowa", "Akacjowa",
			"Debowa", "Oliwkowa", "Lesna", "Zaciszna", "Borowa", "Malinowa", "Jagodowa", "Morelowa", "Jabloniowa", "Winogronowa"
		]
		return random.choice(street_names)

class DistrictName(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, conf_options: dict):
		city_districts = {
			"Gdansk": [
				"Aniolki", "Bretowo", "Brzezno", "Chelm", "Jasien", "Krakowiec-Gorki Zachodnie",
				"Letnica", "Matarnia", "Mlyniska", "Nowy Port", "Olszynka", "Orunia Gorna-Gdansk Poludnie",
				"Orunia-Sw. Wojciech-Lipce", "Osowa", "Piecki-Migowo (Morena)", "Przerobka",
				"Przymorze Male", "Przymorze Wielkie", "Rudniki", "Siedlce", "Srodmiescie", "Stogi",
				"Strzyza", "Suchanino", "Ujescisko-Lostowice", "VII Dwor", "Wrzeszcz Dolny", "Wrzeszcz Gorny",
				"Wyspa Sobieszewska", "Zaspa-Mlyniec", "Zaspa-Rozstaje"
			],
			"Gdynia": [
				"Babie Doly", "Chwarzno-Wiczlino", "Cisowa", "Dabrowa", "Dzialki Lesne", "Grabowek",
				"Kamienna Gora", "Karwiny", "Leszczynki", "Maly Kack", "Obluze", "Oksywie", "Orlowo",
				"Pogorze", "Pustki Cisowskie-Demptowo", "Redlowo", "Srodmiescie", "Wielki Kack",
				"Witomino", "Wzgorze Sw. Maksymiliana"
			],
			"Sopot": [
				"Brodwino", "Centrum", "Dolny Sopot", "Gorny Sopot", "Kamienny Potok",
				"Karlikowo", "Przylesie"
			]
		}
		
		city = conf_options.get("city")
		
		if city in city_districts:
			return random.choice(city_districts[city])
		else:
			raise ValueError(f"Unknown city: {city}. Cannot determine districts.")


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
	"district": DistrictName,
	"street": StreetGen
}


def create_new_instance(ins_conf: dict, population: pd.DataFrame, variant: str | None, references: dict | None) -> dict:
	new_ins = {}
	for field, options in ins_conf['fields'].items():
		if options is None:  # for the edge case when all data is stored in variants
			options = {}
		
		if variant is not None:
			options.update(ins_conf['variants'][variant].get(field, {}))
		
		if 'value' in options.keys():
			attribute = options['value']
			new_ins[field] = attribute
			continue
		
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
