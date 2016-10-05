import numpy as np
import cv2

def analyzeImage( imageFname, camera):
    
    # Read image
    if isinstance(imageFname, basestring):
        image = cv2.imread(imageFname)
    else:
        image = imageFname
    
    # Get edges in image (use mask later)
    edges = cv2.Canny( image, camera['edgeLims'][0], camera['edgeLims'][1])

    # Set up surface for threshold
    surf = cv2.xfeatures2d.SURF_create(camera['threshSurf'])
    
    for spot in camera['spots']:
        
        # get the polygon vertices for the spot
        verts = spot['vertices']
        
        # Make (boolean) mask for spot
        mask = np.zeros((image.shape[0],image.shape[1]))
        cv2.fillConvexPoly(mask,verts,1)
        bMask = mask.astype(bool)
        
        # Make integer mask for surfing
        iMask = bMask.astype('uint8')
        
        ### Get keypoints
        kp, des = surf.detectAndCompute( image, iMask)
        spot['nKeys'] = len(kp)

        ### Get number of edges
        spotEdges = edges[bMask]
        edgeInds = np.where(spotEdges == 255)
        spot['nEdges'] = np.shape(edgeInds)[1]
	
        ### Get channel stats
        for color in range(3):
        
            imc = image[bMask,color]
            spot['means'][color] = imc.mean()
            spot['sigs'][color] = imc.std()
            spot['maxs'][color] = imc.max()
            spot['mins'][color] = imc.min()
    return
