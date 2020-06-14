#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 22:41:44 2020

@author: arky

se definen los distintos tipos de colisiones del mapa
"""

def solid(objeto,x,y):
    #objeto con el que chocamos y posición del tile en el mapa
    #devuelvo la altura del objeto
    return 2.0

def nocollision(objeto,x,y):
    return -2

def stair1_N(objeto,x,y):
    dy=y-int(y)
    return (0.5*dy)
def stair1_S(objeto,x,y):
    dy=y-int(y)
    return (0.5*(1-dy))
def stair1_E(objeto,x,y):
    dx=x-int(x)
    return (0.5*dx)
def stair1_O(objeto,x,y):
    dx=x-int(x)
    return (0.5*(1-dx))

def stair2_N(objeto,x,y):
    dy=y-int(y)
    return (0.5*dy+0.5)
def stair2_S(objeto,x,y):
    dy=y-int(y)
    return (0.5*(1-dy)+0.5)
def stair2_E(objeto,x,y):
    dx=x-int(x)
    return (0.5*dx+0.5)
def stair2_O(objeto,x,y):
    dx=x-int(x)
    return (0.5*(1-dx)+0.5)

def stair3_N(objeto,x,y):
    dy=y-int(y)
    return (0.5*dy+1)
def stair3_S(objeto,x,y):
    dy=y-int(y)
    return (0.5*(1-dy)+1)
def stair3_E(objeto,x,y):
    dx=x-int(x)
    return (0.5*dx+1)
def stair3_O(objeto,x,y):
    dx=x-int(x)
    return (0.5*(1-dx)+1)

def stair4_N(objeto,x,y):
    dy=y-int(y)
    return (0.5*dy+1.5)
def stair4_S(objeto,x,y):
    dy=y-int(y)
    return (0.5*(1-dy)+1.5)
def stair4_E(objeto,x,y):
    dx=x-int(x)
    return (0.5*dx+1.5)
def stair4_O(objeto,x,y):
    dx=x-int(x)
    return (0.5*(1-dx)+1.5)

def landing1(objeto,x,y):
    return 0.5

def landing2(objeto,x,y):
    return 1

def landing3(objeto,x,y):
    return 1.5

#
#   ESCALERAS DE CARACOL
#


def hescalon(tan):
    if tan<0.5:
        return 0.16
    elif tan<1: 
        return 0.32
    elif tan<1.5:
        return 0.48
    else:
        return 0.64

def spiralstair1_SA(objeto,x,y): #
    dx=x-int(x)
    dy=y-int(y)
    print ("espiral1N",dy,"-",dx,"=",hescalon(dy/dx))
    return hescalon(dy/dx)

def spiralstair1_EA(objeto,x,y):#
    dx=x-int(x)
    dy=y-int(y)
    print ("espiral1E",dy,"-",dx,"=",hescalon(((dy)/(1-dx))))
    return hescalon(((dy)/(1-dx)))

def spiralstair1_NA(objeto,x,y):
    dx=x-int(x)
    dy=y-int(y)
    print ("espiral1S",dy,"-",dx,"=",hescalon((1-dy)/(1-dx)))
    return hescalon((1-dy)/(1-dx))

def spiralstair1_OA(objeto,x,y):
    dx=x-int(x)
    dy=y-int(y)
    print ("espiral1O",dy,"-",dx,"=",hescalon((1-dx)/(dy)))
    return hescalon((1-dx)/(dy))

def spiralstair2_SA(objeto,x,y): #
    dx=x-int(x)
    dy=y-int(y)
    print ("espiral2N",dy,"-",dx,"=",hescalon(dy/dx))
    return hescalon(dy/dx)+0.66

def spiralstair2_EA(objeto,x,y):#
    dx=x-int(x)
    dy=y-int(y)
    return hescalon(((dy)/(1-dx)))+0.66

def spiralstair2_NA(objeto,x,y):
    dx=x-int(x)
    dy=y-int(y)
    return hescalon((1-dy)/(1-dx))+0.66

def spiralstair2_OA(objeto,x,y):
    dx=x-int(x)
    dy=y-int(y)
    return hescalon((1-dx)/(dy))+0.66

def spiralstair3_SA(objeto,x,y): #
    dx=x-int(x)
    dy=y-int(y)
    return hescalon(dy/dx) + 1.32

def spiralstair3_EA(objeto,x,y):#
    dx=x-int(x)
    dy=y-int(y)
    return hescalon(((dy)/(1-dx)))+1.32

def spiralstair3_NA(objeto,x,y):
    dx=x-int(x)
    dy=y-int(y)
    return hescalon((1-dy)/(1-dx))+1.32

def spiralstair3_OA(objeto,x,y):
    dx=x-int(x)
    dy=y-int(y)
    return hescalon((1-dx)/(dy))+1.32


ROT_DIR={"90":"E","180":"S","270":"O","0":"N"}
COLISION_TYPE = {"NP":solid,"":nocollision,
                 "E1N":stair1_N,"E1S":stair1_S,"E1E":stair1_E,"E1O":stair1_O,
                 "E2N":stair2_N,"E2S":stair2_S,"E2E":stair2_E,"E2O":stair2_O,
                 "E3N":stair3_N,"E3S":stair3_S,"E3E":stair3_E,"E3O":stair3_O,
                 "E4N":stair4_N,"E4S":stair4_S,"E4E":stair4_E,"E4O":stair4_O,
                 #"SS1N":spiralstair1_EA,"SS1E":spiralstair1_SA,"SS1S":spiralstair1_OA,"SS1O":spiralstair1_NA,
                 #"SS2N":spiralstair2_EA,"SS2E":spiralstair2_SA,"SS2S":spiralstair2_OA,"SS2O":spiralstair2_NA,
                 #"SS3N":spiralstair3_EA,"SS3E":spiralstair3_SA,"SS3S":spiralstair3_OA,"SS3O":spiralstair3_NA,
  #               "SS4N":spiralstair4_NA,"SS4E":spiralstair4_SA,"SS4S":spiralstair4_EA,"SS4O":spiralstair4_SA,
                  "SS1":landing1, "SS2":landing2, "SS3":landing3,
                  "L1":landing1, "L2":landing2, "L3":landing3}

class collision_tiles:    
    def createtiles(self,tilelist):
        self.collisiontypes={0:COLISION_TYPE[""]}
        
        for gid in tilelist.keys():
            if "Collision" in tilelist[gid].properties:
                colprop=tilelist[gid].properties["Collision"]
                if colprop in COLISION_TYPE:
                    self.collisiontypes[gid]=COLISION_TYPE[colprop]
                else:
                    colprop=tilelist[gid].properties["Collision"] + ROT_DIR[tilelist[gid].properties["RefAngle"]]
                    if colprop in COLISION_TYPE:
                        self.collisiontypes[gid]=COLISION_TYPE[colprop]
                    else:
                        self.collisiontypes[gid]=COLISION_TYPE[""]
            else:
                self.collisiontypes[gid]=COLISION_TYPE[""]
                
                

            
