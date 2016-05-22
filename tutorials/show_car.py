from scipy import misc
import matplotlib.pyplot as plt

plt.ion()

import ipdb

tc = misc.imread('two_cars.png')

s = tc.shape
nd = len(s)

plt.figure(figsize=(10, 3.6))
#for i in range(0,nd):
#    nf = 130 + i
#    nf
#    plt.subplot(130 + i)
#    plt.imshow(tc[:,:,i])
#    if i > 0:
#        plt.axis('off')

plt.subplot(131)
plt.imshow(tc)

plt.subplot(132)
plt.imshow(tc[:,:,1],cmap="hot")
plt.axis('off')

plt.subplot(133)
plt.imshow(tc[:,:,2],cmap='spectral')
plt.contourf( tc[:,:,2], [50, 100] )
plt.axis('off')

plt.subplots_adjust(wspace=0, hspace=0., top=0.99, bottom=0.01, left=0.05,
                            right=0.99)

plt.imshow(lum_img, clim=(0.0, 0.7))

plt.colorbar()

ipdb.set_trace()
plt.show()


#ipdb.set_trace()


