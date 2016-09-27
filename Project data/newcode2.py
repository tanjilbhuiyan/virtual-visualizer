from SimpleCV import *
import numpy as np
import RPi.GPIO as GPIO
import time

cam = Camera()
display = Display()

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, 0)

GPIO.setup(ECHO, GPIO.IN)

time.sleep(0.1)
print "starting sensor"

GPIO.output(TRIG, 1)
time.sleep(0.00001)
GPIO.output(TRIG, 0)

while GPIO.input(ECHO) == 0:
	pass
start = time.time()

while GPIO.input(ECHO) == 1:
	pass
stop = time.time()

print (stop - start) * 17000
GPIO.cleanup()

while not display.isDone():
        img = cam.getImage()
        cropImg = img.crop(img.width / 2, img.height / 2, 350, 350, centered=True)
        blobs = cropImg.findBlobs()
        nblobs = 0

        if blobs is not None:
            for b in blobs:
                nblobs += 1
                centroid = b.centroid()
                centroidx, centroidy = centroid  # alt: centroidx = b.minRectX() centroidy = minRectY()
                # draw blob center
                img.drawCircle(centroid, 2, Color.YELLOW)
                # draw bounding box
                b.drawMinRect(color=Color.ORANGE, width=1)
                # draw info
                bstat = "cx = " + str(centroidx) + " cy = " + str(centroidy)
                img.drawText(bstat, x=centroidx, y=centroidy)
                # for x in List():
                if (200 <= b.height() <= 1000) and (100 <= b.width() <= 800):
                    	print str(b.height()) + " and " + str(b.width())  # and b.aspectRatio() == X
                    	print b.aspectRatio()
            blobs.show(width=3)
        time.sleep(1)
        if 0.62 <= b.aspectRatio() <= 0.72:
            	print "this is a glass"

