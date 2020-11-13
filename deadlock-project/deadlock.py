#
# Deadlock-Detection Resource Manager
# Monica Klosin
# 11/12/2020
#
import time

class Detection(object):

    f = open("scenario-1.txt", "r")  # get file
    my_file = []  # read in raw data
    initial_input_array = []  # inital array input
    input_array = []  # array to hold data from file
    element = []  #remove new line
    i = 0  #guess star integer
    currentStep = []  # step in graph
    nodeHolder = [] #holds the processes w/their held resources
   

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
    for i in range(numProcesses):
        nodeHolder.append(["P" + str(i)])
    
    for i in range(len(input_array)):
        print("__________________________\n")
        currentStep = input_array[i].split(" ")
        time.sleep(1)

        #if step is requesting
        if (currentStep[0] == "r"):
            print("Step " + str(i+1) + "/" + str(len(input_array))  + " | P" + currentStep[1] + " -> R" + currentStep[2])
            resourceHeld[int(currentStep[2])] = True
            nodeHolder[int(currentStep[1])].append(currentStep[2])
          
        #If step is free
        if (currentStep[0] == "f"):
            print("Step " + str(i+1) + "/" + str(len(input_array)) + " | P" + currentStep[1] + " X R" + currentStep[2])  # " frees R"
            resourceHeld[int(currentStep[2])] = False
            nodeHolder[int(currentStep[1])].remove(currentStep[2])

        #print out the current status 
        for i in range(numProcesses):
            print(nodeHolder[i])
        for i in range(numResources):
            print("R" + str(i) + ": " + str(resourceHeld[i]))
