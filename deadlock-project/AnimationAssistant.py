#
# Deadlock-Detection Resource Manager
# Monica Klosin
# 11/12/2020
#
# AnimationAssistant class gives the animation information to DeadlockAnimation.py
#
import time
import numpy
import networkx as nx
from os import path


class Detection:

    my_file = []  # read in raw data
    initial_input_array = []  # read in raw data 2
    input_array = []  # array to hold data from file
    i = 0  # guest star integer
    x = 0  # guest star integer

    processHolder = []  # holds the process w/their held resources
    resourceWanted = []  # Holds resources and PID that request use

    currentStep = []  # hold value of request type, PID, and RID
    requestType = []  # holds request type; "r" or "f"
    currentProcess = []  # hold value of current process
    currentResource = []  # hold value of current resource

    #deadlock
    edges = []  # edges holding which resource is pointing to what
    steps = []  # hold *every* step, P -> R or R -> P or P -X-> R, in program
    # hold *every* verbalstep, requests or owns or frees (now owns), in program
    verbalrequests = []
    deadlock = 0  # holds number of cycles detected
    deadlockSteps = []  # holds array of number of cycles at each step in program

    #-------------
    # PREP INPUT OF FILE
    #-------------
    #check that user input for file exists
    print("Please enter val of text file for simulation:")
    userinput = input()
    simFile = f"scenario-{userinput}.txt"
    if (path.exists(simFile) and userinput.isdigit() == True):
        print("Enjoy the animation! Loading...")
    else:
        print("Oh no! Something went wrong. Please try with different credentials.")
        quit()

    # get file
    f = open(f"scenario-{userinput}.txt", "r")

    # read in raw data into array
    with f as my_file:
        initial_input_array = my_file.readlines()

    # remove '\n' from array
    for x in initial_input_array:
        input_array.append(x.strip())

    #-------------
    # PROCESSES
    #-------------
    # Get num of processes
    numProcesses = int(input_array.pop(0).split(' ')[0])

    #Initialize num of process arrays
    #array will hold P and owned RIDs
    for i in range(numProcesses):
        processHolder.append(["P" + str(i)])

    #-------------
    # RESOURCES
    #-------------
    # Get num of resources
    numResources = int(input_array.pop(0).split(' ')[0])

    #Bool if resource is held by a P
    resourceHeld = [False] * numResources

    #Array of PIDS requesting a currenlty owned R
    for i in range(numResources):
        resourceWanted.append([str(i)])

    #-------------
    # Going Step by Step through program
    #-------------
    for i in range(len(input_array)):

        #dramatic effect
        time.sleep(1)

        currentStep = input_array[i].split(" ")  # get current step in program
        requestType = currentStep[0]  # "r" or "f"
        currentProcess = currentStep[1]  # PID
        currentResource = currentStep[2]  # RID

        #if process is requesting
        if (requestType == "r"):

            #check if RID is Held
            if (resourceHeld[int(currentResource)] == False):
                #Since RID is free, PID owns requested RID
                resourceHeld[int(currentResource)] = True
                #add RID to PID's array
                processHolder[int(currentProcess)].append(
                    "R" + str(currentResource))
                # R -> P
                verbalrequests.append("owns")
                edges.append((f"R{currentResource}", f"P{currentProcess}"))
                steps.append((f"R{currentResource}", f"P{currentProcess}"))

            else:
                #Since RID is held by another process,
                #Put PID in resourceWanted array to request access to RID
                resourceWanted[int(currentResource)].append(
                    str(currentProcess))
                #P -> R
                verbalrequests.append("requests")
                edges.append((f"P{currentProcess}", f"R{currentResource}"))
                steps.append((f"P{currentProcess}", f"R{currentResource}"))

        #If process is freeing
        if (requestType == "f"):
            #RID is no longer held
            resourceHeld[int(currentResource)] = False
            #remove RID from PID's array
            processHolder[int(currentProcess)].remove(
                "R" + str(currentResource))
            #P -x-> R
            verbalrequests.append("frees")
            edges.remove((f"R{currentResource}", f"P{currentProcess}"))
            steps.append((f"R{currentResource}", f"P{currentProcess}"))

            #check if RID is wanted by another PID
            if(len(resourceWanted[int(currentResource)]) > 1):
                #first value in this 2D array is the RID, which is why x = [RID][1]
                # x = holds the PID requesting access to RID
                x = resourceWanted[int(currentResource)][1]
                #Add RID to PID array
                processHolder[int(x)].append("R" + str(currentResource))
                #R -> P(new)
                verbalrequests.append("now owns")
                edges.remove((f"P{x}", f"R{currentResource}"))
                edges.append((f"R{currentResource}", f"P{x}"))
                steps.append((f"R{currentResource}", f"P{x}"))

                #Remove PID from resourceWanted array
                resourceWanted[int(currentResource)].remove(str(x))
                #RID is now held
                resourceHeld[int(currentResource)] = True

        #-------------
        # Detecting Cycles
        #-------------
        #Use a Dianamic graph to conenct edges formed so far in
        G = nx.DiGraph(edges)
        #if deadlock > 0, then there is a cycle in program
        deadlock = (len(list(nx.simple_cycles(G))))
        #array of number of loops detected each step in program
        deadlockSteps.append(deadlock)
