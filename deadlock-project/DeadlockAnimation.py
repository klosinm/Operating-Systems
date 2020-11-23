#
# Deadlock-Detection Resource Manager
# Monica Klosin
# 11/22/2020
#
# DeadlockAnimation class renders the animation from steps
# provided from the AnimationAssistant class
#

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation

#importing the variables from AnimationAssistant class
#if a variable from the AnimationAssistant class is used,
#must add "core." to the start of the variable
from AnimationAssistant import Detection
core = Detection

color_map = []  # map node colors to all nodes
edge_color_map = []  # map edge colors to all edges
shape_map = []  # map shapes to process and resource nodes (not working)
extraInfo = 0  # append extra information to title, like "Deadlock!"

class Animation:
    #---------------------------------------
    # METHOD update
    # args:
    # num = step in program
    # G = graph
    # ax = allows us to change title of plt
    #
    # - renders steps in program
    # - detects deadlock, displays deadlock 
    #   as last step in animation 
    #---------------------------------------
    def update(self, num, G, ax):
        global extraInfo
        self.extraInfo = ""
        #clear color array each step to change edge colors
        edge_color_map = []
        ax.clear()

        self.currentStep = core.input_array[num].split(" ")
        self.requestType = self.currentStep[0]  # "r" or "f"
        self.currentProcess = self.currentStep[1]  # PID
        self.currentResource = self.currentStep[2]  # RID

        self.point = core.steps[num][0]  # element pointing
        self.point2 = core.steps[num][1]  # element being pointed to

        #request resource
        if(self.requestType == "r" and core.verbalrequests[num] == "owns"):
            G.add_edge(self.point, self.point2)
        elif(self.requestType == "r" and core.verbalrequests[num] == "requests"):
            G.add_edge(self.point, self.point2)

        #freeing resource
        if (self.requestType == "f"):
            G.remove_edge(self.point, self.point2)
            #check if resource is wanted by another process
            if(num < (len(core.input_array)-1)):
                if (core.verbalrequests[num + 1] == "now owns"):
                    #remove P -> R
                    G.remove_edge(core.steps[num + 1]
                                  [1], core.steps[num + 1][0])
                    #add R -> P
                    G.add_edge(core.steps[num + 1][0], core.steps[num + 1][1])
                    #add to title that a Process now owns a previously requested Resource
                    self.extraInfo = "\n " + \
                        core.steps[num + 1][1] + " now owns " + \
                        core.steps[num + 1][0]
                    #remove next step in step array,
                    #since we just did the "now owns" in this current step and don't want to repeat it
                    del core.verbalrequests[num+1: num + 2]
                    del core.steps[num + 1: num + 2]

        #add edge colors
        for e in self.G.edges:
            if (e[0][0] == "R"):
                edge_color_map.append("lightsalmon")
            else:
                edge_color_map.append("paleturquoise")

        #Detect Deadlock, color edges red and stop simulation
        if (core.deadlockSteps[num] == 1):
            #T: array of nodes in cycle for deadlock
            T = list(nx.simple_cycles(self.G))
            #add to title that deadlock occured
            self.extraInfo = "\n Deadlock!"
            #color nodes in deadlock red
            for e in self.G.edges:

                for i in range(len(T[0])):
                    if (e[0] == T[0][i]):
                        edge_color_map[i] = "crimson"
            #Hault animation, since no more steps can occur
            self.ani.event_source.stop()   

        #set title
        ax.set_title("Deadlock Detection \n Step " + str(num + 1) + "/" + str(len(core.input_array)) +
                     ": P" + str(self.currentProcess) + " " + core.verbalrequests[num] + "'s R" + str(
            self.currentResource) + self.extraInfo,
            fontweight="bold")

        #Draw graph
        nx.draw(G,
                with_labels=True,
                pos=nx.circular_layout(self.G),
                node_color=color_map,
                edge_color=edge_color_map,
                node_shape="s",
                ax=ax)

    #---------------------------------------
    # METHOD init
    # - created so step 0 doesn't print twice
    #---------------------------------------
    def init(self):
        pass

    #---------------------------------------
    # METHOD simple_animation
    # - creates plot 
    # - creates Graph
    # - renders frames for animation
    # - (optional) creates gif of animation 
    #---------------------------------------
    def simple_animation(self):
        # Build plot 
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        #Declare G as a directed (arrows) graph
        self.G = nx.DiGraph()

        #add process nodes
        for i in range(core.numProcesses):
            self.G.add_node("P" + str(i))
            color_map.append("paleturquoise")

        #add resource nodes
        for i in range(core.numResources):
            self.G.add_node("R" + str(i))
            color_map.append("lightsalmon")

        #animation!
        self.ani = animation.FuncAnimation(
            self.fig, self.update, frames=len(core.input_array), init_func=self.init, interval=1500, fargs=(self.G, self.ax), repeat=False)
        #create gif,
        #comment out to make gif, keeping uncommented messes up the arrays and renders graph in plt.show incorrectly
        #self.ani.save('deadlockdetection.gif', writer='PillowWriter', fps=.75)
        plt.show()

#Call simple_animation() method from Animation() class
Animation().simple_animation()
