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
CHANCE_FROM_NEW_USER = 0.9


def simulation_episode(df_users, df_estates, df_requests, entities_conf):
	n_new_requests = int(stats.poisson.ppf(random.random(), mu=REQUESTS_LAMBDA))
	for _ in range(n_new_requests):
		if random.random() <= CHANCE_FROM_NEW_USER:
			new_user = add_instance_to_population(df_users, entities_conf["User"], variant="User")
			new_estate = add_instance_to_population(
				df_estates,
				entities_conf["Estate"],
				variant="House",
			)
			
		else:
			pass  # todo: in future pick random user


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
	df_estates = pd.DataFrame(columns=entities_conf["Estate"]["fields"].keys())
	df_requests = pd.DataFrame(columns=entities_conf["Request"]["fields"].keys())
	for i in range(N_INITIAL_AGENTS):
		new_agent = add_instance_to_population(df_users, entities_conf["User"], variant="Agent")
		add_instance_to_population(df_agents, entities_conf["Agent"], ref_entities={"User": new_agent})
	
	# for N days
	today_date = datetime.datetime.strptime(STARTING_DATE, "%d-%m-%Y")
	for i in range(N_EPISODES):
		simulation_episode(df_users, df_estates, df_requests, entities_conf)
		today_date = today_date + datetime.timedelta(days=1)
	#   ? some new requests
	
	df_users.to_csv("../data/users.csv")
	df_agents.to_csv("../data/agents.csv")
	df_estates.to_csv("../data/estates.csv")
	df_requests.to_csv("../data/requests.csv")


if __name__ == '__main__':
	main()
