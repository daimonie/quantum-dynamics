from simulation import simulation   
import scipy.constants as scc 
import scipy.sparse as sparse  
import numpy as np 
import argparse as argparse
from potential import potential
from initialPsi import initialPsi

parser = argparse.ArgumentParser(prog="python main.py",
  description = "main.py handles everything.  Use python main.py -h to see your options.");

parser.add_argument('-p', '--potential', help='Choose the form of the potential. 1: parabolic, 2: infinite wall, 3: finite walls, 4: ramp, 5: moving semi-circle, 6: constant.', default = 3, action='store', type = int);
parser.add_argument('-w', '--waveFunc', help='Choose the form of psi. 1: gaussian, 2: parabola, 3: triangle, 4: sines/cosines.', default = 4, action='store', type = int);
parser.add_argument('-tm', '--timemultiply', help='Speed up the animation with $value$. This multiplies the tau by $value$.', default = 1.0, action='store', type = float);
args = parser.parse_args();

sim = simulation() 

sim.hbar = scc.hbar
sim.mass = scc.m_e

sim.argsPotential = args.potential


sim.dimensions =  1000
sim.chi = 1e-9/sim.dimensions  #just dx
#1e-18 accounts for mass and the nm, while the sim.dimensions**-2 accounts for the parameters of the simulation.
#The last number, 0.1 at the time of writing, is the timestep in the simulation in a way that makes sense.
sim.tau = 1e-18 * (sim.dimensions)**(-2.0) * 4.0 * sim.mass / sim.hbar * 1.0e2 * args.timemultiply

sim.init() 

xRight = 10e-9 ;
xLeft = 0;

lin = np.linspace(xLeft,xRight, sim.dimensions)
psi = initialPsi(lin, xLeft, xRight, args.waveFunc)

sim.setPsi(lin, psi)
sim.potentialCallback = potential 
sim.show();