import pandas as pd
import scipy.stats as stats
import yaml
import datetime
import random

from generators import add_instance_to_population

N_INITIAL_AGENTS = 16
STARTING_DATE = "20-03-2025"
N_EPISODES = 1

REQUESTS_LAMBDA = 8
CHANCE_FROM_NEW_USER = 0.8

READ_EXISTING_FILES = True

CHANCE_TO_FILL_THE_FORM = 0.2
CHANCE_FORM_VARIANTS = [0.8, 0.2]

# CHANCE_USER_TO_PICK_RANDOM_AGENT = 0.2

CHANCE_AGENT_ACCEPTS_ASSIGNED_REQ = 0.2
CHANCE_AGENT_REJECTS_ASSIGNED_REQ = 0.2
# TODO: HERE THIS HELP!!!
# CHANCE_AGENT_ACCEPTS_RANDOM_REQ = 0.1
# CHANCE_AGENT_REJECTS_RANDOM_REQ = 0.05
# CHANCE_AGENT_IGNORES_RANDOM_REQ = 0.1


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
	# How many requests will be made today, calculate using poison distribution
	n_new_requests = int(stats.poisson.ppf(random.random(), mu=REQUESTS_LAMBDA))
	for _ in range(n_new_requests):
		# pick variants for Request and Estate respectively
		variant_request = list(entities_conf["Request"].get("variants", {}).keys())
		variant_request = random.choice(variant_request) if variant_request else None  # todo: weights
		variant_estate = "House" if "House" in variant_request else "Flat"
		
		# Requests can be made by new users or reoccurring users
		if random.random() <= CHANCE_FROM_NEW_USER:
			# Simple generation of new instance
			user = add_instance_to_population(df_users, entities_conf["User"], variant="User")
		else:
			# Picking new random existing User (not an Agent)
			n_users = len(df_users[df_users["isStaff"] == False])
			if n_users <= 0:
				continue
			user_i = random.randint(0, n_users - 1)
			user = df_users[df_users["isStaff"] == False].iloc[user_i].to_dict()
		
		# Pick variant and generate city
		# todo: not duplicating City Districts
		variant_city = random.choice(list(entities_conf["City"].get("variants", {}).keys()))
		new_city = add_instance_to_population(df_city, entities_conf["City"], variant=variant_city)
		
		# Generate new address in the city, for the estate, request
		new_address = add_instance_to_population(
			df_address,
			entities_conf["Address"],
			ref_entities={"City": new_city}
		)
		# Generate new Estate, from User, under the address for teh request
		new_estate = add_instance_to_population(
			df_estates,
			entities_conf["Estate"],
			variant=variant_estate,
			ref_entities={"User": user, "Address": new_address}
		)
		# Generate new Request, from User, on the Estate
		new_req = add_instance_to_population(
			df_requests,
			entities_conf["Request"],
			variant=variant_request,
			ref_entities={"User": user, "Estate": new_estate},
		)
		# Note: Not the best way to do it, but it works
		# Take the last record in DF and set its date to today's simulation day
		df_requests.loc[len(df_requests) - 1, "CreatedAt"] = today_date.strftime("%d-%m-%Y")
		
		# Read newly created Request, if picked that agent was created, generate corresponding M2M record
		if new_req['isAgentAssigned']:
			# Picking random Agent for assigning the estate
			agent_i = random.randint(0, len(df_agents) - 1)
			agent = df_agents.iloc[agent_i].to_dict()
			add_instance_to_population(
				df_req_agent,
				entities_conf["RequestAgent"],
				ref_entities={"Agent": agent, "Request": new_req}
			)
		
		# At the end of creating the Request User has an option to fill out the Form
		if random.random() <= CHANCE_TO_FILL_THE_FORM:
			# Note: Not realistic but good enough
			# Pick whether user created an account or not, important for data references
			variant_form = list(entities_conf["Form"].get("variants", {}).keys())
			variant_form = random.choices(variant_form, weights=CHANCE_FORM_VARIANTS, k=1)[0] if variant_form else None
			add_instance_to_population(
				df_form,
				entities_conf["Form"],
				variant=variant_form,
				ref_entities={"User": user},
			)
	
	for index, row in df_req_agent[df_req_agent["Status"] == "Pending"].iterrows():
		if random.random() <= CHANCE_AGENT_ACCEPTS_ASSIGNED_REQ:
			df_req_agent.loc[index, "Status"] = "Accepted"
		elif random.random() <= CHANCE_AGENT_REJECTS_ASSIGNED_REQ:
			df_req_agent.loc[index, "Status"] = "Rejected"


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
