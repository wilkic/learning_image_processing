import cv2
from PIL import Image

def analyzeImage( imageFname, spots, threshSurf, edgemin, edgeMax)
    
    # Read image
    image = cv2.imread(imFname)

    # Get edges in image (use mask later)
    edges = cv2.Canny( image, edgeMin, edgeMax )

    # Set up surface for threshold
    surf = cv2.SURF(threshSurf)
    
    for spot in spots:
        
        # get the polygon vertices for the spot
        verts = spot['vertices']
        
        # Make (boolean) mask for spot
        shp = Image.new( 'L', image[:,:,0].shape, 0 )
        ImageDraw.Draw(shp).polygon( verts, outline=1, fill=1 )
        bMask = np.array(shp).transpose().astype(bool)
        
        # Make integer mask for surfing
        iMask = bMask.astype('uint8')
        
        ### Get keypoints
        kp, des = surf.detectAndCompute( image, iMask)
        spot['nKeys'] = len(kp)

        ### Get number of edges
        spotEdges = edges[bMask]
        edgeInds = np.where(spotEdges == 255))
        spot['nEdges'] = np.shape(edgeInds)[1]
    
        ### Get channel stats
        for color in range(3):
        
            imc = im[bMask,color]
            spot['means'][color] = imc.mean()
            spot['sigs'][color] = imc.std()
            spot['maxs'][color] = imc.max()
            spot['mins'][color] = imc.min()

    return
