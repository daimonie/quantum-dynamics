from simulation import simulation   
import scipy.constants as scc 
import scipy.sparse as sparse  
import numpy as np 

sim = simulation() 

sim.mass = 1.0 
sim.chi = 1e-4  #just dx
sim.tau = 1e-2 
sim.hbar = 1.0  #scc.hbar
sim.dimensions =  1000 

sim.init() 

xRight = 1e-9 ;
xLeft = 0;

lin = np.linspace(xLeft, xRight, sim.dimensions);
psi = (30/xRight**5)**0.5 * lin * (xRight - lin); 
for i in range(1,10): 
    psi, info= sim.evolve(psi) ;
    if info == 0:  
        print i, psi
    else:
        raise Exception("For some reason, the tolerance wasn't reached.");
