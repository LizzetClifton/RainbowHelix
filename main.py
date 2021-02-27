import maya.cmds as mc
import math
import random

#this function takes our old sin range of -1 to 1 and changes it to 0 to 1 because we need 0 to 1 for our rgb. 
#using this, we will have an even distribution of colors in our ring, then we apply sin
def reRange(oldValue):
    oldRange = 2
    newRange = 1
    newValue = (oldValue+1)/2
    return newValue

def getSin(x):
    return math.sin(math.radians(x))

distanceX = 1

for i in range(72):
    #get RGB values using i
    r1=reRange(getSin(i*5))
    g1=reRange(getSin(i*5+120))
    b1=reRange(getSin(i*5+240))
    
    #slightly offset the i value by 10 so our medium spheres are different colors
    r2=reRange(getSin((i+10)*5))
    g2=reRange(getSin((i+10)*5+120))
    b2=reRange(getSin((i+10)*5+240))
    
    #slightly offset the i value by 20 so our small spheres are different colors
    r3=reRange(getSin((i+20)*5))
    g3=reRange(getSin((i+20)*5+120))
    b3=reRange(getSin((i+20)*5+240))
    
    #create three polySpheres arranged in a horizontally planar triangle
    #make second and third sphere a little smaller
    
    #create a variable to randomize radius of the spheres we're about to create
    rad1=random.uniform(-0.75, 0.75)
    rad2=random.uniform(-0.5, 0.5)
    rad3=random.uniform(-0.25, 0.25)
    
    #first sphere
    mc.polySphere(n="sphere_a_"+str(i), r=1.5+rad1)
    mc.move(distanceX, 0, 0)
    #use the RGB color values from above
    mc.polyColorPerVertex(rgb=(r1, g1, b1), cdo=True)
    
    #second sphere
    mc.polySphere(n="sphere_b_"+str(i), r=0.75+rad2)
    #rotate the sphere 120 degrees on the Y axis
    mc.rotate(0, 120, 0, r=True, ws=True)
    #move it in object space
    mc.move(distanceX*3, 0, 0, os=True)
    #use the RGB color values from above
    mc.polyColorPerVertex(rgb=(r2, g2, b2), cdo=True)
    
    #third sphere
    mc.polySphere(n="sphere_c_"+str(i), r=0.5+rad3)
    mc.rotate(0, 240, 0, r=True, ws=True)
    mc.move(distanceX*6, 0, 0, os=True)
    #use the RGB color values from above
    mc.polyColorPerVertex(rgb=(r3, g3, b3), cdo=True)
    
    #group the spheres and give the group a unique name
    mc.select("sphere_a_"+str(i), "sphere_b_"+str(i), "sphere_c_"+str(i), replace=True)
    mc.group(n="group_a_"+str(i))
     
    #rotate the group 45*i degrees in y and freeze transformation and set its current values as default 0
    #this gives the spiral look
    mc.rotate(0, (45*i), 0, r=True, os=True)
    mc.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
    
    #experimenting with expressions here
    #mc.expression(s="sphere_a_"+str(i)+".translateX=sin(time/2)", o="sphere_a_"+str(i))
    #mc.expression(s="sphere_b_"+str(i)+".translateX=-sin(time/2); sphere_b_"+str(i)+".translateZ=-sin(time/2)", o="sphere_b_"+str(i))
    mc.expression(s="sphere_c_"+str(i)+".translateX=-sin(time/2); sphere_c_"+str(i)+".translateZ=sin(time/2)", o="sphere_c_"+str(i))
   
    
    #move the group 10 units in x
    mc.move(12, 0, 0)
    
    #apply an expression to the group to spin it. the modulus is used here because we are grouping our spheres to have different speeds
    if i%5==0:
        mc.expression(s="group_a_"+str(i)+".rotateY=time*20;", o="group_a_"+str(i), ae=True, uc="all")
        #mc.expression(s="sphere_c_"+str(i)+".translateX=time*(time%5)", o="sphere_c_"+str(i), ae=True, uc="all")
    #elif i%5==1:
        #mc.expression(s="sphere_c_"+str(i)+".translateX=-time*(time%5)", o="sphere_c_"+str(i), ae=True, uc="all")
    else:
        mc.expression(s="group_a_"+str(i)+".rotateY=time*5;", o="group_a_"+str(i), ae=True, uc="all")
        #mc.expression(s="sphere_c_"+str(i)+".translateX=-time*(time%5)", o="sphere_c_"+str(i), ae=True, uc="all")
    
    #create a new group. This gives us a parent pivot at the origin. Use a unique name
    mc.group(empty=True, n="group_b_"+str(i))
    
    #make new group parent of old group
    mc.select("group_a_"+str(i), r=True)
    mc.select("group_b_"+str(i), tgl=True)
    mc.parent()
    
    #select parent group and rotate (5*i) degrees in z
    mc.select("group_b_"+str(i), r=True)
    mc.rotate(0, 0, (5*i), r=True, os=True)
