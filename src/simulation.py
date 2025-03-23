import pandas as pd
import scipy.stats as stats
import yaml
import datetime
import random

from generators import add_instance_to_population

N_INITIAL_AGENTS = 16
STARTING_DATE = "16-03-2025"
N_EPISODES = 2

REQUESTS_LAMBDA = 8
CHANCE_FROM_NEW_USER = 0.8

READ_EXISTING_FILES = False

CHANCE_TO_FILL_THE_FORM = 0.14
CHANCE_FORM_VARIANTS = [0.8, 0.2]


def simulation_episode(
		df_users,
		df_agents,
		df_estates,
		df_requests,
		df_form,
		df_city,
		df_address,
		df_req_agent,
		entities_conf,
		today_date
):
	n_new_requests = int(stats.poisson.ppf(random.random(), mu=REQUESTS_LAMBDA))
	for _ in range(n_new_requests):
		variant_request = list(entities_conf["Request"].get("variants", {}).keys())
		variant_request = random.choice(variant_request) if variant_request else None  # todo: weights
		variant_estate = "House" if "House" in variant_request else "Flat"
		
		if random.random() <= CHANCE_FROM_NEW_USER:
			user = add_instance_to_population(df_users, entities_conf["User"], variant="User")
		else:
			n_users = len(df_users[df_users["IsStaff"] == False])
			if n_users <= 0:
				continue
			random_i = random.randint(0, n_users - 1)
			user = df_users[df_users["IsStaff"] == False].iloc[random_i].to_dict()
		
		variant_city = random.choice(list(entities_conf["City"].get("variants", {}).keys()))
		new_city = add_instance_to_population(df_city, entities_conf["City"], variant=variant_city)
		
		new_address = add_instance_to_population(
			df_address,
			entities_conf["Address"],
			ref_entities={"City": new_city}
		)
		
		new_estate = add_instance_to_population(
			df_estates,
			entities_conf["Estate"],
			variant=variant_estate,
			ref_entities={"User": user, "Address": new_address}
		)
		new_req = add_instance_to_population(
			df_requests,
			entities_conf["Request"],
			variant=variant_request,
			ref_entities={"User": user, "Estate": new_estate, "Agent": {}},
		)
		# Not the best way to do it, but it works
		df_requests.loc[len(df_requests) - 1, "CreatedAt"] = today_date.strftime("%d-%m-%Y")
		
		
		
		if random.random() <= CHANCE_TO_FILL_THE_FORM:
			variant_form = list(entities_conf["Form"].get("variants", {}).keys())
			variant_form = random.choices(variant_form, weights=CHANCE_FORM_VARIANTS, k=1)[0] if variant_form else None
			add_instance_to_population(
				df_form,
				entities_conf["Form"],
				variant=variant_form,
				ref_entities={"User": user},
			)


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
	
	if READ_EXISTING_FILES:
		df_users = pd.read_csv(entities_conf["User"]["path"])
		df_agents = pd.read_csv(entities_conf["Agent"]["path"])
		df_estates = pd.read_csv(entities_conf["Estate"]["path"])
		df_requests = pd.read_csv(entities_conf["Request"]["path"])
		df_form = pd.read_csv(entities_conf["Form"]["path"])
		df_city = pd.read_csv(entities_conf["City"]["path"])
		df_address = pd.read_csv(entities_conf["Address"]["path"])
		df_req_agent = pd.read_csv(entities_conf["RequestAgent"]["path"])
	else:
		df_users = pd.DataFrame(columns=entities_conf["User"]["fields"].keys())
		df_agents = pd.DataFrame(columns=entities_conf["Agent"]["fields"].keys())
		df_estates = pd.DataFrame(columns=entities_conf["Estate"]["fields"].keys())
		df_requests = pd.DataFrame(columns=entities_conf["Request"]["fields"].keys())
		df_form = pd.DataFrame(columns=entities_conf["Form"]["fields"].keys())
		df_city = pd.DataFrame(columns=entities_conf["City"]["fields"].keys())
		df_address = pd.DataFrame(columns=entities_conf["Address"]["fields"].keys())
		df_req_agent = pd.DataFrame(columns=entities_conf["RequestAgent"]["fields"].keys())
	
	# Add initial Agents
	if not READ_EXISTING_FILES:
		for i in range(N_INITIAL_AGENTS):
			new_agent = add_instance_to_population(df_users, entities_conf["User"], variant="Agent")
			add_instance_to_population(df_agents, entities_conf["Agent"], ref_entities={"User": new_agent})
	
	# for N days
	today_date = datetime.datetime.strptime(STARTING_DATE, "%d-%m-%Y")
	for i in range(N_EPISODES):
		simulation_episode(
			df_users, df_agents, df_estates, df_requests, df_form, df_city, df_address, df_req_agent,
			entities_conf, today_date
		)
		today_date = today_date + datetime.timedelta(days=1)
	#   ? some new requests
	
	df_users.to_csv(entities_conf["User"]["path"], index=False)
	df_agents.to_csv(entities_conf["Agent"]["path"], index=False)
	df_estates.to_csv(entities_conf["Estate"]["path"], index=False)
	df_requests.to_csv(entities_conf["Request"]["path"], index=False)
	df_form.to_csv(entities_conf["Form"]["path"], index=False)
	df_city.to_csv(entities_conf["City"]["path"], index=False)
	df_address.to_csv(entities_conf["Address"]["path"], index=False)
	df_req_agent.to_csv(entities_conf["RequestAgent"]["path"], index=False)


if __name__ == '__main__':
	main()
