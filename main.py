from simulation import simulation   
import scipy.constants as scc 
import scipy.sparse as sparse  
import numpy as np 

def potential(lin, tau, r):
    #Note: r=0 is always excluded so the trial is displayed 
    v = lin / 10 * (1+r)*0;  
    return v    

sim = simulation() 

sim.hbar = scc.hbar
sim.mass = scc.m_e


sim.dimensions =  1000
sim.chi = 1e-9/sim.dimensions  #just dx
#1e-18 accounts for mass and the nm, while the sim.dimensions**-2 accounts for the parameters of the simulation.
#The last number, 0.1 at the time of writing, is the timestep in the simulation in a way that makes sense.
sim.tau = 1e-18 * (sim.dimensions)**(-2.0) * 4 * sim.mass / sim.hbar * 1.0e3

sim.init() 

xRight = 1e-9 ;
xLeft = 0;

lin = np.linspace(xLeft,xRight, sim.dimensions)
psi = np.exp(1j*2*np.pi*2/(1e-9)*lin) * np.exp( - (lin-0.5e-9)**2 / 2 / (0.075e-9)**2);
psi /= np.max(psi);

sim.setPsi(lin, psi)
sim.potentialCallback = potential 
sim.show();