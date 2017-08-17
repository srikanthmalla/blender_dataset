import bpy
from bpy import context
from math import sin, cos, radians
import random as rand
import time
#Output resolution (Stereoscopic images & depthmap)
bpy.context.scene.render.resolution_x = 1000
bpy.context.scene.render.resolution_y = 1000
 
ii = 1
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links 
# clear default nodes
for n in tree.nodes:
    tree.nodes.remove(n)

#setup camera:
camera = bpy.data.objects['Camera']
camera.select = True
camera.rotation_mode = 'XYZ'
#angle1 = 1.3 + (0.5-rand.random())*1.5
#angle2 = (0.5-rand.random())*1.5
#angle3 = 0.75 + (0.5-rand.random())*1.5
camera.rotation_euler = (0, 0, 0.2)
Cam_x = 0 
Cam_y=0
#Cam_y = -3 + (0.5-rand.random())*3
Cam_z =5
# 3 + (0.5-rand.random())*3
camera.location = (Cam_x,Cam_y,Cam_z)
camera.data.stereo.convergence_distance = 10000
camera.data.lens = 15 #(focal length)
#camera.data.stereo.interocular_distance = 0.3
#dist = ((camera.location[0]-(-3.22))**(2)+(camera.location[1]-(8.0))**(2)+(camera.location[2]-(-5.425))**(2))**(1/2)
camera.select = False


##################
#Create new scene:
##################

scene = bpy.context.scene
scene.render.use_multiview = True
scene.render.views_format = 'STEREO_3D'
rl = tree.nodes.new(type="CompositorNodeRLayers")
composite = tree.nodes.new(type = "CompositorNodeComposite")
composite.location = 200,0

scene = bpy.context.scene

#setup the depthmap calculation using blender's mist function:
scene.render.layers['RenderLayer'].use_pass_mist = True
#the depthmap can be calculated as the distance between objects and camera ('LINEAR'), or square/inverse square of the distance ('QUADRATIC'/'INVERSEQUADRATIC'):
scene.world.mist_settings.falloff = 'LINEAR'
#minimum depth:
scene.world.mist_settings.start=0.0
scene.world.mist_settings.intensity = 0.0
#maximum depth (can be changed depending on the scene geometry to normalize the depth map whatever the camera orientation and position is):
dist=10
scene.world.mist_settings.depth = dist
print(dist)


#################
#Render the scene
#################

#ouput the depthmap:
#links.new(rl.outputs['Mist'],composite.inputs['Image'])

#scene.render.use_multiview = False

#scene.render.filepath = 'DepthMap_'+str(ii)+'.png'
#bpy.ops.render.render( write_still=True ) 
#time.sleep(0.2)
#output the stereoscopic images:
links.new(rl.outputs['Image'],composite.inputs['Image'])

scene.render.use_multiview = False

scene.render.filepath = 'Stereoscopic_'+str(ii)+'.png'
bpy.ops.render.render( write_still=True ) 
#time.sleep(0.2)