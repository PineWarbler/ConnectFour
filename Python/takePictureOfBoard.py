def takePictureOfBoard():
    '''
    written by P. Reynolds
    Takes a picture using the Raspberry Pi's camera
    default resolution is 1920 x 1088 

    Returns
        outputArray : a numpy array of the image in RGB format

    '''
    from picamera import PiCamera
    import numpy as np

    camera = PiCamera()


    # The horizontal resolution is rounded up to the nearest multiple of 32 pixels, while the vertical resolution is rounded up to the nearest multiple of 16 pixels.
    # https://picamera.readthedocs.io/en/release-1.12/recipes2.html#capturing-to-a-numpy-array
    # max resolution is: 3280 × 2464 pixels
    xRes = 1920
    yRes = 1088 # nearest multiple of 32 to 1080

    camera.resolution = (xRes, yRes)

    outputArray = np.empty((yRes, xRes, 3), dtype=np.uint8) # make sure that yRes and xRes are correct.  Picamera rounds the resolution
    camera.capture(outputArray, 'rgb')

    camera.close()

    return outputArray
