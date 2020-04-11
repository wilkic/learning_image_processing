
fname = 'camera_assignments.txt'
fdir = '/home/c/gsp/learning_image_processing/tutorials/notes/copi_setup/'

ffname = fdir + fname

with open( ffname, 'a+' ) as out:
    for i in range(26,55):
        mout  = "host cam_%d {\n" % i
        mout += '    option host-name "Camera%d";\n' %i
        mout += '    hardware ethernet ;\n'
        mout += '    fixed-address 10.10.110.1%d;\n' %i
        mout += '}\n'

        print >> out, mout


