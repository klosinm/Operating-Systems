import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph
import time
import seaborn.apionly as sns
import matplotlib.animation


from deadlock import Detection
core = Detection

G = nx.DiGraph()
color_map = []
shape_map = []
#pos = nx.get_node_attributes(G, 'pos')


for i in range(core.numProcesses):
    G.add_node("P" + str(i))  # , pos=(i,1))
    color_map.append("paleturquoise")
    shape_map.append("o")


for i in range(core.numResources):
    G.add_node("R" + str(i))  # , color="lightsalmon", shape='square')
    color_map.append("lightsalmon")
    shape_map.append("v")


#Get all distinct node classes according to the node shape attribute
#nodeShapes = set((aShape[1]["color"] for aShape in G.nodes(data=True)))


for j in range(len(core.steps)):
        currentStep = core.input_array[j].split(" ")
        requestType = currentStep[0]  # "r" or "f"
        currentProcess = (currentStep[1])  # PID
        currentResource = (currentStep[2])  # RID

        print("Step " + str(j + 1) + "/" + str(len(core.input_array)))
        print("P" + currentProcess + " " +
              requestType + "'s R" + currentResource)
        point = core.steps[j][0]
        point2 = core.steps[j][1]
        if(requestType == "r"):
            G.add_edge(point, point2)
        if(requestType == "f"):
            G.remove_edge(point, point2)


def unpdate(num):
    ax.clear()


ax = plt.gca()
ax.set_title(
    "Deadlock Detection \n Step 1/8: P0 requests and owns R0", fontweight="bold")


nx.draw(G,
        with_labels=True,
        pos=nx.circular_layout(G),
        node_color=color_map,
        node_shape="s",
        ax=ax)
plt.show()
