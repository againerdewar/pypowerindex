

#!/usr/bin/python -i
from __future__ import division
import random
import numpy
import matplotlib.pyplot as pyplot

# Set up environment
pop_key = "Population"
vote_key = "Votes"

# Put player data in a dict
# In this case, we use data from the 2010 US Census apportionment of electoral votes
players = {
    "Alabama": {pop_key: 4802982, vote_key: 9},
    "Alaska": {pop_key: 721523, vote_key: 3},
    "Arizona": {pop_key: 6412700, vote_key: 11},
    "Arkansas": {pop_key: 2926229, vote_key: 6},
    "California": {pop_key: 37341989, vote_key: 55},
    "Colorado": {pop_key: 5044930, vote_key: 9},
    "Connecticut": {pop_key: 3581628, vote_key: 7},
    "Delaware": {pop_key: 900877, vote_key: 3},
    "District of Columbia": {pop_key: 601723, vote_key: 3},
    "Florida": {pop_key: 18900773, vote_key: 29},
    "Georgia": {pop_key: 9727566, vote_key: 16},
    "Hawaii": {pop_key: 1366862, vote_key: 4},
    "Idaho": {pop_key: 1573499, vote_key: 4},
    "Illinois": {pop_key: 12864380, vote_key: 20},
    "Indiana": {pop_key: 6501582, vote_key: 11},
    "Iowa": {pop_key: 3053787, vote_key: 6},
    "Kansas": {pop_key: 2863813, vote_key: 6},
    "Kentucky": {pop_key: 4350606, vote_key: 8},
    "Louisiana": {pop_key: 4553962, vote_key: 8},
    "Maine": {pop_key: 1333074, vote_key: 4},
    "Maryland": {pop_key: 5789929, vote_key: 10},
    "Massachusetts": {pop_key: 6559644, vote_key: 11},
    "Michigan": {pop_key: 9911626, vote_key: 16},
    "Minnesota": {pop_key: 5314879, vote_key: 10},
    "Mississippi": {pop_key: 2978240, vote_key: 6},
    "Missouri": {pop_key: 6011478, vote_key: 10},
    "Montana": {pop_key: 994416, vote_key: 3},
    "Nebraska": {pop_key: 1831825, vote_key: 5},
    "Nevada": {pop_key: 2709432, vote_key: 6},
    "New Hampshire": {pop_key: 1321445, vote_key: 4},
    "New Jersey": {pop_key: 8807501, vote_key: 14},
    "New Mexico": {pop_key: 2067273, vote_key: 5},
    "New York": {pop_key: 19421055, vote_key: 29},
    "North Carolina": {pop_key: 9565781, vote_key: 15},
    "North Dakota": {pop_key: 675905, vote_key: 3},
    "Ohio": {pop_key: 11568495, vote_key: 18},
    "Oklahoma": {pop_key: 3764882, vote_key: 7},
    "Oregon": {pop_key: 3848606, vote_key: 7},
    "Pennsylvania": {pop_key: 12734905, vote_key: 20},
    "Rhode Island": {pop_key: 1055247, vote_key: 4},
    "South Carolina": {pop_key: 4645975, vote_key: 9},
    "South Dakota": {pop_key: 819761, vote_key: 3},
    "Tennessee": {pop_key: 6375431, vote_key: 11},
    "Texas": {pop_key: 25268418, vote_key: 38},
    "Utah": {pop_key: 2770765, vote_key: 6},
    "Vermont": {pop_key: 630337, vote_key: 3},
    "Virginia": {pop_key: 8037736, vote_key: 13},
    "Washington": {pop_key: 6753369, vote_key: 12},
    "West Virginia": {pop_key: 1859815, vote_key: 5},
    "Wisconsin": {pop_key: 5698230, vote_key: 10},
    "Wyoming": {pop_key: 568300, vote_key: 3},
}

# Set some parameters
numtrials = 999
quota = 270
numplayers = len(players)
total_population = sum(players[player][pop_key] for player in players)
total_votes = sum(players[player][vote_key] for player in players)

# Set up a dict to store results
player_pivot_counts = {player: 0 for player in players}

player_list = sorted(players)

# Find the pivot player in a specified ordering
def find_pivot (players_ordered):
    votes_ordered = [players[player][vote_key] for player in players_ordered]
    winners = (i for i in xrange(numplayers) if sum(votes_ordered[:i+1]) >= quota)
    return players_ordered[min(winners)]

# Perform the trials
for i in xrange(numtrials):
    random.shuffle(player_list)
    player_pivot_counts[find_pivot(player_list)] += 1

# Set up lists storing various values
player_list = sorted(players)

pivot_count_list = [player_pivot_counts[player] for player in player_list]
pivot_percent_list = [count / numtrials * 100 for count in pivot_count_list]

pop_percent_list = [players[player][pop_key] / total_population * 100 for player in player_list]

pivot_ratio = lambda player: (player_pivot_counts[player] / numtrials) / (players[player][pop_key] / total_population)
vote_ratio = lambda player: (players[player][vote_key] / total_votes) / (players[player][pop_key] / total_population)
pivots_and_votes_per_pop = [( vote_ratio(player), pivot_ratio(player), player) for player in player_list]
pivots_and_votes_per_pop.sort()

vpp, ppp, players_by_ppp = zip(*pivots_and_votes_per_pop)

# Set up chart showing power and population
bar_width = 0.35
index = numpy.arange(numplayers)

index_figure = pyplot.figure(1)

pyplot.bar(index,
           pivot_percent_list,
           bar_width,
           color='b',
           label='SSI')

pyplot.bar(index+bar_width,
           pop_percent_list,
           bar_width,
           color='r',
           label='Population')

pyplot.xticks(index + bar_width,
              player_list,
              rotation=90)
pyplot.legend()
pyplot.tight_layout()

# Set up chart showing power-to-population ratio
ratio_figure = pyplot.figure(2)

pyplot.bar(index,
           ppp,
           bar_width,
           color='b',
           label='SSI per population')

pyplot.bar(index + bar_width,
           vpp,
           bar_width,
           color='r',
           label='Votes per population')

pyplot.xticks(index + bar_width,
              players_by_ppp,
              rotation=90)

pyplot.legend()
pyplot.tight_layout()

# Display plots
pyplot.show()
