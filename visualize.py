from simulation import simulation   
import scipy.constants as scc 
import scipy.sparse as sparse  
import numpy as np 
import argparse as argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation

parser = argparse.ArgumentParser(prog="python visualize.py",
  description = "visualize.py handles visualization.  Use python visualize.py -h to see your options.");

parser.add_argument('-v', '--visualize', help='String composed of 2 or 3 letters. Each letter can be either "r", "i" or "m", meaning "real part", "imaginary part" and "modulus", respectively. THe first letter goes to the top plot, the second to the bottom and the third (optional) is plotted as color.', default = 'rim', action='store', type = str);
args = parser.parse_args();


global fig,count
fig = plt.figure()
count = 0

def propagate(r):
    global fig, psi,count
    sim = simulation()
    sim.mass = 1.0 
    sim.chi = 1e-4  #just dx
    sim.tau = 1e-2
    sim.hbar = 1.0  #scc.hbar
    sim.dimensions =  1000 
    sim.init()
    #If this is the first time that function propagate is called (i.e. count = 0), generate initial psi
    if count == 0:
        xRight = 1e-9
        xLeft = 0
        lin = np.linspace(xLeft, xRight, sim.dimensions)
        psi = (30/xRight**5)**0.5 * lin * (xRight - lin)
        count +=1
        
    #Actual plotting logic starts here    
    fig.clf()                       #clear figure
    ax1 = fig.add_subplot(2,1,1)    #I want two plots in the same figure
    ax2 = fig.add_subplot(2,1,2)    #I want two plots in the same figure
    
    
    psi, info= sim.evolve(psi)      #Evolve psi
    z = [(i.real**2 + i.imag**2)**0.5 for i in psi]     #calculate modulus of psi
    x = np.arange(0,(sim.dimensions)*sim.chi ,sim.chi)  #Position
    placeInPlot= {'r': psi.real, 'i':psi.imag, 'm': z}  #Dictionary: Will be used to assign where to plot each function, depending on the choice made by the user in parser. 
    plotLabels= {'r': 'Real part', 'i':'Imaginary part', 'm': 'Modulus'} #Same as above, but for the labels of the plots
    Y1 = placeInPlot[args.visualize[0]] #Assign to Y1 the function corresponding to the the first letter passed to parser.
    Y2 = placeInPlot[args.visualize[1]] #Assign to Y2 the function corresponding to the the second letter passed to parser.
    #If the user passed a third letter to parser (optional)
    if len(args.visualize) == 3:
        Y3 = placeInPlot[args.visualize[2]] ##Assign to Y3 the function corresponding to the the third letter passed to parser.
        
        s1 = ax1.scatter(x,Y1,c=Y3,linewidth = 0,s = 80) #Show Y1(x) in the first plot. Assign a color to the markers according to the value of Y3.
        s2 = ax2.scatter(x,Y2,c=Y3,linewidth = 0,s = 80) #Show Y2(x) in the second plot. Assign a color to the markers according to the value of Y3.
        
        cb1 = plt.colorbar(mappable=s1,ax=ax1)  #Show colorbar in first plot
        cb2 = plt.colorbar(mappable=s2,ax=ax2)  #Show colorbar in second plot
        
        cb1.set_label(plotLabels[args.visualize[2]]) #Show in the colorbar of plot1 the label corresponding to the the first letter passed to parser.
        cb2.set_label(plotLabels[args.visualize[2]]) #Show in the colorbar of plot2 the label corresponding to the the second letter passed to parser.
        
        ax1.plot(x,Y1,linewidth=0.1)    #Plot a thin line (superimposed to the scatter plot) so that we can see which data-point is connected to each other.
        ax2.plot(x,Y2,linewidth=0.2)    #same as above, for plot2
    #If the user passed only two arguments to parser
    if len(args.visualize) == 2:
        ax1.plot(x,Y1)  #Show Y1(x) in the first plot
        ax2.plot(x,Y2)  #Show Y2(x) in the second plot
    ax1.grid()  #Show grid in first plot
    ax2.grid()  #Show grid in second plot
    ax1.set_ylabel(plotLabels[args.visualize[0]])   #Assign the label of the first plot according to the first letter passed to parser
    ax2.set_ylabel(plotLabels[args.visualize[1]])   #Assign the label of the second plot according to the second letter passed to parser
    ax2.set_xlabel('Position')  #Position is always plotted in the x axis

ani = animation.FuncAnimation(fig,propagate,interval=100)
plt.show()