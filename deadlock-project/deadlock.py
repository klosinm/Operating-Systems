#
# Deadlock-Detection Resource Manager
# Monica Klosin
# 11/12/2020
#
import time
import numpy as np


class Detection(object):

    f = open("scenario-2.txt", "r")  # get file
    initial_input_array = []  # inital array input
    input_array = []  # array to hold data from file

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
    print(str(numResources) + " resources. \n")

    # Get how many times there is a request (r)
    # Get how many times there is a release (f)

   

    #Know if a resource value is free or not
    resourceFree = [True] * numResources

    #step in graph
    currentStep = []
    
    # print(input_array)
    for i in range(numProcesses):
        print("P" + str(i) + ": \n")

    for i in range(numResources):
        print("R" + str(i) + ": " + str(resourceFree[i]))  

    print("\n")


  
    # List all the steps in file

    for i in range(len(input_array)):
        # print(input_array[i])
        currentStep = input_array[i].split(" ")
        # print(inputFirst)
        time.sleep(1)
        if (currentStep[0] == "r"):
            print("P" + currentStep[1] + " -> R" + currentStep[2])  # " now owns R"
            resourceFree[int(currentStep[2])] = False
            #print("R" + currentStep[2] + " is owned") 
        if (currentStep[0] == "f"):
            print("P" + currentStep[1] + " -X> R" + currentStep[2])  # " frees R"
            resourceFree[int(currentStep[2])] = True
            #print("R" + currentStep[2] + " is free")
          

    print(resourceFree)



# loop through each step, have a delay
# show results
