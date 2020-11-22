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
#pos = nx.get_node_attributes(G, 'pos')



#Get all distinct node classes according to the node shape attribute
#nodeShapes = set((aShape[1]["color"] for aShape in G.nodes(data=True)))



def update(num, G, ax, layout):
    currentStep = core.input_array[num].split(" ")
    requestType = currentStep[0]  # "r" or "f"
    currentProcess = (currentStep[1])  # PID
    currentResource = (currentStep[2])  # RID
    print("Step" + str(num) + ": P" + currentProcess + " " + requestType + "'s R" + currentResource)
    point = core.steps[num][0]
    point2 = core.steps[num][1]
    if(requestType == "r" and core.resourceHeld[int(currentResource)] == False):
        G.add_edge(point, point2)
        edge_color_map.append("red")
    elif(requestType == "r" and core.resourceHeld[int(currentResource)] == True):
        G.add_edge(point2, point)
        edge_color_map.append("blue")
    

    if(requestType == "f" ):
        G.remove_edge(point, point2)


    ax.clear()


    nx.draw(G,
            with_labels=True,
            pos=layout,
            node_color=color_map,
            edge_color=edge_color_map,
            node_shape="s",
            ax=ax)
    ax.set_title("Deadlock Detection \n Step " + str(num + 1) + "/" + str(len(core.input_array)) + ": P" + str(currentProcess) + " " + requestType + "'s R" + str(currentResource), fontweight="bold")
    #ax.set_title("Deadlock Detection \n Step {}/8: P0 requests and owns R0".format(num), fontweight="bold")


def simple_animation():
    # Build plot
    fig, ax = plt.subplots(figsize=(6, 5))
    G = nx.DiGraph()

    for i in range(core.numProcesses):
        G.add_node("P" + str(i))
        color_map.append("paleturquoise")
        shape_map.append("o")

    for i in range(core.numResources):
        G.add_node("R" + str(i))
        color_map.append("lightsalmon")
        shape_map.append("v")


    


    layout = nx.circular_layout(G)

    ani = animation.FuncAnimation(
        fig, update, frames=len(core.input_array), interval=1000, fargs=(G, ax, layout), repeat=False)

    plt.show()


simple_animation()









