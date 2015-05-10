import numpy as np

def initialPsi(lin, xLeft, xRight, psiNumber):
    if psiNumber == 1:
        #Gaussian
        psi = np.exp(-1j*2*np.pi*2/(1e-9)*lin) * np.exp( - (lin-xRight/2.0)**2 / 2.0 / (0.075e-9)**2);
        psi /= np.max(psi);
        return psi
    elif psiNumber ==2:
        #Parabola
        width = 0.2
        psi = np.zeros(np.size(lin))
        a = range( int( (0.5 - width/2)*np.size(lin) ) , int( (0.5 + width/2)*np.size(lin) ))
        for i in a:
            psi[i] = (i-a[0])*(a[-1]-i)
        psi /= np.max(psi);
        return psi
    #elif psiNumber ==3:
        ##RIght triangle
        #width = 0.2
        #height = 0.2
        #psi = np.zeros(np.size(lin))
        #a = range( int( (0.5 - width/2)*np.size(lin) ) , int( (0.5)*np.size(lin) ))
        #for i in a:
            #m = (height)/(lin[a[-1]]-lin[a[0]])
            #psi[i] = m*(lin[i]-lin[a[0]])
        #psi /= np.max(psi);
        #return psi
    elif psiNumber ==3:
        #Isosceles triangle
        width = 0.2
        height = 0.2
        psi = np.zeros(np.size(lin))
        a1 = range( int( (0.5 - width/2)*np.size(lin) ) , int( (0.5)*np.size(lin) ))
        a2 = range( int( (0.5)*np.size(lin) ) , int( (0.5 + width/2)*np.size(lin) ))
        for i in a1:
            m = (height)/(lin[a1[-1]]-lin[a1[0]])
            psi[i] = m*(lin[i]-lin[a1[0]])
        for i in a2:
            m = (-height)/(lin[a2[-1]]-lin[a2[0]])
            psi[i] = m*(lin[i]-lin[a2[-1]])
        psi /= np.max(psi);
        return psi
    #elif psiNumber ==4:
        ##Rectangle
        #width = 0.2
        #height = 0.2
        #psi = np.zeros(np.size(lin))
        #a = range( int( (0.5 - width/2)*np.size(lin) ) , int( (0.5+ width/2)*np.size(lin) ))
        #for i in a:
            #psi[i] = height
        #psi /= np.max(psi);
        #return psi
    elif psiNumber ==4:
        #real: sines, imag: cosine, norm: rectangle
        width = 0.2
        psi = np.zeros(np.size(lin))*1j
        a = np.asarray( range( int( (0.5 - width/2)*np.size(lin) ) , int( (0.5+ width/2)*np.size(lin) )) )
        for i in a:
            real = np.sin(2*np.pi*(i-a[0])/(a[-1]-a[0]))
            imag = np.cos(2*np.pi*(i-a[0])/(a[-1]-a[0]))
            psi[i] = real + 1j*imag
        return psi
    #elif psiNumber ==5:
        ##constant
        #psi = np.ones(np.size(lin))
        #return psi