import Ogre


def drawline(scnmgr,ini,fin):
    line=scnmgr.createManualObject("line")
    # we can update object later
    line.setDynamic(True)
    line.begin("BaseWhiteNoLighting", Ogre.RenderOperation.OT_LINE_STRIP )
    line.position(ini)
    line.position(fin)
    line.end()
    return line

def updateline(line,ini,fin):
    line.beginUpdate(0)
    line.position(ini)
    line.position(fin)
    line.end()

class LensFlare:

    def __init__(self,LightPosition,camera,SceneMgr):
        self.mSceneMgr=SceneMgr
        self.mCamera=camera
        self.mHidden=True
        self.createlensflare()
        self.setLightPosition(LightPosition)
        self.raydir=self.mLightPosition-self.mCamera.getDerivedPosition()
        self.ray=Ogre.Ray(self.mCamera.getDerivedPosition(),self.raydir)
        self.query=self.mSceneMgr.createRayQuery(self.ray)
        self.query.getSortByDistance()
    
    def __del__(self):
        self.mNode.detachObject(self.mHaloSet)
        self.mNode.detachObject(self.mBurstSet)
        self.mSceneMgr.destroyBillboardSet(self.mHaloSet)
        self.mSceneMgrdestroyBillboardSet(self.mBurstSet)

    def createlensflare(self):
        self.LF_scale = 2000;
        
        self.line=None
    
     	# -----------------------------------------------------
        # We create 2 sets of billboards for the lensflare
        # -----------------------------------------------------
        self.mHaloSet = self.mSceneMgr.createBillboardSet("halo")
        self.mHaloSet.setMaterialName("lensflare/halo")
        self.mHaloSet.setCullIndividually(True)
        self.mHaloSet.setQueryFlags(0)	# They should not be detected by rays.
        self.mHaloSet.setRenderQueueGroup(Ogre.RENDER_QUEUE_9)
        self.mBurstSet= self.mSceneMgr.createBillboardSet("burst")
        self.mBurstSet.setMaterialName("lensflare/burst")
        self.mBurstSet.setCullIndividually(True)
        self.mBurstSet.setQueryFlags(0)
        self.mBurstSet.setRenderQueueGroup(Ogre.RENDER_QUEUE_9)
        
        #The node is located at the light source.
        self.mNode  = self.mSceneMgr.getRootSceneNode().createChildSceneNode()
        self.mNode.attachObject(self.mBurstSet)
        self.mNode.attachObject(self.mHaloSet)
        
        #Creation of the Halo billboards
        self.LF_Halo1 = self.mHaloSet.createBillboard(0,0,0)
        self.LF_Halo1.setDimensions(self.LF_scale*0.5,self.LF_scale*0.5)
        self.LF_Halo2 = self.mHaloSet.createBillboard(0,0,0)
        self.LF_Halo2.setDimensions(self.LF_scale,self.LF_scale)
        self.LF_Halo3 = self.mHaloSet.createBillboard(0,0,0)
        self.LF_Halo3.setDimensions(self.LF_scale*0.25,self.LF_scale*0.25)
        
        #Creation of the "Burst" billboards
        self.LF_Burst1 = self.mBurstSet.createBillboard(0,0,0)
        self.LF_Burst1.setDimensions(self.LF_scale*0.25,self.LF_scale*0.25)
        self.LF_Burst2 = self.mBurstSet.createBillboard(0,0,0)
        self.LF_Burst2.setDimensions(self.LF_scale*0.5,self.LF_scale*0.5)
        self.LF_Burst3 = self.mBurstSet.createBillboard(0,0,0)
        self.LF_Burst3.setDimensions(self.LF_scale*0.25,self.LF_scale*0.25)
 


         #-------------------------------------------------------------------------- */
         #This function updates the lensflare effect. 
         #This function should be called by your frameListener.
         #
         #-------------------------------------------------------------------------- */
 
    def drawray(self):
        if self.line==None:
            linenode=self.mSceneMgr.getRootSceneNode().createChildSceneNode()
            self.line=drawline(self.mSceneMgr,self.mLightPosition,self.mCamerapos)    
            linenode.attachObject(self.line)
        else:
            updateline(self.line,self.mLightPosition,self.mCamerapos)
    
    def update(self):
         #If the Light is out of the Camera field Of View, the lensflare is hidden.
        if (not self.mCamera.isVisible(self.mLightPosition)):
             self.mHaloSet.setVisible(False);
             self.mBurstSet.setVisible(False)
             return
        else:
             self.mCamerapos=self.mCamera.getDerivedPosition()
             self.raydir=self.mLightPosition-self.mCamerapos
             #self.raydir.normalise()
             #updateline(self.line,self.mLightPosition,self.mCamerapos)
             self.ray=Ogre.Ray(self.mCamerapos,self.raydir)
             self.query.setRay(self.ray)
             #self.query.clearResults()
             if len(self.query.execute())>1:
                 #print (self.query.getLastResults()[0].movable.getName())
                 #self.query.getLastResults()[0].movable.setVisible(False)
                 #self.query.getLastResults()[0].movable.getParentSceneNode().showBoundingBox(True) 
                 self.mHaloSet.setVisible(False);
                 self.mBurstSet.setVisible(False)
                 return
             self.mHaloSet.setVisible(True)
             self.mBurstSet.setVisible(True)
             
        self.LightDistance  = self.mLightPosition.distance(self.mCamerapos)
        #self.CameraVect  = self.mCamera.getDirection() # normalized vector (length 1)
        #self.CameraVect = self.mCamera.getPosition() + (self.LightDistance * self.CameraVect)
        
        #self.LightDistance  = self.mLightPosition.distance(self.camnode.getDerivedPosition())
        
        #self.mSceneMgr.destroyQuery(query)
        self.CameraVect = self.mCamera.getDerivedOrientation() * Ogre.Vector3(0, 0, -1)# normalized vector (length 1)
        self.CameraVect = self.mCamerapos + ( self.CameraVect *self.LightDistance)                


        
        #The LensFlare effect takes place along this vector.
        self.LFvect = (self.CameraVect - self.mLightPosition)
        self.LFvect += Ogre.Vector3(-64,-64,0)  # sprite dimension (to be adjusted, but not necessary)

        #The different sprites are placed along this line.
        self.mHaloSet.getBillboard(0).setPosition(self.LFvect*0.500)
        self.mHaloSet.getBillboard(1).setPosition( self.LFvect*0.125)
        self.mHaloSet.getBillboard(2).setPosition(-self.LFvect*0.250)
        self.mBurstSet.getBillboard(0).setPosition( self.LFvect*0.333)
        self.mBurstSet.getBillboard(1).setPosition(-self.LFvect*0.500)
        self.mBurstSet.getBillboard(2).setPosition(-self.LFvect*0.180)

        #We redraw the lensflare (in case it was previouly out of the camera field, and hidden)
        self.setVisible(True)   

    def setVisible(self,visible):
        self.mHaloSet.setVisible(visible)
        self.mBurstSet.setVisible(visible)
        self.mHidden = not visible


# /* ------------------------------------------------------------------------- */
# /// This function updates the light source position. 
# /** This function can be used if the light source is moving.*/
# /* ------------------------------------------------------------------------- */

    def setLightPosition(self,pos):
        self.mLightPosition = pos
        self.mNode.setPosition(self.mLightPosition) 

# /* ------------------------------------------------------------------------- */
# /// This function changes the colour of the burst. 
# /* ------------------------------------------------------------------------- */
    def setBurstColour(self,color):
        self.mBurstSet.getBillboard(0).setColour(color)
        self.mBurstSet.getBillboard(1).setColour(color*0.8)
        self.mBurstSet.getBillboard(2).setColour(color*0.6)
 
# /* ------------------------------------------------------------------------- */
# /// This function changes the colour of the halos. 
# /* ------------------------------------------------------------------------- */
    def setHaloColour(self,color):
        self.mHaloSet.getBillboard(0).setColour(color*0.8)
        self.mHaloSet.getBillboard(1).setColour(color*0.6)
        self.mHaloSet.getBillboard(2).setColour(color)