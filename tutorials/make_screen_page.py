
fname = 'screen.html'
fdir = '/home/c/gsp/learning_image_processing/tutorials/notes/copi_setup/'

ffname = fdir + fname

with open( ffname, 'a+' ) as out:
    for i in range(26,55):
	mout =  '<h3>Camera %d</h3>\n' % i
	mout += '<img src="imgs/cam%d.jpg" alt="cam%d" style="width:400px;height:224px;">\n' % (i,i)
	mout += '<p></p>\n'
	mout += '<br />\n'
	mout += '<p></p>\n'
	mout += '<script src="imgs/ts%d.js"></script>\n' % i
	mout += '<script>\n'
	mout += '  document.write(text);\n'
	mout += '</script>\n'
	mout += '<p></p>\n'
	mout += '<br />\n'
	mout += '<p></p>\n'
	mout += '</body>\n'
	mout += '</html>\n'

        print >> out, mout


