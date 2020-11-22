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
 
#pos = nx.get_node_attributes(G, 'pos')



#Get all distinct node classes according to the node shape attribute
#nodeShapes = set((aShape[1]["color"] for aShape in G.nodes(data=True)))

def update(num, G, ax, layout):
    global extraInfo
    extraInfo = ""
    ax.clear()

    currentStep = core.input_array[num].split(" ")
    requestType = currentStep[0]  # "r" or "f"
    currentProcess = (currentStep[1])  # PID
    currentResource = (currentStep[2])  # RID
    print(" Step" + str(num+1) + ": P" + currentProcess + " " + str(core.verbalrequests[num]) + "'s R" + currentResource)
 
    #print(core.steps[num])
    point = core.steps[num][0]
    point2 = core.steps[num][1]

    if(requestType == "r" and core.verbalrequests[num] == "owns"):
        G.add_edge(point, point2)
        extraInfo = ""
        #print("in owns")
        #edge_color_map.append("blue")
    elif(requestType == "r" and core.verbalrequests[num] == "requests"):
        G.add_edge(point, point2)
        extraInfo = ""
       # print("in requests")
        #edge_color_map.append("red")
    

    if (requestType == "f"):
        #print("in free ")
        print(core.verbalrequests[num])
        print(core.steps[num])
        G.remove_edge(point, point2)

        if(num  < (len(core.input_array)-1)):
            if (core.verbalrequests[num + 1] == "now owns"):
                
              
                #print("and own ")
                print(core.verbalrequests[num + 1])
                print(core.steps[num+1])
                G.remove_edge(core.steps[num + 1][1], core.steps[num + 1][0])
                G.add_edge(core.steps[num + 1][0], core.steps[num + 1][1])
                extraInfo = "\n " +  core.steps[num+1][1] + " now owns "  + core.steps[num+1][0]
                del core.verbalrequests[num+1: num + 2]
                del core.steps[num + 1 : num + 2]




    ax.set_title("Deadlock Detection \n Step " + str(num + 1) + "/" + str(len(core.input_array)) +
                 ": P" + str(currentProcess) + " " + core.verbalrequests[num] + "'s R" + str(
                     currentResource) + extraInfo,
             fontweight="bold")



   
    nx.draw(G,
            with_labels=True,
            pos=layout,
            node_color=color_map,
            #edge_color=edge_color_map,
            node_shape="s",
            ax=ax)
   
    


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
        fig, update, frames=len(core.input_array), interval=2000, fargs=(G, ax, layout), repeat=False)

    plt.show()


simple_animation()









