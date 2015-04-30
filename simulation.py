import numpy as np 
import scipy as sc 
import scipy.sparse as sparse  
import scipy.sparse.linalg as ssl 
import scipy.constants as scc  
class simulation:
    
    chi = 0.5  #dx
    tau = 0.5  #dt
    mass = 0.5  #mass of particle
    hbar = 0.5 
    
    prefactor = 1.0 
    
    H = None 
    L = None 
    R = None 
    def init(self):
        self.H = -2*sparse.eye(self.dimensions, self.dimensions) +sparse.eye(self.dimensions, self.dimensions, k=1) + sparse.eye(self.dimensions, self.dimensions, k=-1) 
        self.H.toarray() 
        
        self.prefactor = 1j * self.hbar * self.tau / self.mass / (self.chi)**2 
        self.L = sparse.eye(self.dimensions,self.dimensions) + self.prefactor * self.H 
        self.R = sparse.eye(self.dimensions,self.dimensions) - self.prefactor * self.H 
    def evolve(self, lastPsi): 
        return ssl.bicgstab(self.L, self.R * lastPsi, x0=lastPsi, tol=1e-10)  