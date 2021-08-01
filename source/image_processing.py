# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 09:18:30 2021

@author: AppliedSoftTechEd
This has some basic operations on Image to understand how Images are processed by computer

"""
#import sys
import cv2
from PIL import Image
from numpy import asarray

import numpy as np
import os

class ImageProcessing:
    
    """
    Folder structure for input and output images
    """          
    input_path = './input_images/'
    output_path = './output_images/'

  
    
    def printImageSize(self,imageName):
        """
        Prints the shape of image.
        """
        img = Image.open(imageName)
        data = asarray(img)
        print(data.shape)

    

    def convertImageToGrayScale(self,imageName,outName):
        """
        Converts the Image to Gray Scale
        """        
        full_output_path = os.path.join(self.output_path, outName)

        # load the image
        image = Image.open(imageName).convert('L')
        # convert image to numpy array
        data = asarray(image)
        gr_im= Image.fromarray(data).save(full_output_path)

    
    def resizeImage(self,img,x_pixel,y_pixel,resizedname):    
        """
        Resizes the Image as per input 
        """ 
        print(img)
        full_output_path = os.path.join(self.output_path, resizedname)
        #img_array = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        img_array = cv2.imread(img)
        resized_image = cv2.resize(img_array, (x_pixel, y_pixel))
        print('Resizing')
        cv2.imwrite(full_output_path,resized_image) 
     
    def convertImageToPixel(self,image):
        """
        This is to print the image in matrix form to understand the Pixel values
        

        Parameters
        ----------
        image : TYPE
            The Image name which has to be printed as pixel values in matrix form.

        Returns
        -------
        None.
        """

        
        #"""
        an_image = Image.open(image)
        image_sequence = an_image.getdata()
        image_array = np.array(image_sequence)
        print(image_array)
        #"""
        img = Image.open(image).convert('L')  # convert image to 8-bit grayscale
        WIDTH, HEIGHT = img.size
        
        data1 = asarray(image)
        
        data = list(img.getdata()) # convert image data to a list of integers
        # convert that to 2D list (list of lists of integers)
        data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
        
        # At this point the image's pixels are all in memory and can be accessed
        # individually using data[row][col].
        
        # For example:
        for row in data:
            print(' '.join('{:3}'.format(value) for value in row))
        
        # Here's another more compact representation.
        chars = '@%#*+=-:. '  # Change as desired.
        scale = (len(chars)-1)/255.
        print()
        for row in data:
            print(' '.join(chars[int(value*scale)] for value in row))    

    
if __name__ == "__main__":

    imgProce = ImageProcessing()    

    #Number_2_RGB.jpg is original input taken for manupulations.
    
    #full_input_path = os.path.join(imgProce.input_path, 'Number_2_RGB.jpg')    
    #imgProce.printImageSize(full_input_path)


    #Number_2_RGB.jpg is resized to 8 by 8 pixels for understanding purpose
    #full_input_path_gray = os.path.join(imgProce.input_path, 'Number_2_RGB.jpg')
    #imgProce.resizeImage(full_input_path_gray,8,8,'Number_2_RGB_8_8.jpg')
    #full_number_2_RGB_8_8 = os.path.join(imgProce.output_path, 'Number_2_RGB_8_8.jpg')
    #imgProce.printImageSize(full_number_2_RGB_8_8)
    
    #The image is then converted to GRAY scale
    #full_input_path = os.path.join(imgProce.output_path, 'Number_2_RGB_8_8.jpg')
    #imgProce.convertImageToGrayScale(full_input_path,'Number_2_Gray_8_8.jpg')
    #full_number_2_GRAY_8_8 = os.path.join(imgProce.output_path, 'Number_2_Gray_8_8.jpg')
    #imgProce.printImageSize(full_number_2_GRAY_8_8)
    
    
    #Then check the size of image again and Print the GRAY Image in Matrix form
    #full_input_path = os.path.join(imgProce.output_path, 'Number_2_Gray_8_8.jpg')    
    #imgProce.printImageSize(full_input_path)
    
    #Print the COLORED (RGB) image in Matrix form
    full_input_path_gray_8_8 = os.path.join(imgProce.output_path, 'Number_2_RGB_8_8.jpg')
    imgProce.convertImageToPixel(full_input_path_gray_8_8)
