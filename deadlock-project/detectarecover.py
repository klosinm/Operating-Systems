#
# Deadlock-Detection Resource Manager
# Extra Credit
# Monica Klosin
# 11/23/2020
#
# Detect and Recover from Deadlock
# Extra Credit
#
import time
import re
import numpy
import networkx as nx
from os import path


class DetectAndRecover:

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
    T = [] #array to hold nodes in deadlock
    V = []  # amount of each resource currently avaialble
    edges = []  # edges holding which resource is pointing to what
    steps = []  # hold direction, P -> R or R -> P, in program
    verbalrequests = []  # requests, holds
    deadlock = 0  # holds #cycles detected
    deadlockSteps = []  # holds if a cycle is detect

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
    print(str(numProcesses) + " processes.")

    #Initialize num of process arrays
    #output P and owned RIDs
    for i in range(numProcesses):
        processHolder.append(["P" + str(i)])

    #-------------
    # RESOURCES
    #-------------
    # Get num of resources
    numResources = int(input_array.pop(0).split(' ')[0])
    print(str(numResources) + " resources. ")

    #Bool if resource value is held by a P
    resourceHeld = [False] * numResources

    #Array of PIDS requesting a currenlty owned R
    for i in range(numResources):
        resourceWanted.append([str(i)])
        V.append([1])

    #-------------
    # Deadlock detect and recover set up
    #-------------
    pointName = [] #Holds whole name of node pointing
    pointType = [] #Holds type of noding pointing, ie P or R
    pointValue = [] #Holds value of node pointing, ie 0 or 1

    point2Name = [] #Holds whole name of node being pointed to
    point2Type = []  #Holds type of node being pointed to, ie P or R
    point2Value = []  #Holds value of node being pointed to, ie 0 or 1


    #-------------
    # Going Step by Step through input
    #-------------
    Running = True #Help exit out of loop if deadlock occurs
    blep = 0  #Honorary helper to get ouf of while loop, blep
    meep = 0  #Honorary helper to get out of while loop, meep!
    while Running:
        for i in range(len(input_array)):

            print("__________________________\n")

            #blep counts if cycle has been repeated
            if ((i) == 0):
                blep += 1
                
            #for deadlock
            if (i == 0 and meep == 1):
                Running = False
            #For normal simulation
            elif ((i + 1) == len(input_array)):
                Running = False
         
            #dramatic effect
            time.sleep(1)

        
            #Tell step in program so far
            if(blep != 2):
                print("Step " + str(i + 1) + "/" + str(len(input_array)))
            else:
                print("Step " + str(len(input_array)) + "/" + str(len(input_array)))
            
     
            currentStep = input_array[i].split(" ")
            requestType = currentStep[0]  # "r" or "f"
            currentProcess = currentStep[1]  # PID
            currentResource = currentStep[2]  # RID

            #if process is requesting
            if (requestType == "r"):

                #check if RID is Held
                if (resourceHeld[int(currentResource)] == False):
                    #Since RID is free, PID owns it
                    print("R" + currentResource + " owned by P" + currentProcess)
                    verbalrequests.append("owned")
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
                    print("P" + currentProcess + " requests R" + currentResource)
                    verbalrequests.append("requests")
                    # Put PID in resourceWanted array to request access to RID
                    resourceWanted[int(currentResource)].append(
                        str(currentProcess))
                    #P -> R
                    edges.append((f"P{currentProcess}", f"R{currentResource}"))
                    steps.append((f"R{currentResource}", f"P{currentProcess}"))

            #If process is freeing
            if (requestType == "f"):
                #P -x-> R
                print("P" + currentProcess + " frees R" + currentResource)
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
                    print("R" + currentResource + " now owned by P" + x)
                    verbalrequests.append("now owns")
                    edges.remove((f"P{x}", f"R{currentResource}"))
                    edges.append((f"R{currentResource}", f"P{x}"))
                    steps.append((f"R{currentResource}", f"P{x}"))

                    #Remove PID from resourceWanted array
                    resourceWanted[int(currentResource)].remove(str(x))
                    #RID is now held
                    resourceHeld[int(currentResource)] = True

            #-------------
            # current status of program
            #-------------
            
            for i in range(numProcesses):
                # PID's and held RID's
                print(processHolder[i])

            print("_ _ _ _ _\n")

            for i in range(numResources):
                #boolean if R is held or not
                print("R" + str(i) + " held: " + str(resourceHeld[i]))
                #list of PID's requesting RID
                print(str(resourceWanted[i][1:]))


            #-------------
            # Detecting Cycles for a directed graph
            #-------------

            G = nx.DiGraph(edges)
            deadlock = (len(list(nx.simple_cycles(G))))
            deadlockSteps.append(deadlock)

            #Detect and Recover
            if (int(deadlock) > 0):
                meep += 1

                print("_ _ _ _ _ _\n")
                print("There is deadlock!")
                print(list(nx.simple_cycles(G)))
                print("_ _ _ _ _ _\n")

                T = list(nx.simple_cycles(G))

                #dramatic effect
                time.sleep(1)

                #Loop through edges created and see which latest
                #edge is in the cycle
                for i in range(len(edges)):
                    find = False #used to exit out of double for loop
                    for j in range(len(T[0])):

                        if (edges[i][0] == T[0][j]):
                            #Node pointing
                            pointName = edges[i][0]  
                            pointType = edges[i][0][0]  
                            pointValue = edges[i][0][1]  
                            #Node being pointed too
                            point2Name = edges[i][1]  
                            point2Type = edges[i][1][0]  
                            point2Value = edges[i][1][1]
                            
                            #remove edge from Graph cycle
                            print("Kill request \"" + pointName + " " +
                                verbalrequests[i] + " " + point2Name + "\"")
                            G.remove_edge(pointName, point2Name)
                            verbalrequests.append("frees")

                            #If the node pointing is a resourse,
                            #this means this resource is held, so we unhold it since
                            #we killed this step
                            if (pointType == "R"):
                                resourceHeld[int(pointValue)] = False
                                processHolder[int(point2Value)].remove( str(edges[i][0]))

                        
                                #Check if any  other Process wanted this Resource
                                if (len(resourceWanted[int(pointValue)]) > 1):
                                    x = resourceWanted[int(pointValue)][1]
                                    processHolder[int(x)].append("R" + str(pointValue))
                                    print("P" + x + " now owns " + pointName)

                                    #R -> P(new)
                                    verbalrequests.append("now owns")
                                    edges.remove((f"P{x}", f"R{pointValue}"))
                                    edges.append((f"R{pointValue}", f"P{x}"))
                                    steps.append((f"R{pointValue}", f"P{x}"))

                                    #Remove PID from resourceWanted array
                                    resourceWanted[int(pointValue)].remove(str(x))
                                    #RID is now held
                                    resourceHeld[int(pointValue)] = True

                            #remove this edge from arrays
                            edges.remove(edges[i])
                            steps.append(edges[i])

                            #append killed request to end of program
                            if (pointType == "P"):
                                #input_array.remove( "r " + pointName + " " + point2Name)
                                input_array.append(("r " + pointName + " " + point2Name))
                                print("Added " + pointName + " requests " + point2Name + " to end of program.") 
                            elif (pointType == "R"):
                                #input_array.remove( "r " + point2Value + " " + pointValue)
                                input_array.append( "r " + point2Value + " " + pointValue)
                                print("Added " + point2Name + " requests " + pointName + " to end of program.") 

                    
                            print("_ _ _ _ _ _\n")

                            find = True     
                            break

                    if find:
                        break
            
            #For deadlock
            if(blep == 2):
                break
              