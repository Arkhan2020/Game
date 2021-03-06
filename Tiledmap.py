#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:05:57 2020

@author: arky
"""

import sys

def trace(frame, event, arg):
    #print(f"[{event}] {frame.f_code.co_filename}:{frame.f_lineno}")
    return trace

sys.settrace(trace)

import Ogre
import Ogre.RTShader as OgreRTShader
import Ogre.Bites as OgreBites
import os.path
import Ogretmxmap
import Ogre.Overlay as OgreOverlay
import Player
import Skyefect

def gettilepos(vector):
    return [vector.x,vector.z]


RGN_MESHVIEWER = "OgreMeshViewer"


class Game(OgreBites.ApplicationContext, OgreBites.InputListener):
    def __init__(self):
        OgreBites.ApplicationContext.__init__(self, "Titulo de la ventana")
        OgreBites.InputListener.__init__(self)
        #self.pos=Ogre.Vector3(-1,1.5,0) #altura 1.80m
        self.LINEAL_VEL=5
        self.ANGULAR_VEL=1

        self.show_about = False

    def draw_about(self):
        flags = OgreOverlay.ImGuiWindowFlags_AlwaysAutoResize
        self.show_about = OgreOverlay.Begin("About TiledMap", True, flags)[1]
        OgreOverlay.Text("By arky")
        OgreOverlay.Text("TiledMap is licensed under the MIT License, see LICENSE for more information.")
        OgreOverlay.Separator()
        OgreOverlay.BulletText(f"Ogre: {Ogre.__version__}")
        OgreOverlay.BulletText(f"imgui: {OgreOverlay.GetVersion()}")
        OgreOverlay.End()


#    def frameStarted(self, evt):
#        return True
#        OgreBites.ApplicationContext.frameStarted(self, evt)
#
#        if not self.cam.getViewport().getOverlaysEnabled():
#            return True
#
#        ImGuiOverlay.NewFrame(evt)

    def locateResources(self):

        self.rescfg= os.path.basename("./resources.cfg")
        self.meshdir = os.path.dirname("./resources.cfg")

        rgm = Ogre.ResourceGroupManager.getSingleton()
        # ensure our resource group is separate, even with a local resources.cfg
        rgm.createResourceGroup(RGN_MESHVIEWER, False)

        # use parent implementation to locate system-wide RTShaderLib
        OgreBites.ApplicationContext.locateResources(self)

        # allow override by local resources.cfg
        if not self.getFSLayer().fileExists(self.rescfg):
            # we use the fonts from SdkTrays.zip
            trays_loc = self.getDefaultMediaDir()+"/packs/SdkTrays.zip"
            rgm.addResourceLocation(trays_loc, "Zip", RGN_MESHVIEWER)

        if self.rescfg:
            cfg = Ogre.ConfigFile()
            cfg.loadDirect(self.rescfg)

            for sec, settings in cfg.getSettingsBySection().items():
                for kind, loc in settings.items():
                    rgm.addResourceLocation(loc, kind, sec)

        # explicitly add mesh location to be safe
        if not rgm.resourceLocationExists(self.meshdir, Ogre.RGN_DEFAULT):
            rgm.addResourceLocation(self.meshdir, "FileSystem", Ogre.RGN_DEFAULT)


    def setup(self):
        # SETUP es la primera función a la que se llama
        # Primero llamamos a la base y ponemos el listener
        OgreBites.ApplicationContext.setup(self)
        #Ahora se llama a locate resources
        self.addInputListener(self)
        #imgui_overlay = ImGuiOverlay()

        self.restart = False

        imgui_overlay = OgreOverlay.ImGuiOverlay()
        OgreOverlay.GetIO().IniFilename = self.getFSLayer().getWritablePath("imgui.ini")

        #Inicializamos ogre u hacemos un puntero a Root
        root = self.getRoot()
        #self.getRoot().getRenderSystem().clearFrameBuffer(1.0)

        #Creamos el scene manager
        scn_mgr = root.createSceneManager()
        scn_mgr.addRenderQueueListener(self.getOverlaySystem())
        self.scn_mgr = scn_mgr

        imgui_overlay.show()
        OgreOverlay.OverlayManager.getSingleton().addOverlay(imgui_overlay)
        imgui_overlay.disown() # owned by OverlayMgr now


        # Creamos el Shader y definimos las sombras
        shadergen = OgreRTShader.ShaderGenerator.getSingleton()
        shadergen.addSceneManager(scn_mgr)
        scn_mgr.setShadowTechnique(Ogre.Ogre.SHADOWTYPE_TEXTURE_MODULATIVE)
        #scn_mgr.setShadowTechnique(Ogre.Ogre.SHADOWTYPE_TEXTURE_ADDITIVE)
        #scn_mgr.setShadowTechnique(Ogre.Ogre.SHADOWTYPE_STENCIL_MODULATIVE)
        scn_mgr.setShadowDirLightTextureOffset(1)
        scn_mgr.setShadowFarDistance(200)
        #para que los objetos emitan shadow sobre si mismos
        scn_mgr.setShadowTextureSelfShadow(True)
        
        #Creamos el mapa
        #mapa=Ogretmxmap.tmxmap("Maps/cathedral.tmx")
        mapa=Ogretmxmap.tmxmap("resources/tiled/cathedral.tmx")
        mannode=scn_mgr.getRootSceneNode().createChildSceneNode()
        mannode.setPosition(0,0,0)
        mapa.createmap(scn_mgr)


        # Vamos a crear el nodo perteneciente al personaje
        Playernode=scn_mgr.getRootSceneNode().createChildSceneNode()
        #Playernode.setPosition(self.pos)
        self.Playernode=Playernode
        # Creo el player y lo fusiono con su nodo
        self.Player=Player.Player(Playernode)
        self.Player.mapa=mapa
        self.Player.setpos(10,10,0)


        # Creamos la camara y la posicionamos en el personaje
        camNode = Playernode.createChildSceneNode()
        camNode.setPosition(0,1.5,0)
        self.cam = scn_mgr.createCamera("MainCam")
        #camNode.setPosition(0, 0, 80)
        camNode.lookAt(Ogre.Vector3(300, 1.5, 0), Ogre.Node.TS_WORLD)
        self.cam.setNearClipDistance(.2)
        camNode.attachObject(self.cam)
        vp = self.getRenderWindow().addViewport(self.cam)
        vp.setBackgroundColour(Ogre.ColourValue(0, 0, 0))
        self.cam.setAspectRatio((vp.getActualWidth()) / (vp.getActualHeight()))
        self.camNode=camNode

        # Setup the scene
        #night light
        self.Sky=Skyefect.NightSky(scn_mgr,Ogre.Vector3(1500,3000,10000),self.cam)
        self.Sky.lensflare.drawray()
        
        # Creamos una pointlight sobre el player
        pointLight = scn_mgr.createLight("PointLight")
        pointLight.setType(Ogre.Light.LT_POINT)
        pointLight.setDiffuseColour(1, 1, 1)
        pointLight.setSpecularColour(1, 1, 1)
        pointLightNode = Playernode.createChildSceneNode()
        pointLightNode.attachObject(pointLight)
        pointLightNode.setPosition(0, 1.5, 0)
        pointLight.setAttenuation(100,1,0.045,0.0075)
        
        #Daylight, esta tecnica de sombreado queda mucho mejor
#        scn_mgr.setShadowTechnique(Ogre.Ogre.SHADOWTYPE_TEXTURE_ADDITIVE)
#        scn_mgr.setAmbientLight(Ogre.ColourValue(.2, .2, .2))
#        light=scn_mgr.createLight("MainLight")
#        light.setType(Ogre.Light.LT_DIRECTIONAL);
#        light.setDiffuseColour(Ogre.ColourValue(.6, .6, 1));
#        light.setSpecularColour(Ogre.ColourValue(.6, .6, 1))
#        light.setDirection(1, -0.5, 0.5)


#        lightNode = scn_mgr.getRootSceneNode().createChildSceneNode()
#        lightNode.attachObject(light)
#        lightNode.setPosition(0, 3, 0)

        self.mapa=mapa

        self.cam.getViewport().setOverlaysEnabled(True)
        #self.mtraymanager=OgreBites.TrayManager("Interface",self.getRenderWindow())
        #self.mtraymanager.createLabel(OgreBites.TL_TOP,"TInfo","",350)

        self.imgui_input = OgreBites.ImGuiInputListener()
        self.input_dispatcher = OgreBites.InputListenerChain([self.imgui_input])
        self.addInputListener(self.input_dispatcher)

    def frameStarted(self, evt):
        OgreBites.ApplicationContext.frameStarted(self, evt)

        if not self.cam.getViewport().getOverlaysEnabled():
            return True

        self.time=evt.timeSinceLastFrame
        self.Player.actualiza(self.time)
        self.Sky.update()

        OgreBites.ApplicationContext.frameStarted(self, evt)

        OgreOverlay.ImGuiOverlay.NewFrame(evt)

        if OgreOverlay.BeginMainMenuBar():

            if OgreOverlay.BeginMenu("Help"):
                if OgreOverlay.MenuItem("About"):
                    self.show_about = True
                OgreOverlay.EndMenu()

            OgreOverlay.EndMainMenuBar()

        if self.show_about:
            self.draw_about()

        return True


    def keyPressed(self, evt):
            if evt.keysym.sym == OgreBites.SDLK_ESCAPE:
                self.getRoot().queueEndRendering()

            if evt.keysym.sym == OgreBites.SDLK_DOWN:
                self.Player.keydown=True
            if evt.keysym.sym == OgreBites.SDLK_UP:
                self.Player.keyup=True
            if evt.keysym.sym == OgreBites.SDLK_LEFT:
                self.Player.keyleft=True
            if evt.keysym.sym == OgreBites.SDLK_RIGHT:
                self.Player.keyright=True
            if evt.keysym.sym == OgreBites.SDLK_SPACE:
                self.Player.jump()
            
            if evt.keysym.sym == OgreBites.SDLK_RETURN:
                self.Sky.lensflare.drawray()


            if evt.keysym.sym == OgreBites.SDLK_PAGEDOWN:
                self.camNode.pitch(Ogre.Ogre.Radian(-self.time*self.ANGULAR_VEL),Ogre.Ogre.Node.TS_LOCAL)

            if evt.keysym.sym == OgreBites.SDLK_PAGEUP:
                self.camNode.pitch(Ogre.Ogre.Radian(self.time*self.ANGULAR_VEL),Ogre.Ogre.Node.TS_LOCAL)

            return True

    def keyReleased(self, evt):
            if evt.keysym.sym == OgreBites.SDLK_DOWN:
                self.Player.keydown=False
            if evt.keysym.sym == OgreBites.SDLK_UP:
                self.Player.keyup=False
            if evt.keysym.sym == OgreBites.SDLK_LEFT:
                self.Player.keyleft=False
            if evt.keysym.sym == OgreBites.SDLK_RIGHT:
                self.Player.keyright=False

            return True

    def mousePressed(self, evt):
        return True

    def shutdown(self):
        OgreBites.ApplicationContext.shutdown(self)

        if self.restart:
            # make sure empty rendersystem is written
            self.getRoot().shutdown()
            self.getRoot().setRenderSystem(None)



if __name__ == "__main__":

    app = Game()

    while True: # allow auto restart
        app.initApp()
        app.getRoot().startRendering()
        app.closeApp()

        if not app.restart: break

