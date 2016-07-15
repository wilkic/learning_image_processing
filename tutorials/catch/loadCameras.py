import numpy as np

def loadCameras( time, threshSurf, edgeLims ):

    camera1 = {
        'number': 1,
        'port': 9001,
        'im_ts': time,
        'threshSurf': threshSurf,
        'edgeLims': edgeLims,       
        'spots': [
            {
                'number': 1,
                'vertices': np.array(
                            [[   0,   0],
                             [   0,  30],
                             [ 150,  60],
                             [ 150,   0]]),
                'base_means': [118,123,127],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 15,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            },
            {
                'number': 2,
                'vertices': np.array(
                            [[   0, 90],
                             [   0, 290],
                             [ 224, 230],
                             [ 224, 110]]),
                'base_means': [117,117,115],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 15,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            },
            {
                'number': 3,
                'vertices': np.array(
                            [[   0, 310],
                             [   0, 400],
                             [ 224, 400],
                             [ 224, 250]]),
                'base_means': [119,119,117],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 15,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            }
        ]
    }

    camera2 = {
        'number': 2,
        'port': 9002,
        'im_ts': time,
        'threshSurf': threshSurf,
        'edgeLims': edgeLims,       
        'spots': [
            {
                'number': 4,
                'vertices': np.array(
                            [[   0, 215],
                             [   0, 370],
                             [ 100, 400],
                             [ 224, 400],
                             [ 224, 210]]),
                'base_means': [126,126,125],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 10,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            },
            {
                'number': 5,
                'vertices': np.array(
                            [[   0,  50],
                             [   0, 200],
                             [ 224, 195],
                             [ 224,   0],
                             [ 170,   0]]),
                'base_means': [130,130,131],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 10,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            }
        ]
    }

    camera3 = {
        'number': 3,
        'port': 9003,
        'im_ts': time,
        'threshSurf': threshSurf,
        'edgeLims': edgeLims,       
        'spots': [
            {
                'number': 6,
                'vertices': np.array(
                            [[   0, 280],
                             [   0, 380],
                             [  35, 400],
                             [ 224, 400],
                             [ 224, 330]]),
                'base_means': [102,102,101],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 10,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            },
            {
                'number': 7,
                'vertices': np.array(
                            [[   0, 130],
                             [   0, 265],
                             [ 224, 310],
                             [ 224, 105]]),
                'base_means': [122,123,121],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 10,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            },
            {
                'number': 8,
                'vertices': np.array(
                            [[   0,  20],
                             [   0, 115],
                             [ 224,  85],
                             [ 224,   0],
                             [  40,   0]]),
                'base_means': [137,137,140],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 10,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            }
        ]
    }

    camera4 = {
        'number': 4,
        'port': 9004,
        'im_ts': time,
        'threshSurf': threshSurf,
        'edgeLims': edgeLims,       
        'spots': [
            {
                'number': 9,
                'vertices': np.array(
                            [[  30, 275],
                             [  30, 335],
                             [ 115, 400],
                             [ 224, 400],
                             [ 224, 390]]),
                'base_means': [120,121,119],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 10,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            },
            {
                'number': 10,
                'vertices': np.array(
                            [[  30, 165],
                             [  30, 260],
                             [ 224, 370],
                             [ 224, 240]]),
                'base_means': [121,122,119],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 10,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            },
            {
                'number': 11,
                'vertices': np.array(
                            [[  30,  40],
                             [  30, 150],
                             [ 224, 220],
                             [ 224,  40]]),
                'base_means': [119,119,119],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 10,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            }
        ]
    }

    camera5 = {
        'number': 5,
        'port': 9005,
        'im_ts': time,
        'threshSurf': threshSurf,
        'edgeLims': edgeLims,       
        'spots': [
            {
                'number': 12,
                'vertices': np.array(
                            [[   0, 310],
                             [   0, 400],
                             [ 224, 400],
                             [ 224, 360]]),
                'base_means': [99,101,103],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 10,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            },
            {
                'number': 13,
                'vertices': np.array(
                            [[   0, 135],
                             [   0, 290],
                             [ 224, 330],
                             [ 224,  85]]),
                'base_means': [122,122,121],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 10,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            },
            {
                'number': 14,
                'vertices': np.array(
                            [[   0,  20],
                             [   0, 115],
                             [ 224,  60],
                             [ 224,   0],
                             [  30,   0]]),
                'base_means': [119,119,121],
                'means': [0,0,0],
                'sigs': [0,0,0],
                'maxs': [0,0,0],
                'mins': [0,0,0],
                'mean': 0,
                'tol': 10,
                'time_present': 0,
                'occupied': 0,
                'persistence_threshold': 145
            }
        ]
    }

    cameras = {1: camera1,
               2: camera2,
               3: camera3,
               4: camera4,
               5: camera5}
    
    return cameras
