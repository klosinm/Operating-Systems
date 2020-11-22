import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib import animation

from deadlock import Detection
core = Detection

color_map = []
edge_color_map = []
shape_map = []
extraInfo = 0
 
def update(num, G, ax, layout):
    global extraInfo
    extraInfo = ""
    #clear evert loop to change colors
    edge_color_map = []
    ax.clear()
    
    currentStep = core.input_array[num].split(" ")
    requestType = currentStep[0]  # "r" or "f"
    currentProcess = (currentStep[1])  # PID
    currentResource = (currentStep[2])  # RID
    print("---")
    print(" Step" + str(num+1) + ": P" + currentProcess + " " + str(core.verbalrequests[num]) + "'s R" + currentResource)

    point = core.steps[num][0] #element pointing
    point2 = core.steps[num][1] #element being pointed to

    #request resource
    if(requestType == "r" and core.verbalrequests[num] == "owns"):
        G.add_edge(point, point2)
    elif(requestType == "r" and core.verbalrequests[num] == "requests"):
        G.add_edge(point, point2)
        
    #freeing resource
    if (requestType == "f"):
        G.remove_edge(point, point2)
        #check if resource is wanted by another process
        if(num  < (len(core.input_array)-1)):
            if (core.verbalrequests[num + 1] == "now owns"):
                #remove P -> R
                G.remove_edge(core.steps[num + 1][1], core.steps[num + 1][0])
                #add R -> P
                G.add_edge(core.steps[num + 1][0], core.steps[num + 1][1])

                extraInfo = "\n " + core.steps[num + 1][1] + " now owns " + core.steps[num + 1][0]
                #remove next step in step array, since we just did the "now owns" in this current loop
                del core.verbalrequests[num+1: num + 2]
                del core.steps[num + 1 : num + 2]

   
    #add edge colors
    for e in G.edges:
        print("in egdes loop")
        if (e[0][0] == "R"):
            edge_color_map.append("blue")
        else:
            edge_color_map.append("red")

    #title
    ax.set_title("Deadlock Detection \n Step " + str(num + 1) + "/" + str(len(core.input_array)) +
                 ": P" + str(currentProcess) + " " + core.verbalrequests[num] + "'s R" + str(
                     currentResource) + extraInfo,
                 fontweight="bold")

    #Draw graph
    nx.draw(G,
            with_labels=True,
            pos=layout,
            node_color=color_map,
            edge_color=edge_color_map,
            node_shape="s",
            ax=ax)
   
#initial step, just so step 0 doesn't print twice
def init():
    pass


def simple_animation():
    # Build plot
    fig, ax = plt.subplots(figsize=(6, 5))
    G = nx.DiGraph()

    #add process nodes
    for i in range(core.numProcesses):
        G.add_node("P" + str(i))
        color_map.append("paleturquoise")
        shape_map.append("o")

    #add resource nodes
    for i in range(core.numResources):
        G.add_node("R" + str(i))
        color_map.append("lightsalmon")
        shape_map.append("v")

    #set graph
    layout = nx.circular_layout(G)

    ani = animation.FuncAnimation(
        fig, update, frames=len(core.input_array), init_func=init(), interval=2000, fargs=(G, ax, layout), repeat=False)

    plt.show()


simple_animation()
