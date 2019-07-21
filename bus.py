#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:08:08 2019

@author: vpfernandez
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats

from qol import average,vlookup

p=0.90

nn = 100000
full = np.zeros((30*2))
fullwas = np.zeros((30*2))   
fullwas2 = np.zeros((30*2))  
tick = 0

for h in np.arange(0,30,0.5):
    #nl()
    proba = []
    wasted = []
    
    départ = h
    temps_marche = np.random.normal(7.3,0.2,nn) #Google 9 min, test [7.4,7.5,7]
    wait_trafic_light = np.random.uniform(0,2,nn)
    wait_luas = np.random.exponential(7,nn) #every 2-8 min test [1/10/16]
    
    temps_luas = np.random.normal(5.5,0.5,nn) #CORRECT Google 5 min [6.32,5.3]
    trajet = temps_marche + wait_trafic_light + wait_luas + temps_luas
    
    heure_bus = np.random.normal(40,1,nn) #[10,]
    
    caught = départ+trajet < heure_bus
    waste = heure_bus - (départ+trajet)

    proba = np.sum(caught)/len(caught)    
    waste2 = np.minimum.reduce([heure_bus-départ,trajet])

    wastex = np.concatenate(((heure_bus - (départ+(trajet-(wait_trafic_light+wait_luas))))[caught == True],
                             (trajet)[caught == False]))

    full[int(h*2)] = proba
    fullwas[int(h*2)] = average(wastex)
    
    tick += 1
    if tick % 6 == 0:
        print(round((tick/len(np.arange(0,30,0.5)))*100),'%')

#Interpolation cubic spline
x1 = np.arange(0-40,30-40,0.5)
z = scipy.interpolate.CubicSpline(x1,full)

x = np.arange(0-40,30-40,0.01)
y = z(x)

z2 = scipy.interpolate.CubicSpline(x1,fullwas)
fullwas_i = z2(x)        

inflac = vlookup(p,y,x,exact=False)
point_inflection = vlookup(0,np.diff(y)[:2000],x[:2000],exact=False)
point_time = vlookup(min(-fullwas_i/x),(-fullwas_i/x),x,exact=False)

max_noret = np.where(np.diff(fullwas_i) == np.max(np.diff(fullwas_i)))[0][0]
no_return = vlookup(0,np.diff(fullwas_i)[0:max_noret],x,exact=False)

#plt.plot(x[1:],np.diff(y))
#plt.axvline(x=point_inflection,color='b',linestyle=':')
#plt.axhline(y=0,color='b')
#plt.title("1st derivative: proba")
#plt.show()
#  
#plt.plot(x[1:],np.diff(fullwas_i))
#plt.axvline(x=no_return,color='k',linestyle='--')
#plt.axhline(y=0,color='b')
#plt.title("1st derivative: t wasted")
#plt.show()
#
#plt.plot(x[1:],np.diff(-fullwas_i/x))
#plt.axvline(x=point_time,color='g',linestyle=':')
#plt.axhline(y=0,color='b')
#plt.title("1st derivative: t wasted (%)")
#plt.show()

plt.plot(x,y)
plt.axvline(x=inflac,color='r',linestyle='--',ymax=p)
plt.axvline(x=point_time,color='g',linestyle=':')
plt.axvline(no_return,color='k',linestyle='--')
plt.hlines(p,color='r',linestyle='--', xmin = -40, xmax=inflac+0.5)
plt.legend(['P(x)','P(x) = {}'.format(p),'Min % wasted time','Event Horizon'])
plt.title("Probability of not missing my bus depending on when I leave home")
plt.xlabel("Time before expected arrival (min)")
plt.ylabel("Probability of not missing")
plt.show()

plt.plot(x,fullwas_i)
plt.axvline(x=inflac,color='r',linestyle='--')
plt.axvline(x=point_time,color='g',linestyle=':')
plt.axvline(no_return,color='k',linestyle='--')
plt.legend(['Avg. wasted time','P(x) = {}'.format(p),'Min % wasted time','Event Horizon'])
plt.title("Average wasted time")
plt.xlabel("Time before expected arrival (min)")
plt.ylabel("Average wasted time")
plt.show()

plt.plot(x[:2000],(-fullwas_i/x)[:2000])
plt.axvline(x=inflac,color='r',linestyle='--')
plt.axvline(x=point_time,color='g',linestyle=':')
plt.axvline(no_return,color='k',linestyle='--')
plt.legend(['% wasted time','P(x) = {}'.format(p),'Min % wasted time','Event Horizon'])
plt.title("Average wasted time as %")
plt.xlabel("Time before expected arrival (min)")
plt.ylabel("Average wasted time %")
plt.show()
