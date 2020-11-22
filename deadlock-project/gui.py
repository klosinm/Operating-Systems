import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation


def simple_update(num, G, ax, numsteps):
    ax.clear()

    # Draw the graph with random node colors
 
    G.add_edge(num, num+1)
    
    nx.draw(G, pos=nx.circular_layout(G), with_labels=True, ax=ax)



    # Set the title
    ax.set_title("Frame {}".format(num))


def simple_animation():

    # Build plot
    fig, ax = plt.subplots(figsize=(6, 4))

    # Create a graph and layout
    
   
    G = nx.DiGraph()
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    numsteps = 3


    ani = animation.FuncAnimation(
        fig, simple_update, frames=numsteps, interval=1500, fargs=(G, ax, numsteps))
  

    plt.show()


simple_animation()
