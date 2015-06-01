# -*- encoding: utf-8 -*-
#
# Social Network Analysis of Twitter lists members connections (Ego Networks)
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: GPL v.3
#
# Requisite:
# pip install twitter
# pip install networkx
#

# Import libraries
from twitter import *
import networkx as nx
from time import sleep
import sys
import os
import unicodedata

# Some global variables
graph=nx.DiGraph()
locations = {}
errors = 0
members = {}

# Your Twitter App details
# Get them from http://dev.twitter.com
OAUTH_TOKEN = "Insert here"
OAUTH_SECRET = "Insert here"
CONSUMER_KEY = "Insert here"
CONSUMER_SECRET = "Insert here"


##########################################################################################
#
# load_connections: load connections (followers, following) in one list of Twitter accounts
#

def load_connections(user_list,option):

	global errors
	connections = {}

	for p in user_list:
		query = {}
		counting = 0
		cursor = -1
		connections[p] = []

		while cursor != "0":

			# API: https://dev.twitter.com/docs/api/1.1/get/friends/ids
			try:
				if option == "followers":
					query = twitter.followers.ids(user_id=p,count=5000,cursor=cursor)
				else:
					query = twitter.friends.ids(user_id=p,count=5000,cursor=cursor)
				cursor = query["next_cursor_str"]
				for idtocheck1 in query["ids"]:
					connections[p].append(idtocheck1)
					# If you want to show the id of the user...
					# print " - ",id

			except Exception,e:
				if "Rate limit exceeded" in str(e):
					print "Rate exceeded... waiting 15 minutes before retrying"

					# Countdown http://stackoverflow.com/questions/3249524/print-in-one-line-dynamically-python
					for k in range(1,60*15):
						remaining = 60*15 - k
						sys.stdout.write("\r%d seconds remaining   " % remaining)
						sys.stdout.flush()
						sleep(1)
					sys.stdout.write("\n")

					if option == "followers":
						query = twitter.followers.ids(user_id=p,count=5000,cursor=cursor)
					else:
						query = twitter.friends.ids(user_id=p,count=5000,cursor=cursor)
					cursor = query["next_cursor_str"]
					for idtocheck2 in query["ids"]:
						connections[p].append(idtocheck2)
						# If you want to show the id of the user...
						# print " - ",id

				elif "Not authorized" in str(e):
					print "There were some errors with user",i,"... most likely it is a protected user"
					cursor = "0"
					errors += 1

				else:
					print "Some error happened with user",i
					cursor = "0"
					errors += 1

	return connections


##########################################################################################
#
# load_members: load members in one list of Twitter accounts
#

def load_members(choice):

	global members
	cursor = -1

	print ""
	print "Members of the list: ", choice
	print ""

	while cursor != 0:

		try:
			# API: https://dev.twitter.com/docs/api/1.1/get/lists/members
			query = twitter.lists.members(list_id=choice, cursor=cursor)
			cursor = query["next_cursor"]

		except Exception,e:
			if "Rate limit exceeded" in str(e):
				print "Rate exceeded... waiting 15 minutes before retrying"

				# Countdown http://stackoverflow.com/questions/3249524/print-in-one-line-dynamically-python
				for k in range(1,60*15):
					remaining = 60*15 - k
					sys.stdout.write("\r%d seconds remaining   " % remaining)
					sys.stdout.flush()
					sleep(1)
				sys.stdout.write("\n")

				query = twitter.lists.members(list_id=choice, cursor=cursor)
				cursor = query["next_cursor"]

		for i in query["users"]:
			print "-",i["screen_name"],"(id =",i["id"],")"
			members[i["id"]] = i["screen_name"]


##########################################################################################
#
# Main
#

if __name__ == "__main__":

	# Clear the screen
	os.system('cls' if os.name=='nt' else 'clear')

	print ""
	print "....................................................."
	print "Connections among members in Twitter lists"
	print ""
	username = raw_input("From which Twitter user would you like to analyse the lists? ")

	# Log in
	twitter = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

	# Load the lists of the user username
	# API: https://dev.twitter.com/docs/api/1.1/get/lists/list
	query = twitter.lists.list(screen_name=username)
	print ""
	print "These are the lists of",username
	print ""
	for i in query:
		print "-",i["name"],"list (id =",i["id"],") has",i["member_count"],"users."

	# Choose the lists
	print ""
	lists_number = input("How many lists would you like to analyse together? ")
	print ""
	choice = []
	for i in range(lists_number):
		message = "Enter id of list #"+str(i+1)+": "
		current_choice = raw_input(message)
		choice.append(current_choice)

	# Load the members of all the lists selected
	for j in range(lists_number):
		load_members(choice[j])

	print ""
	print "Checking the connections among the users..."

	# Load connections of each member
	for l in members:
		print ""
		print "USER:",members[l]
		print "Loading connections..."
		followers = load_connections([l], "followers")
		friends = load_connections([l], "friends")

		# Add edges...
		print "Building the graph..."

		for f in followers:
			for k in followers[f]:
				graph.add_edge(k,f)

		for o in friends:
			for p in friends[o]:
				graph.add_edge(o,p)

	# Prepare 100 ids lists for converting id to screen names
	mapping = {}
	lista = {}
	position = 0
	hundreds = 0
	lista[hundreds] = []
	for d in graph.nodes():
		if position == 100:
			hundreds += 1
			position = 0
			lista[hundreds] = []
		lista[hundreds].append(d)
		position += 1

	# Convert id to screen names
	print ""
	print "Converting ids to screen names..."
	for w in lista:
		try:
			# API: https://dev.twitter.com/docs/api/1.1/get/users/lookup
			query = twitter.users.lookup(user_id=lista[w])
		except Exception,e:
			if "Rate limit exceeded" in str(e):
				print "Rate exceeded... waiting 15 minutes before retrying"

				# Countdown http://stackoverflow.com/questions/3249524/print-in-one-line-dynamically-python
				for k in range(1,60*15):
					remaining = 60*15 - k
					sys.stdout.write("\r%d seconds remaining   " % remaining)
					sys.stdout.flush()
					sleep(1)
				sys.stdout.write("\n")

				query = twitter.users.lookup(user_id=lista[w])
		for h in query:
			mapping[h["id"]] = h["screen_name"]
			loc = h["location"]
			loc = unicodedata.normalize('NFKD', loc).encode('ascii','ignore')
			loc.decode('utf8')
			locations[h["screen_name"]] = loc

	# Swap node names from ids to screen names
	graph_screen_names = nx.relabel_nodes(graph,mapping)

	# Save the full graph, all members of the chosen lists and all their connections
	print ""
	print "The personal profile was analyzed successfully.",errors,"errors were encountered.",len(graph_screen_names),"nodes in the network."
	print ""
	print "Saving the file as "+username+"-twitter-lists-ego-networks-full.gexf..."
	nx.write_gexf(graph_screen_names, username+"-twitter-lists-ego-networks-full.gexf")

	# Clean from nodes who are not members, in order to get a 1.5 level network
	for v in graph_screen_names.nodes_iter(data=True):
		if v[0] not in members.values():
			graph_screen_names.remove_node(v[0])

	# Add locations
	for g in graph_screen_names.nodes():
		try:
			graph_screen_names.node[g]["location"] = locations[g]
		except Exception as e:
			print "Error adding a location: error",e,"for",g

	# Save the graph, only members of the chosen lists and the connections among them
	print ""
	print "Saving the file as "+username+"-twitter-lists-ego-networks-members.gexf..."
	nx.write_gexf(graph_screen_names, username+"-twitter-list-ego-networks-members.gexf")
