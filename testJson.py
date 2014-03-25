
import sys
import json
from pprint import pprint

args = sys.argv

# We will take many samples in an attempt to reduce number of keys to farm
# This is the number of samples to take since the last improvement
EXTRA_SAMPLES = 20

if len(args) < 3:
    print '''
    -----Introduction-----

    This is for Ingress. If you don't know what that is, you're lost.

    -----Usage-----

    >> python makePlan.py agent_count input_file [output_directory] [output_file]
    
    agent_count: Number of agents for which to make a plan
    
    input_file:  One of two types of files:
                   .csv formatted as portal name,latE6,lngE6,keys
                        
                        portal name should not contain commas
                        latE6 and lngE6 should be the portal's global coordinates
                        E6 means times 10^6 (no decimal)
                            e.g. the Big Ben portal is at 51500775,-124466
                        keys is the number of keys you have for the portal
                   
                   .pkl an output from a previous run of this program
                        this can be used to make the same plan with a different number of agents

    output_directory: directory in which to put all output
                      default is the working directory

    output_file: name for a .pkl file containing information on the plan
                 if you use this for the input file, the same plan will be produced with the number of agents you specify
                 default: "lastPlan.pkl"
    '''
    exit()

import networkx as nx
from lib import maxfield,PlanPrinter,geometry,agentOrder,iitcBookmarks as bookmarks
np = geometry.np
import pickle

#GREEN = 'g'
#BLUE  = 'b'
GREEN = '#3BF256' # Actual faction text colors in the app
BLUE  = '#2ABBFF'
#GREEN = (0.0 , 1.0 , 0.0 , 0.3)
#BLUE  = (0.0 , 0.0 , 1.0 , 0.3)
COLOR = BLUE

if args[1] == '-g':
    COLOR = GREEN
    print COLOR
    args = [args[0]] + args[2:]

if len(args) < 4:
    output_directory = ''
else:
    output_directory = args[3]
    if output_directory[-1] != '/':
        output_directory += '/'

if len(args) < 5:
    output_file = 'lastPlan.pkl'
else:
    output_file = args[4]

    if not output_file[-3:] == 'pkl':
        print 'WARNING: output file should end in "pkl" or you cannot use it as input later'

nagents = int(args[1])
if nagents < 0:
    print 'Number of agents should be positive'
    exit()

input_file = args[2]

if input_file[-3:] != 'pkl':
    a = nx.DiGraph()

    locs = []

    i = 0
    with open(input_file) as data_file:    
        data = json.load(data_file)
    print(bookmarks.loadBookmarks(data, "NISC"))
