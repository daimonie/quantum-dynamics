import numpy as np

def potential(lin, tau, r, potNumber):
    ##Note: r=0 is always excluded so the trial is displayed 
    #v = lin**2 / 10 * (1+r);  
    #return v    
    if potNumber == 1:
        #Parabolic potential
        k = 0.5e6
        v = 0.5*k*(lin-5e-9)**2
        return v
    elif potNumber == 2:
        #'Infinite' Potential barrier (tunnel effect!!)
        height = 1e10
        width = 1e-4
        v = np.zeros(np.size(lin))
        for i in range( int( 0.65*np.size(lin) ) , int( (0.65 + width)*np.size(lin) )):
            v[i] = height#*abs(np.sin(2*np.pi*r/10))
        return v
    elif potNumber == 6:
        #Flat potential
        height =  100*0
        v = np.ones(np.size(lin))*height#*abs(np.sin(2*np.pi*r/20))
        return v
    elif potNumber == 4:
        #ramp
        slope = 1
        v =  np.zeros(np.size(lin))
        for i in range( int( 0.55*np.size(lin) ) , np.size(lin) ):
            v[i] = slope*(lin[i] - lin[int( 0.55*np.size(lin) )])#*abs(np.sin(2*np.pi*r/30))
        return v
    elif potNumber == 5:
        #semi-circular travelling potental
        radius = 0.1e-10
        chi = 1e-9/np.size(lin)
        scaledR = int(np.ceil(radius/chi))
        v = np.zeros(np.size(lin))
        center = 100*r - int(100.0*r/np.size(lin))*np.size(lin)
        for i in range( center-scaledR , center + scaledR ):
            v[i] = abs(( (i-center)*chi )**2 - radius**2)**0.5
        return v
    elif potNumber == 3:
        #Finite potential barriers
        width = 1e-2
        height = 1e-11
        v = np.zeros(np.size(lin))
        for i in range( int( 0.7*np.size(lin) ) , int( (0.7 + width)*np.size(lin) )):
            v[i] = height*0.1
        for i in range( int( (0.7 + 3*width)*np.size(lin) ) , int( (0.7 + 4*width)*np.size(lin) )):
            v[i] = height*0.6
        for i in range( int( (0.7 + 6*width)*np.size(lin) ) , int( (0.7 + 7*width)*np.size(lin) )):
            v[i] = height
        return v
    elif potNumber == 7:
        potential = -(lin - np.min(lin)) * (lin-np.max(lin));
        potential /= np.max(potential);
        potential *= 1e-31;
        
        return potential