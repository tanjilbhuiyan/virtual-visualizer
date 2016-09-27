from SimpleCV import *
import numpy as np
# Initialize the camera
cam = Camera()
display = Display()
numFrames = 1

while not display.isDone():
    img = cam.getImage()
    cropImg = img.crop(img.width / 2, img.height / 2, 350, 400, centered=True)
    blobs = cropImg.findBlobs()

    # inside the blobs
    nblobs = 0

    if blobs is not None:
        for b in blobs:
            nblobs += 1
            centroid = b.centroid()
            centroidx, centroidy = centroid  
            # draw blob center
            img.drawCircle(centroid, 2, Color.YELLOW)
            # draw bounding box
            b.drawMinRect(color=Color.ORANGE, width=1)
            # draw info
            bstat = "cx = " + str(centroidx) + " cy = " + str(centroidy)
            img.drawText(bstat, x=centroidx, y=centroidy)
            # for x in List():
            if (200 <= b.height() <= 1000) and (100 <= b.width() <= 800):
                print str(b.height()) + " and " + str(b.width())  # and b.aspectRatio() ==X
                print b.aspectRatio()
        blobs.show(width=3)
    time.sleep(1)
    if 0.62 <= b.aspectRatio() <= 0.72:
        print "this is a glass"
