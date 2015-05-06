import numpy as np 
import scipy as sc 
import scipy.sparse as sparse  
import scipy.sparse.linalg as ssl 
import scipy.constants as scc  
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class simulation:
    
    chi = 0.5  #dx
    tau = 0.5  #dt
    mass = 0.5  #mass of particle
    hbar = 0.5 
    
    prefactor = 1.0 
    
    H = None 
    L = None 
    R = None 
    
    fig = None
    
    ax1 = None
    ax2 = None
    ax3 = None
    
    line1 = None
    line2 = None
    line3 = None
    
    psi = None
    
    space = None;
    def init(self):
        #Display logic
        self.initFigure()
    
        #Calculations
        self.H = -2*sparse.eye(self.dimensions, self.dimensions) +sparse.eye(self.dimensions, self.dimensions, k=1) + sparse.eye(self.dimensions, self.dimensions, k=-1) 
        self.H.toarray() 
        
        self.prefactor = 1j * self.hbar * self.tau / self.mass / (self.chi)**2 
        self.L = sparse.eye(self.dimensions,self.dimensions) + self.prefactor * self.H 
        self.R = sparse.eye(self.dimensions,self.dimensions) - self.prefactor * self.H 
        
        #We need to add a part here to add the time-independent part of V(r), since this is just a part of H.
        #We also need to incorporate the logic for the time-dependent part of V(r) into the class.
        #Both should be done by callback functions.
    def evolve(self): 
        self.psi, info = ssl.bicgstab(self.L, self.R * self.psi, x0=self.psi, tol=1e-10);
        #Time-dependent potential logic
        
        if info != 0:
            raise Exception("Tolerance wasn't met?");
    def setPsi(self, lim, psi):
        self.space = lim
        self.psi = psi    
        
        self.ax1.set_xlim( [self.space[0], self.space[-1]] )
        self.ax2.set_xlim( [self.space[0], self.space[-1]] )
        self.ax3.set_xlim( [self.space[0], self.space[-1]] )
        
    def initFigure(self):
        self.fig = plt.figure();
        self.fig.clf()                       #clear figure
        
        self.ax1 = self.fig.add_subplot(3,1,1)     
        self.ax2 = self.fig.add_subplot(3,1,2)     
        self.ax3 = self.fig.add_subplot(3,1,3)     
        
        self.ax1.grid()
        self.ax2.grid()
        self.ax3.grid()
    
        self.ax1.set_xlabel('Position')
        self.ax2.set_xlabel('Position')
        self.ax3.set_xlabel('Position')
        
        self.ax1.set_ylabel('Re(Psi)')
        self.ax2.set_ylabel('Im(Psi)')
        self.ax3.set_ylabel('Norm(Psi)')
        
        self.ax1.set_ylim( [-2, 2] );
        self.ax2.set_ylim( [-2, 2] );
        self.ax3.set_ylim( [-2, 2] );
    def propagate(self, r):
        #r contains the number of the frame, starting at zero :)
        #This can be used for the time-dependent potential
        #First, evolve
        if r != 0:
            self.evolve();        
        #Now plot it 
        realPsi = np.real(self.psi);
        imagPsi = np.imag(self.psi);
        normPsi = np.absolute(self.psi);
        if r == 0:
            self.line1, = self.ax1.plot(self.space, realPsi);
            self.line2, = self.ax2.plot(self.space, imagPsi);
            self.line3, = self.ax3.plot(self.space, normPsi);
        else:
            self.line1.set_ydata( realPsi )
            self.line2.set_ydata( imagPsi )
            self.line3.set_ydata( normPsi )
        
        
    def show(self):
        
        ani = animation.FuncAnimation(self.fig, self.propagate,interval=100) 
        
        plt.show()