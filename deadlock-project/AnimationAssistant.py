#
# Deadlock-Detection Resource Manager
# Monica Klosin
# 11/12/2020
#
import time
import re
import numpy
import networkx as nx


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
    stepsInProgram = []  # hold direction, P -> R or R -> P, in program

    #deadlock
    V = []  # amount of each resource currently avaialble
    edges = []  # edges holding which resource is pointing to what
    steps = []  # hold direction, P -> R or R -> P, in program
    verbalrequests = []  # requests, holds
    deadlock = 0  # holds #cycles detected
    deadlockSteps = []  # holds if a cycle is detect

    # read in raw data into array
    f = open("scenario-2.txt", "r")  # get file
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
    #output P and owned RIDs
    for i in range(numProcesses):
        processHolder.append(["P" + str(i)])

    #-------------
    # RESOURCES
    #-------------
    # Get num of resources
    numResources = int(input_array.pop(0).split(' ')[0])


    #Bool if resource value is held by a P
    resourceHeld = [False] * numResources

    #Array of PIDS requesting a currenlty owned R
    for i in range(numResources):
        resourceWanted.append([str(i)])
        V.append([1])

    #-------------
    # Deadlock *prediction* set up
    #-------------

    claimMatrix = numpy.zeros((numProcesses, numResources))
    allocationMatrix = numpy.zeros((numProcesses, numResources))
    for i in range(len(input_array)):
        currentStep = input_array[i].split(" ")
        requestType = currentStep[0]  # "r" or "f"
        currentProcess = int(currentStep[1])  # PID
        currentResource = int(currentStep[2])  # RID

        if (requestType == "r"):
            claimMatrix[currentProcess][currentResource] = 1
        allocationMatrix[currentProcess][currentResource] = 0  # R -> P

    #-------------
    # Going Step by Step through input
    #-------------
    for i in range(len(input_array)):
       
        #dramatic effect
        time.sleep(1)

        currentStep = input_array[i].split(" ")
        requestType = currentStep[0]  # "r" or "f"
        currentProcess = currentStep[1]  # PID
        currentResource = currentStep[2]  # RID

        #if process is requesting
        if (requestType == "r"):

            #check if RID is Held
            if (resourceHeld[int(currentResource)] == False):
                #Since RID is free, PID owns it
                allocationMatrix[int(currentStep[1])][int(currentStep[2])] = 1
                verbalrequests.append("owns")
                #RID is now held
                resourceHeld[int(currentResource)] = True
                #add RID to PID's array
                processHolder[int(currentProcess)].append(
                    "R" + str(currentResource))
               
                # R -> P
                edges.append((f"R{currentResource}", f"P{currentProcess}"))
                steps.append((f"R{currentResource}", f"P{currentProcess}"))
            else:
                #Since RID is held by another process,
                

                # Put PID in resourceWanted array to request access to RID
                resourceWanted[int(currentResource)].append(str(currentProcess))
                #P -> R
                verbalrequests.append("requests")
                edges.append((f"P{currentProcess}", f"R{currentResource}"))
                steps.append((f"P{currentProcess}", f"R{currentResource}"))

        #If process is freeing
        if (requestType == "f"):
            #P -x-> R
            #edges.remove("P" + currentProcess + ", R" + currentResource)
            verbalrequests.append("frees")
            edges.remove((f"R{currentResource}", f"P{currentProcess}"))
            steps.append((f"R{currentResource}", f"P{currentProcess}"))
            #RID is no longer held
            resourceHeld[int(currentResource)] = False
            #remove RID from PID's array
            processHolder[int(currentProcess)].remove(
                "R" + str(currentResource))

            #check if RID is wanted by another PID
            if(len(resourceWanted[int(currentResource)]) > 1):
                #first value in this 2D array is the RID, which is why x = [RID][1]
                # x = holds the PID requesting access to RID
                x = resourceWanted[int(currentResource)][1]
                #Add RID to PID array
                processHolder[int(x)].append("R" + str(currentResource))
                verbalrequests.append("now owns")
                edges.remove((f"P{x}", f"R{currentResource}"))
                edges.append((f"R{currentResource}", f"P{x}"))
                steps.append((f"R{currentResource}", f"P{x}"))
               
                #Remove PID from resourceWanted array
                resourceWanted[int(currentResource)].remove(str(x))
                #RID is now held
                resourceHeld[int(currentResource)] = True


        #-------------
        # Detecting Cycles for a directed graph
        #-------------

        G = nx.DiGraph(edges)
        deadlock = (len(list(nx.simple_cycles(G))))
        deadlockSteps.append(deadlock)
        #if (int(deadlock) > 0):

            #print("There is deadlock!")
            #print(list(nx.simple_cycles(G)))
        
        #-------------
        # Predict Deadlock using Banker’s algorithm
        #-------------

        #V: vector of amount of resources available for each R
        for i in range(numResources):
            if resourceHeld[i] == True:
                V[i] = 0
            else:
                V[i] = 1

      
