from scipy import misc
import matplotlib.pyplot as plt

plt.ioff()
plt.ion()

import ipdb

tc = misc.imread('/home/acp/Projects/ggp/next_car/two_cars.jpg')

s = tc.shape
nd = len(s)


#plt.figure()
#plt.imshow(tc[:,:,0],cmap='cool')
#plt.colorbar()
#plt.show()


#plt.figure(figsize=(10, 3.6))
plt.figure(figsize=(10, 7))

#for i in range(0,nd):
#    nf = 130 + i
#    nf
#    plt.subplot(130 + i)
#    plt.imshow(tc[:,:,i])
#    if i > 0:
#        plt.axis('off')

plt.subplot(331)
plt.imshow(tc)

plt.subplot(332)
plt.imshow(tc[:,:,1],cmap="gray")
plt.axis('off')
#plt.colorbar()

plt.subplot(333)
plt.imshow(tc[:,:,2],cmap="hot")
plt.axis('off')


plt.subplot(334)
plt.imshow(tc[:,:,0],cmap='cool')
#plt.contourf( tc[:,:,2], [50, 100] )
plt.axis('off')

plt.subplot(335)
plt.imshow(tc[:,:,1],cmap='bone')
#plt.contourf( tc[:,:,2], [100, 140] )
plt.axis('off')

plt.subplot(336)
plt.imshow(tc[:,:,2],cmap='copper')
#plt.contourf( tc[:,:,2], [170, 255] )
plt.axis('off')


plt.subplot(337)
plt.imshow(tc[:,:,0],cmap='jet')
plt.contourf( tc[:,:,0], [0, 50], colors='k' )
plt.axis('off')

plt.subplot(338)
plt.imshow(tc[:,:,1],cmap='bone')
plt.contourf( tc[:,:,1], [0, 60], colors='#ff6666' )
plt.axis('off')

plt.subplot(339)
plt.imshow(tc[:,:,2],cmap='spring')
plt.contourf( tc[:,:,2], [0, 30], colors='k' )
plt.axis('off')


plt.subplots_adjust(wspace=0, hspace=0., top=0.99, bottom=0.01, left=0.05,
                            right=0.99)



plt.show()

#plt.imshow(lum_img, clim=(0.0, 0.7))

#ipdb.set_trace()

