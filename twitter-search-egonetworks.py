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
graph = nx.DiGraph()
locations = {}
errors = 0

# Your Twitter App details
# Get them from http://dev.twitter.com
OAUTH_TOKEN = ""
OAUTH_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""


##########################################################################
#
# load_connections: load connections (followers, following) in one list of Twitter accounts
#

def load_connections(user_list, option):

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
                    query = twitter.followers.ids(
                        user_id=p, count=5000, cursor=cursor)
                else:
                    query = twitter.friends.ids(
                        user_id=p, count=5000, cursor=cursor)
                cursor = query["next_cursor_str"]
                for idtocheck1 in query["ids"]:
                    connections[p].append(idtocheck1)

            except Exception, e:
                if "Rate limit exceeded" in str(e):
                    print "Rate exceeded... waiting 15 minutes before retrying"
                    notworking = False
                    # Countdown http://stackoverflow.com/questions/3249524/print-in-one-line-dynamically-python
                    for k in range(1, 60 * 15):
                        remaining = 60 * 15 - k
                        sys.stdout.write(
                            "\r%d seconds remaining   " % remaining)
                        sys.stdout.flush()
                        sleep(1)
                    sys.stdout.write("\n")

                    if option == "followers":
                        try:
                            query = twitter.followers.ids(
                            user_id=p, count=5000, cursor=cursor)
                        except:
                            cursor = "0"
                            errors += 1
                            notworking = True
                    else:
                        try:
                            query = twitter.friends.ids(
                            user_id=p, count=5000, cursor=cursor)
                        except:
                            cursor = "0"
                            errors += 1
                            notworking = True

                    if notworking is False:
                        cursor = query["next_cursor_str"]
                        for idtocheck2 in query["ids"]:
                            connections[p].append(idtocheck2)

                elif "Not authorized" in str(e):
                    print "There were some errors with user", i, "... most likely it is a protected user"
                    cursor = "0"
                    errors += 1

                else:
                    print "Some error happened with user", i
                    cursor = "0"
                    errors += 1

    return connections

##########################################################################
#
# Main
#

if __name__ == "__main__":

    # Clear the screen
    #os.system('cls' if os.name == 'nt' else 'clear')

    print ""
    print "....................................................."
    print "Connections among members in users searched on Twitter by keywords"
    print ""
    # username = raw_input("From which Twitter user would you like to analyse the lists? ")

    # Log in
    twitter = Twitter(
        auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

    keywords = [""]
    search_results = []
    members = []
    members_usernames = []
    members_data = {}
    for word in keywords:
        print(word)
        for i in range(1500/20):
            try:
                search = twitter.users.search(q=word,page=i)
                search_results.append(search)
            except:
                pass
    for result in search_results:
        for user in result:
            members_data[user["id"]] = user
            members.append(user["id"])
            members_usernames.append(user["screen_name"])

    # Remove duplicates
    members = list(dict.fromkeys(members))

    print ""
    print "Checking the connections among the users..."

    # Load connections of each member
    for k,l in enumerate(members):
        print ""
        print k+1,"/", len(members)
        print "USER:", members_data[l]["screen_name"]
        print "Loading connections..."
        followers = load_connections([l], "followers")
        friends = load_connections([l], "friends")

        # Add edges...
        print "Building the graph..."

        for f in followers:
            for k in followers[f]:
                graph.add_edge(k, f)

        for o in friends:
            for p in friends[o]:
                graph.add_edge(o, p)

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


    # Save the full graph, all members of the chosen lists and all their
    # connections
    print ""
    print "The personal profile was analyzed successfully.", errors, "errors were encountered.", len(graph), "nodes in the network."
    print ""
    print "Saving the file as twitter-lists-ego-networks-full.gexf..."
    nx.write_gexf(
        graph, "twitter-lists-ego-networks-full.gexf")

    # Clean from nodes who are not members, in order to get a 1.5 level network
    for v in graph.nodes(data=True):
        if v[0] not in members:
            graph.remove_node(v[0])
        else:
            for j in members_data[v[0]]:
                try:
                    if members_data[v[0]][j] == None:
                        graph.node[v[0]][j] = "None"
                    else:
                        graph.node[v[0]][j] = members_data[v[0]][j]
                except:
                    pass

    # Save the graph, only members of the chosen lists and the connections
    # among them
    print ""
    print "Saving the file as twitter-lists-ego-networks-search.gexf..."
    nx.write_gexf(graph, "twitter-list-ego-networks-search.gexf")
