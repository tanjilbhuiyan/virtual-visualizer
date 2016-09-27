from SimpleCV import *
import pygame
# import os
import numpy as np

# Initialize the camera
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
                numFrames = 1
                for x in range(0, numFrames):
                    time.sleep(3)  # this will on the camera but for 5 sec the camera wont catch anything.
                    img = cam.getImage()
                    # img = img.grayscale()
                    filepath = "image-" + str(x) + ".jpg"
                    img.save(filepath)
                    img.show()
                    time.sleep(3)
                    break
                img = Image("/home/pi/image-0.jpg")
                # Crop the image starting at the center of the image
                cropImg = img.crop(img.width / 2, img.height / 2, 300, 400, centered=True)
                filepath = "imagecrop-" + str(x) + ".jpg"
                cropImg.save(filepath)
                time.sleep(3)
                cropImg.show()
                time.sleep(3)
                blobfind = Image("/home/pi/imagecrop-0.jpg")
                blobs = blobfind.findBlobs()
                blobs.show(width=2)
                nblobs = 0
                if blobs is not None:
                    for b in blobs:
                        nblobs += 1
                        # get centroid
                        centroid = b.centroid()
                        centroidx, centroidy = centroid  # alt: centroidx = b.minRectX() centroidy = minRectY()
                        # draw blob center
                        img.drawCircle(centroid, 2, Color.YELLOW)
                        # draw bounding box
                        b.drawMinRect(color=Color.ORANGE, width=1)
                        # draw info
                        bstat = "cx = " + str(centroidx) + " cy = " + str(centroidy)
                        img.drawText(bstat, x=centroidx, y=centroidy)
                    blobs.show(width=3)
                    time.sleep(3)

                    H = blobs.height()
                    W = blobs.width()

                    print "H", H
                    print "W", W
                    time.sleep(3)

                    for x in H:
                        if x >= 200 and x <= 240:
                            print "this is glass height"
                        else:
                            print ""
                    for y in W:
                        if y >= 220 and y <= 280:
                            print " this is the glass width"
                        else:
                            print ""
        sys.exit()

