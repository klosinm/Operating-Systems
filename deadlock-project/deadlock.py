#
# Deadlock-Detection Resource Manager
# Monica Klosin
# 11/12/2020
#
import time
import re

class Detection(object):

    f = open("scenario-3.txt", "r")  # get file
    my_file = []  # read in raw data
    initial_input_array = []  # inital array input
    input_array = []  # array to hold data from file
    element = []  #remove new line
    i = 0  #guest star integer
    x = 0  #guest star integer
    
    currentStep = []  # step in graph
    processHolder = []  # holds the processes w/their held resources
    resourcesPWaiting = []  #holds the resources P#ID waits for
    resourceWanted = []  #Holds resources wanting to be held by P
    
    requestType = []  #holds if the step in program is a "r" or "f"
    currentProcess = []  #hold value of current process in program
    currentResource = []  #hold value of current resource in program
    stepsInProgram = [] #hold steps taken in program
    

    # read in raw data into array
    with f as my_file:
        initial_input_array = my_file.readlines()

    # remove '\n' from array
    for element in initial_input_array:
        input_array.append(element.strip())

    # Get number of processes
    numProcesses = int(input_array.pop(0).split(' ')[0])
    print(str(numProcesses) + " processes.")

    # Get number of resources
    numResources = int(input_array.pop(0).split(' ')[0])
    print(str(numResources) + " resources. ")

    #Know if a resource value is free or not
    resourceHeld = [False] * numResources

    #Initialize how many process arrays there will  be
    #is what is outputed to terminal to show status of P
    for i in range(numProcesses):
        processHolder.append(["P" + str(i)])

    #Initialize how many process waiting arrays there will  be
    #Holds the resources P desire
    for i in range(numProcesses):
        resourcesPWaiting.append(["P" + str(i)])

    #Know if a resource value is wanted or not
    for i in range(numResources):
        resourceWanted.append([str(i)])





    for i in range(len(input_array)):
        print("__________________________\n")
        time.sleep(1)
        print("Step " + str(i + 1) + "/" + str(len(input_array)))
        currentStep = input_array[i].split(" ")
        requestType = currentStep[0]
        currentProcess = currentStep[1]
        currentResource = currentStep[2]
        
 
       
        #if process is requesting
        if (requestType == "r"):
        
            #check if resource is free
            if (resourceHeld[int(currentResource)] == False):
                print("R" + currentResource + " owned by P" + currentProcess)
                resourceHeld[int(currentResource)] = True
                processHolder[int(currentProcess)].append("R" + str(currentResource))

                stepsInProgram.append("R" + str(currentResource))
                stepsInProgram.append( "P" + str(currentProcess))
            else:
                print("P" + currentProcess + " requests R" + currentResource)
                #Share that resource is wanted, Put resource in P ID waiting array
                resourceWanted[int(currentResource)].append(str(currentProcess))
                resourcesPWaiting[int(currentProcess)].append("R" + str(currentResource))

                stepsInProgram.append("P" + str(currentProcess))
                stepsInProgram.append("R" + str(currentResource))
         
        #print(resourceWanted)

        #If step is freeing
        if (requestType == "f"):
            print( "P" + currentProcess + " frees R" + currentResource) 
            resourceHeld[int(currentResource)] = False
            processHolder[int(currentProcess)].remove("R" + str(currentResource))

            #check if resource is wanted by any other P
            if(len(resourceWanted[int(currentResource)]) > 1):
                
                x = resourceWanted[int(currentResource)][1]
                processHolder[int(x)].append("R" + str(currentResource))
                print("R" + currentResource + " now owned by P" + x)
                resourceWanted[int(currentResource)].remove(str(x))                  

        #print out the current status
        print("\n")
        for i in range(numProcesses):
            print(processHolder[i])
        for i in range(numResources):
            print("R" + str(i) + ": " + str(resourceHeld[i]))



    def cycle(self):
        for i in range(len(input_array)):
            print("__________________________\n")
        
            print("Step " + str(i + 1) + "/" + str(len(input_array)))
            currentStep = input_array[i].split(" ")
            requestType = currentStep[0]
            currentProcess = currentStep[1]
            currentResource = currentStep[2]

            nextStep = input_array[i+1].split(" ")
            nextType = nextStep[0]
            nextProcess = nextStep[1]
            nextResource = nextStep[2]


