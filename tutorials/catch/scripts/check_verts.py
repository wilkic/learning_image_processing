
import os

import numpy as np
import matplotlib.pyplot as plt
import cv2

import json
import pprint as pp

import ipdb



plt.close("all")

def onclick(event):
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))


camera1 = {
    'number': 1,
    #'im_full_path': '/home/acp/work/ggp/cam_images/camera1/snap20160705224323.jpg',
    #'im_full_path': '/home/acp/work/aws/current_images/spot1.jpg',
    #'im_full_path': '/home/acp/Downloads/spot2violation.jpg',
    #'im_full_path': '/home/acp/Downloads/spot3_taken.jpg',
    #'im_full_path': '/home/acp/Downloads/spot1_fv.jpg',
    #'im_full_path': '/home/acp/work/aws/images_of_undetections/spot3_20161007T092135.jpg',
    #'im_full_path': '/home/acp/work/aws/images_of_undetections/spot1_20161007T214217.jpg',
    'im_full_path': '/home/c/work/aws/current_images/spot1.jpg',

    'spots': [
        {
            'number': 1,
            'vertices': np.array(
                        [[  1920,  960],
                         [  1470,  190],
                         [  1675,  190],
                         [  1920,  540]]),
            'base_means': [143,147,147],
            'base_nEdges': 440,
            'base_nKeys': 0,
        },
        {
            'number': 2,
            'vertices': np.array(
                        [[   790,  1080],
                         [   705,   120],
                         [  1220,   150],
                         [  1630,  1080]]),
            'base_means': [136,141,140],
            'base_nEdges': 12000,
            'base_nKeys': 2,
        },
        {
            'number': 3,
            'vertices': np.array(
                        [[    0,   375],
                         [  150,   100],
                         [  590,   100],
                         [  630,  1080],
                         [    0,  1080]]),
            'base_means': [75,78,71],
            'base_nEdges': 4670,
            'base_nKeys': 1,
        }
    ]
}

camera2 = {
    'number': 2,
    'im_full_path': '/home/acp/work/aws/cam_images/camera2/snap20160731155138.jpg',
    'spots': [
        {
            'number': 4,
            'vertices': np.array(
                        [[ 220,   0],
                         [ 370,   0],
                         [ 400, 100],
                         [ 400, 224],
                         [ 220, 224]]),
            'base_means': [127,123,123],
            'base_nEdges': 6,
            'base_nKeys': 2,
        },
        {
            'number': 5,
            'vertices': np.array(
                        [[  40,  50],
                         [ 190,  20],
                         [ 175, 224],
                         [   0, 224],
                         [   0, 180]]),
            'base_means': [130,130,131],
            'base_nEdges': 0,
            'base_nKeys': 1,
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
                        [[ 290,   0],
                         [ 380,   0],
                         [ 400,  40],
                         [ 400, 224],
                         [ 340, 224]]),
            'base_means': [101,102,101],
            'base_nEdges': 0,
            'base_nKeys': 0,
        },
        {
            'number': 7,
            'vertices': np.array(
                        [[ 130,  30],
                         [ 265,   0],
                         [ 310, 224],
                         [ 105, 224]]),
            'base_means': [121,122,122],
            'base_nEdges': 0,
            'base_nKeys': 5,
        },
        {
            'number': 8,
            'vertices': np.array(
                        [[   0,  50],
                         [ 100,  50],
                         [  80, 224],
                         [   0, 224]]),
            'base_means': [137,137,140],
            'base_nEdges': 0,
            'base_nKeys': 0,
        },
    ]
}

camera4 = {
    'number': 4,
#    'im_full_path': '/home/acp/work/ggp/cam_images/camera4/snap20160706230618.jpg',
#    'im_full_path': '/home/acp/work/aws/cam_images/camera4/snap20160723023418.jpg',
    #'im_full_path': '/home/acp/Downloads/spot10_fd.jpg',
    'im_full_path': '/home/c/work/aws/current_images/spot9.jpg',
    'spots': [
        {
            'number': 9,
            'vertices': np.array(
                        [[ 400, 180],
                         [ 290, 20],
                         [ 400, 20]]),
            'base_means': [118,120,120],
            'base_nEdges': 450,
            'base_nKeys': 0,
        },
        {
            'number': 10,
            'vertices': np.array(
                        [[ 190,  30],
                         [ 260,  30],
                         [ 370, 224],
                         [ 260, 224]]),
            'base_means': [119,122,122],
            'base_nEdges': 0,
            'base_nKeys': 1,
        },
        {
            'number': 11,
            'vertices': np.array(
                        [[  40,  40],
                         [ 145,  40],
                         [ 170, 224],
                         [  40, 224]]),
            'base_means': [117,117,118],
            'base_nEdges': 0,
            'base_nKeys': 0,
        },
    ]
}

camera5 = {
    'number': 5,
    #'im_full_path': '/home/acp/work/ggp/cam_images/camera5/snap20160705224325.jpg',
    #'im_full_path': '/home/acp/Downloads/spot12_fd.png',
    #'im_full_path': '/home/acp/Downloads/spot12_fd_again.jpg',
    'im_full_path': '/home/acp/Downloads/spot14_taken.jpg',
    'spots': [
        {
            'number': 12,
            'vertices': np.array(
                        [[ 330,   0],
                         [ 400,   0],
                         [ 400, 224],
                         [ 370, 224]]),
            'base_means': [99,101,103],
            'base_nEdges': 0,
            'base_nKeys': 0,
        },
        {
            'number': 13,
            'vertices': np.array(
                        [[ 130,  25],
                         [ 290,  25],
                         [ 330, 224],
                         [  90, 224]]),
            'base_means': [122,122,121],
            'base_nEdges': 280,
            'base_nKeys': 21,
        },
        {
            'number': 14,
            'vertices': np.array(
                        [[   0,  50],
                         [ 100,  50],
                         [  50, 224],
                         [   0, 224]]),
            'base_means': [126,123,123],
            'base_nEdges': 0,
            'base_nKeys': 1
        },
    ]
}

camera6 = {
    'number': 6,
    #'im_full_path': '/home/acp/work/ggp/cam_images/camera6/snap20160705224325.jpg',
#    'im_full_path': '/home/acp/work/learning_image_processing/tutorials/catch/current_images/spot16.jpg',
#    'im_full_path': '/home/acp/work/aws/images_of_violations/spot17_Sat Jul 23 21:10:46 2016.jpg',
   # 'im_full_path': '/home/acp/work/aws/cam_images/camera6/snap20160727024451.jpg',
    #'im_full_path': '/home/acp/Downloads/spot16.jpg',
    #'im_full_path': '/home/acp/Downloads/spot16taken_072916211956.jpg',
    #'im_full_path': '/home/acp/Downloads/spots1617_occ.jpg',
    #'im_full_path': '/home/acp/Downloads/spot22_fd.jpg',
    #'im_full_path': '/home/acp/Downloads/spot17_bad_detection.jpg',
    #'im_full_path': '/home/acp/Downloads/spot15_empty.jpg',
    'im_full_path': '/home/acp/Downloads/spot16_fd.jpg',
    'spots': [
        {
            'number': 15,
            'vertices': np.array(
                        [[   0,  40],
                         [  30,  40],
                         [ 100, 170],
                         [   0, 170]]),
            'base_means': [121,118,118],
            'base_nEdges': 187,
            'base_nKeys': 1
        },
        {
            'number': 16,
            'vertices': np.array(
                        [[  85,  20],
                         [ 290,  20],
                         [ 235, 195],
                         [ 140, 195]]),
            'base_means': [113,115,115],
            'base_nEdges': 220,
            'base_nKeys': 21
        },
        {
            'number': 17,
            'vertices': np.array(
                        [[ 400,   0],
                         [ 400,  85],
                         [ 350, 150],
                         [ 300, 155]]),
            'base_means': [123,125,125],
            'base_nEdges': 28,
            'base_nKeys': 0
        },
        {
            'number': 22,
            'vertices': np.array(
                        [[ 150, 200],
                         [ 275, 200],
                         [ 255, 224],
                         [ 155, 224]]),
            'base_means': [166,163,163],
            'base_nEdges': 122,
            'base_nKeys': 0
        }
    ]
}

camera7 = {
    'number': 7,
    #'im_full_path': '/home/acp/Downloads/cam7.jpg',
    #'im_full_path': '/home/acp/Downloads/spot23_fd.jpg',
    'im_full_path': '/home/acp/Downloads/spot23_bad.jpg',
    
    'spots': [
        {
            'number': 18,
            'vertices': np.array(
                        [[ 180, 110],
                         [ 295, 110],
                         [ 375, 224],
                         [ 175, 224]]),
            'base_means': [110,114,114],
            'base_nEdges': 82,
            'base_nKeys': 4,
        },
        {
            'number': 19,
            'vertices': np.array(
                        [[  50, 110],
                         [ 150, 110],
                         [ 150, 224],
                         [   0, 224],
                         [   0, 180]]),
            'base_means': [120,121,121],
            'base_nEdges': 72,
            'base_nKeys': 6,
        },
        {
            'number': 23,
            'vertices': np.array(
                        [[  80,  30],
                         [ 220,  30],
                         [ 220,  50],
                         [  80,  50]]),
            'base_means': [150,148,145],
            'base_nEdges': 141,
            'base_nKeys': 4,
        }
    ]
}

camera8 = {
    'number': 8,
    #'im_full_path': '/home/acp/work/aws/cam_images/camera8/snap20160721043347.jpg',
    #'im_full_path': '/home/acp/Downloads/spot21.jpg',
    #'im_full_path': '/home/acp/Downloads/spot21_new.jpg',
    'im_full_path': '/home/c/work/aws/current_images/spot20.jpg',
    'spots': [
        {
            'number': 20,
            'vertices': np.array(
                        [[ 260,  20],
                         [ 360,  20],
                         [ 400,  70],
                         [ 400, 224],
                         [ 275, 224],
                         [ 255,  50]]),
            'base_means': [99,99,99],
            'base_nEdges': 9,
            'base_nKeys': 3,
        },
        {
            'number': 21,
            'vertices': np.array(
                        [[  70,  25],
                         [ 170,  25],
                         [ 140, 224],
                         [   0, 224],
                         [   0, 130]]),
            'base_means': [105,105,105],
            'base_nEdges': 400,
            'base_nKeys': 21,
        }
    ]
}

camera9 = {
    'number': 9,
    #'im_full_path': '/home/acp/work/aws/cam_images/camera9/snap20160721043347.jpg',
    'im_full_path': '/home/acp/Downloads/spot26_taken.jpg',
    'spots': [
        {
            'number': 24,
            'vertices': np.array(
                        [[  80,  40],
                         [ 155,  30],
                         [  95, 170],
                         [  35, 165],
                         [  15, 120]]),
            'base_means': [138,137,135],
            'base_nEdges': 31,
            'base_nKeys': 0,
        },
        {
            'number': 25,
            'vertices': np.array(
                        [[ 172,  30],
                         [ 260,  30],
                         [ 290, 100],
                         [ 145, 100]]),
            'base_means': [112,112,112],
            'base_nEdges': 11,
            'base_nKeys': 0,
        },
        {
            'number': 26,
            'vertices': np.array(
                        [[ 300,  20],
                         [ 340,  20],
                         [ 400,  75],
                         [ 400, 160],
                         [ 370, 165]]),
            'base_means': [143,142,142],
            'base_nEdges': 0,
            'base_nKeys': 0,
        },
    ]
}

camera10 = {
    'number': 10,
    #'im_full_path': '/home/acp/work/aws/cam_images/camera10/snap20160707210354.jpg',
    'im_full_path': '/home/c/work/aws/current_images/spot27.jpg',
    'spots': [
        {
            'number': 27,
            'vertices': np.array(
                            [[ 489,  474],
                             [ 835,  446],
                             [ 711,  867],
                             [ 272,  839]]),
                'base_means': [90,94,93],
                'base_nEdges': 250,
                'base_nKeys': 0,
        },
        {
            'number': 28,
            'vertices': np.array(
                            [[ 1383,  341],
                             [ 1700,  328],
                             [ 1885,  638],
                             [ 1897,  951],
                             [ 1665, 1016]]),
                'base_means': [90,94,93],
                'base_nEdges': 250,
                'base_nKeys': 0,
        }
    ]
}

camera11 = {
    'number': 11,
    'im_full_path': '/home/acp/work/aws/cam_images/camera11/snap20160721043348.jpg',
    #'im_full_path': '/home/acp/work/aws/cam_images/camera11/snap20160721043348.jpg',
    #'im_full_path': '/home/acp/Downloads/spot38_violation.jpg',
    'spots': [
        {
            'number': 36,
            'vertices': np.array(
                        [[  50,  75],
                         [ 105,  75],
                         [  50, 224],
                         [   0, 224],
                         [   0, 155]]),
            'base_means': [114,116,115],
            'base_nEdges': 92,
            'base_nKeys': 1,
        },
        {
            'number': 37,
            'vertices': np.array(
                        [[ 140,  75],
                         [ 245,  75],
                         [ 300, 224],
                         [ 120, 224]]),
            'base_means': [140,142,141],
            'base_nEdges': 109,
            'base_nKeys': 2,
        },
        {
            'number': 38,
            'vertices': np.array(
                        [[ 305,  90],
                         [ 350,  85],
                         [ 400, 145],
                         [ 400, 224],
                         [ 355, 224]]),
            'base_means': [110,113,112],
            'base_nEdges': 104,
            'base_nKeys': 0,
        },
        {
            'number': 43,
            'vertices': np.array(
                        [[ 168,   2],
                         [ 200,   2],
                         [ 223,  30],
                         [ 159,  30]]),
            'base_means': [152,144,143],
            'base_nEdges': 72,
            'base_nKeys': 2,
        },
    ]
}

camera12 = {
    'number': 12,
    #'im_full_path': '/home/acp/work/aws/cam_images/camera12/snap20160721233213.jpg',
    #'im_full_path': '/home/acp/Downloads/snap20160729153725.jpg',
    #'im_full_path': '/home/acp/Downloads/45failed_detect.jpg',
    #'im_full_path': '/home/acp/Downloads/46failed_detect.jpg',
    #'im_full_path': '/home/acp/Downloads/spot46_fd.jpg',
    #'im_full_path': '/home/acp/Downloads/46left.jpg',
    #'im_full_path': '/home/acp/Downloads/spot35_bad.jpg',
    #'im_full_path': '/home/acp/Downloads/spot34_baseline.jpg',
    #'im_full_path': '/home/acp/Downloads/spot35_taken.jpg',
    'im_full_path': '/home/c/work/aws/current_images/spot33.jpg',
    'spots': [
        {
            'number': 33,
            'vertices': np.array(
                        [[  225,  675],
                         [  646,  688],
                         [  535, 1035],
                         [   11, 1060]]),
            'base_means': [150,150,150],
            'base_nEdges': 3322,
            'base_nKeys': 10,
        },
        {
            'number': 34,
            'vertices': np.array(
                        [[  730,  709],
                         [ 1287,  697],
                         [ 1374, 1041],
                         [  690, 1038]]),
            'base_means': [140,140,140],
            'base_nEdges': 4500,
            'base_nKeys': 160,
        },
        {
            'number': 35,
            'vertices': np.array(
                        [[ 1402,  700],
                         [ 1792,  685],
                         [ 1894, 1041],
                         [ 1501, 1050]]),
            'base_means': [130,130,130],
            'base_nEdges': 1000,
            'base_nKeys': 70,
        },
        {
            'number': 44,
            'vertices': np.array(
                        [[ 1523,  127],
                         [ 1684,  223],
                         [ 1510,  208]]),
            'base_means': [130,123,127],
            'base_nEdges': 100,
            'base_nKeys': 0,
        },
        {
            'number': 45,
            'vertices': np.array(
                        [[ 1157,  102],
                         [ 1334,  118],
                         [ 1399,  192],
                         [ 1191,  180]]),
            'base_means': [102,98,89],
            'base_nEdges': 101,
            'base_nKeys': 0,
        },
        {
            'number': 46,
            'vertices': np.array(
                        [[  903,   90],
                         [ 1089,  100],
                         [ 1101,  174],
                         [  888,  174]]),
            'base_means': [107,106,110],
            'base_nEdges': 100,
            'base_nKeys': 0,
        },
    ]
}

camera13 = {
    'number': 13,
    #'im_full_path': '/home/acp/work/aws/cam_images/camera13/snap20160721233213.jpg',
    #'im_full_path': '/home/acp/Downloads/cam13_30present_false31.jpg',
    'im_full_path': '/home/acp/Downloads/spot30_bad.jpg',
    'spots': [
        {
            'number': 29,
            'vertices': np.array(
                        [[   0,  60],
                         [  60,  50],
                         [  70,  75],
                         [  55, 140],
                         [  50, 224],
                         [   0, 224]]),
            'base_means': [144,138,135],
            'base_nEdges': 8,
            'base_nKeys': 0,
        },
        {
            'number': 30,
            'vertices': np.array(
                        [[ 140,  55],
                         [ 280,  55],
                         [ 300, 224],
                         [ 115, 224]]),
            'base_means': [111,115,115],
            'base_nEdges': 300,
            'base_nKeys': 21,
        }
    ]
}

camera14 = {
    'number': 14,
    #'im_full_path': '/home/acp/work/aws/cam_images/camera14/snap20160727024454.jpg',
    #'im_full_path': '/home/acp/Downloads/48failed_detect.jpg',
    #'im_full_path': '/home/acp/Downloads/spot38_fn.jpg',
    #'im_full_path': '/home/acp/Downloads/spot47_fd.jpg',
    #'im_full_path': '/home/acp/Downloads/spot48_fd.jpg',
    #'im_full_path': '/home/acp/Downloads/spot32.jpg',
    'im_full_path': '/home/c/work/aws/current_images/spot32.jpg',
    'spots': [
        {
            'number': 31,
            'vertices': np.array(
                        [[    0, 1080],
                         [   10, 1000],
                         [  260,  710],
                         [  570,  750],
                         [  440, 1080]]),
            'base_means': [150,150,150],
            'base_nEdges': 6300,
            'base_nKeys': 0,
        },
        {
            'number': 32,
            'vertices': np.array(
                        [[  721,  719],
                         [ 1275,  722],
                         [ 1340, 1080],
                         [  620, 1080]]),
            'base_means': [140,140,140],
            'base_nEdges': 8220,
            'base_nKeys': 0,
        },
        {
            'number': 47,
            'vertices': np.array(
                        [[ 1173,  161],
                         [ 1349,  155],
                         [ 1454,  260],
                         [ 1213,  260]]),
            'base_means': [121,112,105],
            'base_nEdges': 500,
            'base_nKeys': 20,
        },
        {
            'number': 48,
            'vertices': np.array(
                        [[  940,  155],
                         [ 1123,  152],
                         [ 1151,  239],
                         [  891,  248]]),
            'base_means': [74,75,74],
            'base_nEdges': 377,
            'base_nKeys': 110,
        },
        {
            'number': 49,
            'vertices': np.array(
                        [[  714,  143],
                         [  885,  143],
                         [  817,  242],
                         [  590,  254]]),
            'base_means': [91,86,81],
            'base_nEdges': 45,
            'base_nKeys': 0,
        },
    ]
}


camera15 = {
    'number': 15,
    'im_full_path': '/tmp/tmp.jpg',
    'spots': [
        {
            'number': 32,
            'vertices': np.array(
                        [[ 410,   0],
                         [ 690,   0],
                         [ 640, 330],
                         [1280, 350],
                         [1280, 720],
                         [   0, 720]]),
            'base_means': [115,118,118],
            'base_nEdges': 0,
            'base_nKeys': 0,
        },
    ]
}

camera = camera14

_plot = True

fname = camera['im_full_path']

im = cv2.imread(fname)


edges = cv2.Canny( im, 100, 200 )

if _plot is True:
    #plt.ion()
    imc = np.copy(im)
    imc[:,:,0] = edges

imcc = np.copy(imc)

for spot in camera['spots']:
    
#    if spot['number'] != 38:
#        continue
    
    verts = spot['vertices']
    pverts = verts.copy()
    pverts.astype('int32')
    cv2.polylines(imcc,[verts],True,(0,255,255))

    mask = np.zeros((im.shape[0],im.shape[1]))

    imm = np.zeros_like(im).astype('uint8')

    cv2.fillConvexPoly(mask,verts,1)
    bMask = mask.astype(bool)
    iMask = mask.astype('uint8')
    
    spotEdges = edges[bMask]
    edgeInds = np.where(spotEdges == 255)
    spot['base_nEdges'] = np.shape(edgeInds)[1]
    
#    if _plot is True:
#        
#        for color in range(0,3):
#            imm[bMask,color] = im[bMask,color]
#        imm[bMask,0] = edges[bMask]
#        ims = np.copy(imm)
#        ims = cv2.drawKeypoints( imm, kp, None, (255,0,0), 4 )
#        sfig = plt.figure(figsize=(10,6))
#        plt.imshow(ims)

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


    if _plot is True: 
        plt.show()

if _plot is True:
    fig = plt.figure(figsize=(10,6))
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.imshow(imcc)
    plt.show()

    plt.figure()
    plt.ioff()
    plt.close()


for spot in camera['spots']:
    pp.pprint(spot)


