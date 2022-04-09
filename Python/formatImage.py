def formatImage(img, mode='float32'): 
    import numpy as np
    if mode=='float32':
        # converts image to float32 from 0-1 range
        if np.amax(img) > 1:
            img = img/255
        if type(img) != 'float32':
            img = img.astype('float32')
    if mode=='uint8':
        # converts image to uint8 from 0-255 range
        if np.mean(img) < 1:
            img = img*255
        if type(img) != 'uint8':
            img = img.astype('uint8')
    return img
