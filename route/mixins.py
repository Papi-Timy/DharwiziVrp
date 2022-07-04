from django.conf import settings
import requests
import json
import datetime
from humanfriendly import format_timespan
import math
import time
import random
from decimal import Decimal
import googlemaps
import collections



def tabuSearch(items, maxDuration, maxSteps, neighboursPerSteps, numVehicles):
        tabu_list = [i for i in range(len(items))]  # indexes of locations available to select randomly

        # Random number generator
        def get_random_neighbour_index(n):
            index = random.randint(0, n - 1)
            return index

        # Get new neighbours from list of locations not used yet
        def randomize_new_neighbours(neighboursPerSteps):
            ans = []
            n = neighboursPerSteps
            if len(tabu_list) < neighboursPerSteps: n = len(tabu_list)
            for i in range(n):
                ans.append(tabu_list[get_random_neighbour_index(n)])
            return ans

        # User defined metric to evaluate neighbour
        def cost_function(current_loc, next_loc):
            try:
                distance_increment = items[current_loc][next_loc][0]
                duration_increment = items[current_loc][next_loc][1]
                return (distance_increment / duration_increment), next_loc
            except:
                return 0, next_loc

        # Evaluate best neighbour from random choices
        def calculate_cost_functions(current_loc, new_neighbours):
            ans = []
            for i in range(len(new_neighbours)):
                ans.append(cost_function(current_loc, new_neighbours[i]))

            return ans

        def get_best_neighbour(current_loc):

            random_neighbour_values = calculate_cost_functions(current_loc,
                                                               randomize_new_neighbours(neighboursPerSteps))

            # get index of best neighbour from random choices made
            if len(random_neighbour_values) != 0:
                best_neighbour_index = random_neighbour_values.index(max(random_neighbour_values))
                # returns global location index of best neighbour
                return random_neighbour_values[best_neighbour_index][1]

        def get_best_neighbours(current_loc):
            ans = []
            for i in range(maxSteps):
                ans.append(get_best_neighbour(current_loc))
            return ans

        def mode_filter(neighbour_indexes):
            data = collections.Counter(neighbour_indexes)
            return data.most_common(1)[0][0]  # returns item'[0]' with frequency of occurence'[1]'

        # Initial setup
        n = 0

        route = [[] for i in range(numVehicles)]
        route_distance = [0] * numVehicles
        route_duration = [0] * numVehicles
        current_loc_index = [0] * numVehicles
        return_distance = [0] * numVehicles
        return_duration = [0] * numVehicles
        previous_return_distance = [0] * numVehicles
        previous_return_duration = [0] * numVehicles

        tabu_list.remove(current_loc_index[0])
        for v in range(numVehicles):
            route[v].append(current_loc_index[v])

        for i in range(len(tabu_list)):
            for v in range(numVehicles):
                best_neighbour_index = mode_filter(get_best_neighbours(current_loc_index[v]))
                best_neighbour_distance = items[current_loc_index[v]][best_neighbour_index][0]
                best_neighbour_duration = items[current_loc_index[v]][best_neighbour_index][1]

                return_distance[v] = items[0][best_neighbour_index][0]
                return_duration[v] = items[0][best_neighbour_index][1]
                m = best_neighbour_duration + return_duration[v] - previous_return_duration[v]

                if (route_duration[v] + m) < maxDuration:
                    route_distance[v] += (best_neighbour_distance + return_distance[v] - previous_return_distance[v])
                    route_duration[v] += (best_neighbour_duration + return_duration[v] - previous_return_duration[v])

                    previous_return_distance[v] = return_distance[v]
                    previous_return_duration[v] = return_duration[v]

                    current_loc_index[v] = best_neighbour_index
                    route[v].append(current_loc_index[v])
                    tabu_list.remove(current_loc_index[v])  # remove location from tabulist
                    n += 1

        for v in range(numVehicles):
            route[v].append(0)
        return route, route_distance, route_duration


def Directions(*args, **kwargs):

	lat_a = kwargs.get("lat_a")
	long_a = kwargs.get("long_a")
	lat_b = kwargs.get("lat_b")
	long_b = kwargs.get("long_b")
	lat_c = kwargs.get("lat_c")
	long_c = kwargs.get("long_c")
	lat_d = kwargs.get("lat_d")
	long_d = kwargs.get("long_d")

	origin = f'{lat_a},{long_a}'
	destination = f'{lat_b},{long_b}'
	waypoints = f'{lat_c},{long_c}|{lat_d},{long_d}'

	result = requests.get(
		'https://maps.googleapis.com/maps/api/directions/json?',
		 params={
		 'origin': origin,
		 'destination': destination,
		 'waypoints': waypoints,
		 "key": "Key"
		 })

	directions = result.json()

	if directions["status"] == "OK":

		routes = directions["routes"][0]["legs"]


		distance = 0
		duration = 0
		route_list = []

		for route in range(len(routes)):

			distance += int(routes[route]["distance"]["value"])
			duration += int(routes[route]["duration"]["value"])

			route_step = {
				'origin': routes[route]["start_address"],
				'destination': routes[route]["end_address"],
				'distance': routes[route]["distance"]["text"],
				'duration': routes[route]["duration"]["text"],

				'steps': [
					[
						s["distance"]["text"],
						s["duration"]["text"],
						s["html_instructions"],

					]
					for s in routes[route]["steps"]]
				}

			
			route_list.append(route_step)
			

	return {
		"origin": origin,
		"destination": destination,
		"distance": f"{round(distance/1000, 2)} Km",
		"duration": format_timespan(duration),
		"route": route_list
		}