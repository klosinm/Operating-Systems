import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib import animation
from matplotlib.widgets import Button, Slider


from deadlock import Detection
core = Detection

color_map = []
edge_color_map = []
shape_map = []
extraInfo = 0

 
class Animation:
    def update(self, num, G, ax, layout):
        global extraInfo
        self.extraInfo = ""
        #clear evert loop to change colors
        edge_color_map = []
        ax.clear()

        self.currentStep = core.input_array[num].split(" ")
        self.requestType = self.currentStep[0]  # "r" or "f"
        self.currentProcess = self.currentStep[1]  # PID
        self.currentResource = self.currentStep[2]  # RID
       

        print("Deadlock: ")
        print(core.deadlockSteps[num])
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
        for e in self.G.edges:
            print(e)
            if (e[0][0] == "R"):
                edge_color_map.append("lightsalmon")
            else:
                edge_color_map.append("paleturquoise")

        #Detect Deadlock, color edges red and stop simulation
        if (core.deadlockSteps[num] == 1):
                #print(list(nx.simple_cycles(G)))
                T = list(nx.simple_cycles(G))
                print(T[0])           
                self.extraInfo = "\n Deadlock!"
                for e in G.edges:
                    edge_color_map.append("red")
                #plt.pause(10)


        #title
        ax.set_title("Deadlock Detection \n Step " + str(num + 1) + "/" + str(len(core.input_array)) +
                     ": P" + str(self.currentProcess) + " " + core.verbalrequests[num] + "'s R" + str(
            self.currentResource) + self.extraInfo,
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
    def init(self):
        pass


    def simple_animation(self):
        # Build plot
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.G = nx.DiGraph()

        #add process nodes
        for i in range(core.numProcesses):
            self.G.add_node("P" + str(i))
            color_map.append("paleturquoise")

        #add resource nodes
        for i in range(core.numResources):
            self.G.add_node("R" + str(i))
            color_map.append("lightsalmon")
            
        #set graph
        self.layout = nx.circular_layout(self.G)



        ani = animation.FuncAnimation(
            self.fig, self.update, frames=len(core.input_array), init_func=self.init, interval=2500, fargs=(self.G, self.ax, self.layout), repeat=False)

        plt.show()


Animation().simple_animation()
