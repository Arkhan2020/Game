#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 23:09:18 2020

@author: arky
"""
import Lensflare, Ogre

class NightSky:
    def __init__(self,scn_mgr,moonpos,cam):
        #skybox and distance of the skybox
        #scn_mgr.setSkyDome(True,"Skyes/Night1",50,5)
        scn_mgr.setSkyBox(True,"Skyes/NightSkyBox",100)
        #scn_mgr.setSkyDome(True,"Examples/SpaceSkyPlane",5,8)

        #lets set a fog
        #Fadecolor=Ogre.ColourValue(0,0,0)
        #vp.setBackgroundColour(Fadecolor)
        #scn_mgr.setFog(Ogre.Ogre.FOG_LINEAR,Fadecolor,0,600,900)

        scn_mgr.setAmbientLight(Ogre.ColourValue(.1, .1, .1))
        
        dirlight=scn_mgr.createLight("MoonLight1")
        dirlight.setType(Ogre.Light.LT_DIRECTIONAL);
        dirlight.setDiffuseColour(Ogre.ColourValue(0, .1, .7));
        dirlight.setSpecularColour(Ogre.ColourValue(0, 0, .5))
        #dirlight.setDirection(-0.5, -0.5, -0.3)
        dirlight.setDirection(moonpos*-1)
        
        moon= scn_mgr.createBillboardSet("Moon")
        moon.setMaterialName("Skyes/Moon")
        moon.setDefaultDimensions(2000,2000)
        #self.mBurstSet.setCullIndividually(True)
        #self.mBurstSet.setQueryFlags(0)
        moonNode  = scn_mgr.getRootSceneNode().createChildSceneNode()
        moonboard = moon.createBillboard(moonpos)
        #moonboard.setDimensions(1,1)

        moonNode.attachObject(moon)
        moonNode.setPosition(0, 1, 1)
        #lens flare
        self.lensflare = Lensflare.LensFlare(moonpos,cam, scn_mgr)
    
    def update(self):
        self.lensflare.update()
        