import random
import hashlib


class Generator:
	def __init__(self):
		pass
	
	def get_random(self, **kwargs):
		pass


class EmailGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, **kwargs):
		email = 'DW'
		
		r_name = ''.join([chr(random.randint(65, 123)) for _ in range(random.randint(8, 16))])
		email = '-'.join([email, r_name])
		
		email = '-'.join([email, ''.join([str(random.randint(0, 10)) for _ in range(4)])])
		email = '@'.join([email, random.choice(['gmail.com', 'wp.pl'])])
		return email


class NameGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, **kwargs):
		names = ['Steve', 'Alex']
		return random.choice(names)


class SurnameGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, **kwargs):
		surnames = ['Kowalski', 'Bond']
		return random.choice(surnames)


class HashGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, **kwargs):
		password = ''.join([chr(random.randint(65, 123)) for _ in range(random.randint(8, 16))])
		return hashlib.sha256(password.encode()).hexdigest()


class NumberGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, **kwargs):
		range_ = kwargs.get('range', [0, 100])
		return random.randint(*range_)


class ChoiceGen(Generator):
	def __init__(self):
		super().__init__()
	
	def get_random(self, **kwargs):
		pass
