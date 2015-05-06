from simulation import simulation   
import scipy.constants as scc 
import scipy.sparse as sparse  
import numpy as np 

sim = simulation() 

sim.mass = 1.0 
sim.chi = 1e-4  #just dx
sim.tau = 4e-5 
sim.hbar = 1.0  #scc.hbar
sim.dimensions =  1000 

sim.init() 

xRight = 1e-9 ;
xLeft = 0;

lin = np.linspace(xLeft,xRight, sim.dimensions);
psi = 1/(45000.0) * (30/xRight**5)**0.5 * lin * (xRight - lin); 

sim.setPsi(lin, psi)
#sim.potential()
#sim.potentialTime()
sim.show();