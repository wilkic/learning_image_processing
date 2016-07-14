#!/usr/bin/env python

import ipdb


from SimpleCV import Image, Color, Display

img = Image('/home/acp/Projects/ggp/cam_images/camera1/spot2_occupied.jpg')

feats = img.findKeypoints()

feats.draw(color=Color.RED)

img.show()

output = img.applyLayers()

output.save('keyFeats.png')

