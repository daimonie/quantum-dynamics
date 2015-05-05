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
    if count == 0:
        xRight = 1e-9
        xLeft = 0
        lin = np.linspace(xLeft, xRight, sim.dimensions)
        psi = (30/xRight**5)**0.5 * lin * (xRight - lin)
        count +=1
    fig.clf() #clear figure
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)    
    psi, info= sim.evolve(psi)
    z = [(i.real**2 + i.imag**2)**0.5 for i in psi] #modulus of psi
    x = np.arange(0,(sim.dimensions)*sim.chi ,sim.chi)    #Position
    placeInPlot= {'r': psi.real, 'i':psi.imag, 'm': z}
    plotLabels= {'r': 'Real part', 'i':'Imaginary part', 'm': 'Modulus'} 
    Y1 = placeInPlot[args.visualize[0]]
    Y2 = placeInPlot[args.visualize[1]]
    if len(args.visualize) == 3:
        Y3 = placeInPlot[args.visualize[2]]
        s1 = ax1.scatter(x,Y1,c=Y3,linewidth = 0,s = 80)
        s2 = ax2.scatter(x,Y2,c=Y3,linewidth = 0,s = 80)
        cb1 = plt.colorbar(mappable=s1,ax=ax1)
        cb2 = plt.colorbar(mappable=s2,ax=ax2)
        cb1.set_label(plotLabels[args.visualize[2]])
        cb2.set_label(plotLabels[args.visualize[2]])
        ax1.plot(x,Y1,linewidth=0.1)
        ax2.plot(x,Y2,linewidth=0.2)
    if len(args.visualize) == 2:
        ax1.plot(x,Y1)
        ax2.plot(x,Y2)
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel(plotLabels[args.visualize[0]])
    ax2.set_ylabel(plotLabels[args.visualize[1]])
    ax2.set_xlabel('Position')

ani = animation.FuncAnimation(fig,propagate,interval=100)
plt.show()