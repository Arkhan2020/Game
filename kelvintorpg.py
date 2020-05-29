# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:11:15 2020

@author: CARLOS
"""
import math

def colortemperaturetorgb(kelvin):
    temp=kelvin/100
    if temp<66:
        r=255
        g=99.4708025861*math.log(kelvin/100)-161.1195681661
    
        if temp<=19:
            b=0
        else:
            b=138.5177312231*math.log(kelvin/100-10)-305.0447927307
    else:
        r=kelvin/100-60
        r=329.698727446*math.pow(kelvin/100-60,-0.1332047592)
        g=288.1221695283*math.pow(kelvin/100-60,-0.0755148492)
        b=255
    return (r,g,b)
        
        