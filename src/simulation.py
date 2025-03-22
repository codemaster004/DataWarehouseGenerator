import random

import pandas as pd
import scipy.stats as stats
import yaml
import datetime
import random

from generators import add_instance_to_population

N_INITIAL_AGENTS = 16
STARTING_DATE = "16-03-2025"
N_EPISODES = 10

REQUESTS_LAMBDA = 32


def simulation_episode():
	n_new_requests = int(stats.poisson.ppf(random.random(), mu=REQUESTS_LAMBDA))
	for _ in range(n_new_requests):
		pass


def main():
	# todo: prob to function
	entities_conf = None
	with open("../configs/entities.yml", 'r') as ymlfile:
		try:
			entities_conf = yaml.safe_load(ymlfile)['entities']
		except yaml.YAMLError as exc:
			print(exc)
		except KeyError as exc:
			print(exc)
	
	# todo: to function
	if entities_conf is None:
		print("No entities configuration")
		return
	
	# Add initial Agents
	df_users = pd.DataFrame(columns=entities_conf["User"]["fields"].keys())
	df_agents = pd.DataFrame(columns=entities_conf["Agent"]["fields"].keys())
	for i in range(N_INITIAL_AGENTS):
		new_ins = add_instance_to_population(df_users, entities_conf["User"], variant="Agent")
		add_instance_to_population(df_agents, entities_conf["Agent"], ref_entities={"User": new_ins})
	
	df_users.to_csv("../data/users.csv")
	df_agents.to_csv("../data/agents.csv")
	
	# for N days
	today_date = datetime.datetime.strptime(STARTING_DATE, "%d-%m-%Y")
	for i in range(N_EPISODES):
		simulation_episode()
		today_date = today_date + datetime.timedelta(days=1)
	#   ? some new requests
	pass


if __name__ == '__main__':
	main()
