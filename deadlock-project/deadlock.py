#
# Deadlock-Detection Resource Manager
# Monica Klosin
# 11/12/2020
#
import time
import re
import numpy

class Detection(object):

    my_file = []  # read in raw data
    initial_input_array = []  # read in raw data 2
    input_array = []  # array to hold data from file
    i = 0  #guest star integer
    x = 0  #guest star integer
    
    
    processHolder = []  # holds the process w/their held resources
                        #allocation matrix
    resourceWanted = []  #Holds resources and PID that request use
                         #request matrix 
    
    currentStep = []  # hold value of request type, PID, and RID
    requestType = []  #holds request type; "r" or "f"
    currentProcess = []  #hold value of current process 
    currentResource = []  #hold value of current resource
    stepsInProgram = []  #hold direction, P -> R or R -> P, in program
    
    #deadlock
    resourceR = []  # amount of each resource available, will be a vector holding 1's
    V = []  # amount of each resource currently avaialble
    tally = 0  # tally if Process can be run
    
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
        resourceR.append(1)
        V.append([1])


    #-------------
    # Deadlock set up
    #-------------

    claimMatrix = numpy.zeros((numProcesses, numResources))
    allocationMatrix = numpy.zeros((numProcesses, numResources))

    for i in range(len(input_array)):
        currentStep = input_array[i].split(" ")
        requestType = currentStep[0] # "r" or "f"
        currentProcess = int(currentStep[1]) #PID
        currentResource = int(currentStep[2]) #RID

        if (requestType == "r"):
            claimMatrix[currentProcess][currentResource] = 1

        allocationMatrix[currentProcess][currentResource] = 0

    #-------------
    # Going Step by Step through input
    #-------------
    for i in range(len(input_array)):
        print("__________________________\n")
        #dramatic effect
        time.sleep(1)
        #Tell step in program so far
        print("Step " + str(i + 1) + "/" + str(len(input_array)))
        currentStep = input_array[i].split(" ")
        requestType = currentStep[0] # "r" or "f"
        currentProcess = currentStep[1] #PID
        currentResource = currentStep[2] #RID
        
        #if process is requesting
        if (requestType == "r"):
        
            #check if RID is Held
            if (resourceHeld[int(currentResource)] == False):
                #Since RID is free, PID owns it
                allocationMatrix[int(currentStep[1])][int(currentStep[2])] = 1

                print("R" + currentResource + " owned by P" + currentProcess)
                #RID is now held
                resourceHeld[int(currentResource)] = True
                #add RID to PID's array
                processHolder[int(currentProcess)].append("R" + str(currentResource))
                # R -> P
                stepsInProgram.append("R" + str(currentResource))
                stepsInProgram.append( "P" + str(currentProcess))
            else:
                #Since RID is held by another process,
                print("P" + currentProcess + " requests R" + currentResource)
                # Put PID in resourceWanted array to request access to RID
                resourceWanted[int(currentResource)].append(str(currentProcess))
                #P -> R
                stepsInProgram.append("P" + str(currentProcess))
                stepsInProgram.append("R" + str(currentResource))
         
        #If process is freeing
        if (requestType == "f"):
            print("P" + currentProcess + " frees R" + currentResource)
            #RID is no longer held
            allocationMatrix[int(currentStep[1])][int(currentStep[2])] = 0
            resourceHeld[int(currentResource)] = False
            #remove RID from PID's array
            processHolder[int(currentProcess)].remove("R" + str(currentResource))

            #check if RID is wanted by another PID
            if(len(resourceWanted[int(currentResource)]) > 1):
                #first value in this 2D array is the RID, which is why x = [RID][1]
                # x = holds the PID requesting access to RID
                x = resourceWanted[int(currentResource)][1]
                #Add RID to PID array
                processHolder[int(x)].append("R" + str(currentResource))
                print("R" + currentResource + " now owned by P" + x)
                #Remove PID from resourceWanted array
                resourceWanted[int(currentResource)].remove(str(x))
                #RID is now held
                resourceHeld[int(currentResource)] = True

        #-------------
        # current status of program
        #-------------
        print("\n")
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
        # Detect Deadlock using Banker’s algorithm 
        #-------------
        # Creates a list containing 5 lists, each of 8 items, all set to 0

        R = resourceR  # Total amount of each type of resource
 
        #V: vector if amount of resources available 
        for i in range(numResources):
            if resourceHeld[i] == True:
                V[i] = 0
            else:
                V[i] = 1
        

        C = claimMatrix   # amount of each resource needed by each process(P -> R)
        A = allocationMatrix  # amount of each resource held by each process (P <- R)
        N = C - A #Need
        #print("C: \n", C)
        #print("A: \n", A)
        print("N: \n", N)
        print("V: \n", V)
    

        #P > V True for ALL P, then  deadlock
        for i in range(numProcesses):
            for y in range(numResources):
                if (N[i][y] > V[y]):
                    tally += 1
                    break
        
        print(tally)


    






    def cycle(self):
        for i in range(len(input_array)):
            print("__________________________")
        
            print("Step " + str(i + 1) + "/" + str(len(input_array)))
            currentStep = input_array[i].split(" ")
            requestType = currentStep[0]
            currentProcess = currentStep[1]
            currentResource = currentStep[2]

            nextStep = input_array[i+1].split(" ")
            nextType = nextStep[0]
            nextProcess = nextStep[1]
            nextResource = nextStep[2]


