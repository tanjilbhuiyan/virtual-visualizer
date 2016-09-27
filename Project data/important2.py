from SimpleCV import *
import numpy as np
import RPi.GPIO as GPIO
import time
import pygame

cam = Camera()
display = Display()
numFrames = 1
for x in range(0, numFrames):
    time.sleep(5)  # this will on the camera but for 5 sec the camera wont catch anything.
    img = cam.getImage()
    img = img.grayscale()
    filepath = "image-" + str(x) + ".jpg"
    img.save(filepath)
    break
while not display.isDone():
    # Get Image from camera
    img = cam.getImage()
    # Make image black and white
    img = img.grayscale()
    # Show the image
    img.show()
    if display.mouseLeft:
        win = img.show()
        win.quit()
    if display.mouseRight:
        img = img.save("filename.jpg", display)

        compare = Image("/home/pi/filename.jpg")
        img2 = Image("/home/pi/image-0.jpg")
        edgeFeats = EdgeHistogramFeatureExtractor()

        a = np.array(edgeFeats.extract(compare))
        b = np.array(edgeFeats.extract(img2))

        AandB = np.sum(np.square((a - b)))
        print AandB

        if AandB < 0.30:
            print "this picture is matched, this is a glass"
            pygame.init()
            pygame.mixer.music.load("/home/pi/audio/Voice 007.wav")
            pygame.mixer.music.play()
            time.sleep(7)
        else:
            print "No match found"
            pygame.init()
            pygame.mixer.music.load("/home/pi/audio/Voice 008.wav")
            pygame.mixer.music.play()
            time.sleep(7)

            while not display.isDone():
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

                if 5 <= (stop - start) * 17000 <= 20:
                    print (stop - start) * 17000
                    pygame.init()
                    pygame.mixer.music.load("/home/pi/audio/Voice 001.wav")
                    pygame.mixer.music.play()
                    time.sleep(7)
                if 21 <= (stop - start) * 17000 <= 40:
                    print (stop - start) * 17000
                    pygame.init()
                    pygame.mixer.music.load("/home/pi/audio/Voice 002.wav")
                    pygame.mixer.music.play()
                    time.sleep(7)
                if 41 <= (stop - start) * 17000 <= 60:
                    print (stop - start) * 17000
                    pygame.init()
                    pygame.mixer.music.load("/home/pi/audio/Voice 003.wav")
                    pygame.mixer.music.play()
                    time.sleep(7)
                if (stop - start) * 17000 >= 60:
                    print (stop - start) * 17000
                    pygame.init()
                    pygame.mixer.music.load("/home/pi/audio/Voice 004.wav")
                    pygame.mixer.music.play()
                    time.sleep(7)
                GPIO.cleanup()
                img = cam.getImage()
                cropImg = img.crop(img.width / 2, img.height / 2, 350, 350, centered=True)
                blobs = cropImg.findBlobs()
                nblobs = 0

                if blobs is not None:
                    for b in blobs:
                        nblobs += 1
                        centroid = b.centroid()
                        centroidx, centroidy = centroid  # alt: centroidx = b.minRectX() centroidy = minRectY()
                        img.drawCircle(centroid, 2, Color.YELLOW)
                        b.drawMinRect(color=Color.ORANGE, width=1)
                        bstat = "cx = " + str(centroidx) + " cy = " + str(centroidy)
                        img.drawText(bstat, x=centroidx, y=centroidy)
                        if (200 <= b.height() <= 1000) and (100 <= b.width() <= 800):
                            print str(b.height()) + " and " + str(b.width())  # and b.aspectRatio() == X
                            print b.aspectRatio()
                    blobs.show(width=3)
                time.sleep(1)
                if 0.80 <= b.aspectRatio() <= 1.1:
                    print "this is a glass"
                    pygame.init()
                    pygame.mixer.music.load("/home/pi/audio/Voice 005.wav")
                    pygame.mixer.music.play()
                    time.sleep(7)
                if 0.60 <= b.aspectRatio() <= 0.78:
                    print "this is a box"
                    pygame.init()
                    pygame.mixer.music.load("/home/pi/audio/Voice 006.wav")
                    pygame.mixer.music.play()
                    time.sleep(7)
