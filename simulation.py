import numpy as np 
import scipy as sc 
import scipy.sparse as sparse  
import scipy.sparse.linalg as ssl 
import scipy.constants as scc  
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class simulation:
    
    chi     = 0.5  #dx
    tau     = 0.5  #dt
    mass    = 0.5  #mass of particle
    hbar    = 0.5 
    
    prefactor = 1.0 
    
    H = None 
    L = None 
    R = None 
    
    fig = None
    
    ax1 = None
    ax2 = None
    ax3 = None
    ax4 = None
    
    line1 = None
    line2 = None
    line3 = None
    line4 = None
    
    psi = None
    
    space               = None
    potentialCallback   = None
    potential           = None
    
    argsPotential   = None
    
    def init(self):
        #Display logic
        self.initFigure()
    
        #Calculations
        self.H = -2*sparse.eye(self.dimensions, self.dimensions) +sparse.eye(self.dimensions, self.dimensions, k=1) + sparse.eye(self.dimensions, self.dimensions, k=-1) 
        #self.H.toarray() 
        
        self.prefactor = 1j * self.hbar * self.tau / 4.0 / self.mass / (self.chi)**2   
        
        self.L = sparse.eye(self.dimensions,self.dimensions) + self.prefactor * self.H 
        self.R = sparse.eye(self.dimensions,self.dimensions) - self.prefactor * self.H
            
        #U = self.R.H / self.L
        #print U * U.H
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
        self.ax4.set_xlim( [self.space[0], self.space[-1]] )
        
    def initFigure(self):
        self.fig = plt.figure();
        self.fig.clf()                       #clear figure
        
        self.ax1 = self.fig.add_subplot(4,1,1)     
        self.ax2 = self.fig.add_subplot(4,1,2)     
        self.ax3 = self.fig.add_subplot(4,1,3)     
        self.ax4 = self.fig.add_subplot(4,1,4)     
        
        self.ax1.grid()
        self.ax2.grid()
        self.ax3.grid()
        self.ax4.grid()
    
        self.ax1.set_xlabel('Position')
        self.ax2.set_xlabel('Position')
        self.ax3.set_xlabel('Position')
        self.ax4.set_xlabel('Position')
        
        self.ax1.set_ylabel('Re(Psi)')
        self.ax2.set_ylabel('Im(Psi)')
        self.ax3.set_ylabel('Norm(Psi)')
        self.ax4.set_ylabel('Potential')
        
        self.ax1.set_ylim( [-1.1, 1.1] );
        self.ax2.set_ylim( [-1.1, 1.1] );
        self.ax3.set_ylim( [0, 1.1] );
        self.ax4.set_ylim( [-1.1, 1.1] );
    def propagate(self, r):
        #r contains the number of the frame, starting at zero :)
        #This can be used for the time-dependent potential
        
        #Note that I have no idea why it has the initial psi fixed. It does look good, so I'm not going to try and fix it.
        #First, evolve
        self.potential = self.potentialCallback( self.space, self.tau, r, self.argsPotential) 
        if r != 0:
            self.evolve();        
            
            exponentPotential = np.exp( -1j*self.tau * self.potential / self.hbar );
            
            self.psi = np.multiply(exponentPotential, self.psi)
         
        self.ax4.set_ylim( [np.min(self.potential), np.max(self.potential)] ); 
        
        #Now plot it 
        realPsi = np.real(self.psi);
        imagPsi = np.imag(self.psi);
        normPsi = np.absolute(self.psi);
        if r == 0:
            self.line1, = self.ax1.plot(self.space, realPsi);
            self.line2, = self.ax2.plot(self.space, imagPsi);
            self.line3, = self.ax3.plot(self.space, normPsi);
            self.line4, = self.ax4.plot(self.space, self.potential);
        else:
            self.line1.set_ydata( realPsi )
            self.line2.set_ydata( imagPsi )
            self.line3.set_ydata( normPsi )
            self.line4.set_ydata( self.potential ); 
        print "Animation frame %d . Norm surface %2.3e . Energy %2.3e" % (r, np.sum(np.square(normPsi))*self.chi,  self.energy());
    def show(self):
        
        ani = animation.FuncAnimation(self.fig, self.propagate,interval=100) 
        
        plt.show()
    def energy(self):
        H0 = 1j * self.hbar * self.prefactor * self.H
        H1 = np.diag(self.potential) 
        Htotal = H0 + H1 
        ket = np.dot(Htotal, np.array(self.psi).T)
        bra = np.array(self.psi).conj()
        return np.sum(np.sum(np.dot(ket,bra)))