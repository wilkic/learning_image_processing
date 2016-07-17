
import os

import numpy as np
import matplotlib.pyplot as plt
import cv2

import json
import pprint as pp

import ipdb



plt.close("all")



camera1 = {
    'number': 1,
    'im_full_path': '/home/acp/work/ggp/cam_images/camera1/snap20160705224323.jpg',
    'spots': [
        {
            'number': 1,
            'vertices': np.array(
                        [[   0,   0],
                         [  30,   0],
                         [  60, 150],
                         [   0, 150]]),
            'base_means': [118,123,127],
            'base_nEdges': 404,
            'base_nKeys': 11
        },
        {
            'number': 2,
            'vertices': np.array(
                        [[  90,   0],
                         [ 290,   0],
                         [ 230, 224],
                         [ 110, 224]]),
            'base_means': [117,117,115],
            'base_nEdges': 419,
            'base_nKeys': 18
        },
        {
            'number': 3,
            'vertices': np.array(
                        [[ 310,   0],
                         [ 400,   0],
                         [ 400, 224],
                         [ 250, 224]]),
            'base_means': [119,119,117],
            'base_nEdges': 479,
            'base_nKeys': 3
        }
    ]
}

camera2 = {
    'number': 2,
    'im_full_path': '/home/acp/work/ggp/cam_images/camera2/snap20160706230618.jpg',
    'spots': [
        {
            'number': 4,
            'vertices': np.array(
                        [[ 215,   0],
                         [ 370,   0],
                         [ 400, 100],
                         [ 400, 224],
                         [ 210, 224]]),
            'base_means': [126,126,125],
            'base_nEdges': 121,
            'base_nKeys': 4
        },
        {
            'number': 5,
            'vertices': np.array(
                        [[  50,   0],
                         [ 200,   0],
                         [ 195, 224],
                         [   0, 224],
                         [   0, 170]]),
            'base_means': [130,130,131],
            'base_nEdges': 652,
            'base_nKeys': 35
        }
    ]
}

camera3 = {
    'number': 3,
    'im_full_path': '/home/acp/work/ggp/cam_images/camera3/snap20160705224324.jpg',
    'spots': [
        {
            'number': 6,
            'vertices': np.array(
                        [[ 280,   0],
                         [ 380,   0],
                         [ 400,  35],
                         [ 400, 224],
                         [ 330, 224]]),
            'base_means': [102,102,101],
            'base_nEdges': 4,
            'base_nKeys': 1
        },
        {
            'number': 7,
            'vertices': np.array(
                        [[ 130,   0],
                         [ 265,   0],
                         [ 310, 224],
                         [ 105, 224]]),
            'base_means': [122,123,121],
            'base_nEdges': 152,
            'base_nKeys': 11
        },
        {
            'number': 8,
            'vertices': np.array(
                        [[  20,   0],
                         [ 115,   0],
                         [  85, 224],
                         [   0, 224],
                         [   0,  40]]),
            'base_means': [137,137,140],
            'base_nEdges': 730,
            'base_nKeys': 43
        },
    ]
}

camera4 = {
    'number': 4,
    'im_full_path': '/home/acp/work/ggp/cam_images/camera4/snap20160706230618.jpg',
    'spots': [
        {
            'number': 9,
            'vertices': np.array(
                        [[ 275,  30],
                         [ 335,  30],
                         [ 400, 115],
                         [ 400, 224],
                         [ 390, 224]]),
            'base_means': [120,121,119],
            'base_nEdges': 67,
            'base_nKeys': 2
        },
        {
            'number': 10,
            'vertices': np.array(
                        [[ 165,  30],
                         [ 260,  30],
                         [ 370, 224],
                         [ 240, 224]]),
            'base_means': [121,122,119],
            'base_nEdges': 67,
            'base_nKeys': 2
        },
        {
            'number': 11,
            'vertices': np.array(
                        [[  40,  30],
                         [ 150,  30],
                         [ 220, 224],
                         [  40, 224]]),
            'base_means': [119,119,119],
            'base_nEdges': 391,
            'base_nKeys': 12
        },
    ]
}

camera5 = {
    'number': 5,
    'im_full_path': '/home/acp/work/ggp/cam_images/camera5/snap20160705224325.jpg',
    'spots': [
        {
            'number': 12,
            'vertices': np.array(
                        [[ 310,   0],
                         [ 400,   0],
                         [ 400, 224],
                         [ 360, 224]]),
            'base_means': [99,101,103],
            'base_nEdges': 2,
            'base_nKeys': 1
        },
        {
            'number': 13,
            'vertices': np.array(
                        [[ 135,   0],
                         [ 290,   0],
                         [ 330, 224],
                         [  85, 224]]),
            'base_means': [122,122,121],
            'base_nEdges': 405,
            'base_nKeys': 24
        },
        {
            'number': 14,
            'vertices': np.array(
                        [[  20,   0],
                         [ 115,   0],
                         [  60, 224],
                         [   0, 224],
                         [   0,  30]]),
            'base_means': [119,119,121],
            'base_nEdges': 650,
            'base_nKeys': 25
        },
    ]
}


camera = camera5

_plot = True

fname = camera['im_full_path']

im = cv2.imread(fname)

#pylab.ion()
#pylab.figure(figsize=(10,6))
#pylab.imshow(im)
#pylab.colorbar()
#pylab.show()
#break


surf = cv2.xfeatures2d.SURF_create(400)

edges = cv2.Canny( im, 100, 200 )

if _plot is True:
    plt.ion()
    imc = np.copy(im)
    imc[:,:,0] = edges
    plt.figure(figsize=(10,6))
    plt.imshow(imc)

for spot in camera['spots']:
    
#    if spot['number'] != 2:
#        continue
    
    verts = spot['vertices']
    
    mask = np.zeros((im.shape[0],im.shape[1]))

    imm = np.zeros_like(im).astype('uint8')

    cv2.fillConvexPoly(mask,verts,1)
    bMask = mask.astype(bool)
    iMask = mask.astype('uint8')
    
    kp, des = surf.detectAndCompute( im, iMask)
    spot['base_nKeys'] = len(kp)
    
    spotEdges = edges[bMask]
    edgeInds = np.where(spotEdges == 255)
    spot['base_nEdges'] = np.shape(edgeInds)[1]
    
    if _plot is True:
        
        for color in range(0,3):
            imm[bMask,color] = im[bMask,color]
        imm[bMask,0] = edges[bMask]
        plt.figure(figsize=(10,6))
        plt.imshow(imm)

    for color in range(0,3):
    #for color in range(0,1):
    
        imc = im[:,:,color]
        spot['base_means'][color] = imc[bMask].mean()
        
        #edges = cv2.Canny( imc, 100, 200 )
        #spotEdges = edges[bMask]
        #edgeInds = np.where(spotEdges == 255)
        #
        #kp, des = surf.detectAndCompute( imc, iMask)
        #
        #spot['base_nKeys_vec'][color] = len(kp)
        #spot['base_nEdges_vec'][color] = np.shape(edgeInds)[1]


#        if _plot is True:
#            plt.figure(figsize=(10,6))
#            plt.imshow(imc)
#            
#            imm[bMask] = imc[bMask]
#            plt.figure(figsize=(10,6))
#            plt.imshow(imm)
    
    if _plot is True: 
        plt.show()

if _plot is True:
    plt.figure()
    plt.ioff()
    plt.close()


for spot in camera['spots']:
    pp.pprint(spot)


