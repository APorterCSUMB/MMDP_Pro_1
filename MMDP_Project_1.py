# ----- pictureReducer() begin
def pixelReducer(pic_a, pic_b, pic_c, i, j, k):    # function takes three pictures and a (i,j) location and returns a color if there is a successful reduction based on distance (k)
  
  pixel_1 = getPixelAt(pic_a, i, j)      # get a pixel object at position (i,j) from pic_list[0]
  pixel_2 = getPixelAt(pic_b, i, j)      # get a pixel object at position (i,j) from pic_list[0]
  pixel_3 = getPixelAt(pic_c, i, j)      # get a pixel object at position (i,j) from pic_list[0]
  
  pixel_1_red = getRed(pixel_1)             # get the red value from pixel_1
  pixel_2_red = getRed(pixel_2)             # get the red value from pixel_2
  pixel_3_red = getRed(pixel_3)             # get the red value from pixel_3
  
  pixel_1_green = getGreen(pixel_1)         # get the green value from pixel_1
  pixel_2_green = getGreen(pixel_2)         # get the green value from pixel_2
  pixel_3_green = getGreen(pixel_3)         # get the green value from pixel_3
  
  pixel_1_blue = getBlue(pixel_1)           # get the blue value from pixel_1
  pixel_2_blue = getBlue(pixel_2)           # get the blue value from pixel_2
  pixel_3_blue = getBlue(pixel_3)           # get the blue value from pixel_3
  
  pixel_1_color = getColor(pixel_1)         # get the color from pixel_1
  pixel_2_color = getColor(pixel_2)         # get the color from pixel_2
  pixel_3_color = getColor(pixel_3)         # get the color from pixel_3
  
  color_comp = [0,0,0,0]                    # an array to hold total magnitude RGB values and an index of how many contributions have been made
       
  if distance(pixel_1_color,pixel_2_color) < k:     # if pixel_1 and pixel_2 have colors within radius k (hit)     
                                                
    color_comp[0] = color_comp[0] + ((pixel_1_red +   pixel_2_red)  /2)    # add the average values of the two red channels to the magnitude tracker
    color_comp[1] = color_comp[1] + ((pixel_1_green + pixel_2_green)/2)    # add the average values of the two green channels to the magnitude tracker
    color_comp[2] = color_comp[2] + ((pixel_1_blue +  pixel_2_blue) /2)    # add the average values of the two blue channels to the magnitude tracker
    color_comp[3] = color_comp[3] + 1                                      # add an index value to the total values counter
    
  if distance(pixel_2_color,pixel_3_color) < k:     # if pixel_2 and pixel_3 have colors within radius k (hit)
  
    color_comp[0] = color_comp[0] + ((pixel_2_red +   pixel_3_red)  /2)    # add the average values of the two red channels to the magnitude tracker
    color_comp[1] = color_comp[1] + ((pixel_2_green + pixel_3_green)/2)    # add the average values of the two green channels to the magnitude tracker
    color_comp[2] = color_comp[2] + ((pixel_2_blue +  pixel_3_blue) /2)    # add the average values of the two blue channels to the magnitude tracker
    color_comp[3] = color_comp[3] + 1                                      # add an index value to the total values counter
    
  if distance(pixel_1_color,pixel_3_color) < k:     # if pixel_1 and pixel_3 have colors within radius k (hit)
  
    color_comp[0] = color_comp[0] + ((pixel_1_red +   pixel_3_red)  /2)    # add the average values of the two red channels to the magnitude tracker
    color_comp[1] = color_comp[1] + ((pixel_1_green + pixel_3_green)/2)    # add the average values of the two green channels to the magnitude tracker
    color_comp[2] = color_comp[2] + ((pixel_1_blue +  pixel_3_blue) /2)    # add the average values of the two blue channels to the magnitude tracker
    color_comp[3] = color_comp[3] + 1                                      # add an index value to the total values counter
  
  if (color_comp[3]>0):                                 # if there is at least one hit during the process, return a color that is the combination of
    return makeColor((color_comp[0]/color_comp[3]),     # red level that is the average of the channel magnitudes across the number of inputs
                     (color_comp[1]/color_comp[3]),     # blue level that is the average of the channel magnitudes across the number of inputs
                     (color_comp[2]/color_comp[3]))     # green level that is the average of the channel magnitudes across the number of inputs  
    
  return red    # without a hit just return red
# ----- pictureReducer() end

import time          # import the time library for code benchmarking
import os

pic_list = []               # setup an array to hold the pictures being compared
color_comp = [0,0,0,0]      # setup an array to hold intermediate color results

pic_path = pickAFolder()    # ask the user for a folder path to find the images to be reduced

for file in os.listdir(pic_path):                      # for all files int in the selected directory
    if file.endswith(".png"):                          # if the file extension is .png
      pic_list.append(makePicture(pic_path + file))    # add it to the pic_list array

start_time = time.time()   # begin timing the code's execution from this point << *****BENCHMARK BEGIN*****
cycle_monitor = 0          # "int" counter to handle tasks not necessary every "cycle"

pic_height = getHeight(pic_list[1])    # get the height of the first picture in the comparison list (should all be same)
pic_width = getWidth(pic_list[1])      # get the width of the first picture in the comparison list (should all be same)
print 'The picture is ' + str(pic_height) + ' pixels high and ' + str(pic_width) + ' pixels wide.'  # HxW console output, formatted
  
target_pic = makeEmptyPicture(pic_width, pic_height, red)    # make a new HxW picture to hold the final result
heat_map = makeEmptyPicture(pic_width, pic_height, green)    # make a new HxW picture for the heat_map, green used for high contrast while processing

show(target_pic)  # show the final result as it is being processed
show(heat_map)    # show the heat map as it is being processed

for k in range(1,255):            # algorithm based on "distance radius" concept, so lets step up to 255 (max distance)

  loop_break_flag = true          # bool to track whether we need any more image processing
  
  for i in range(pic_width):      # loop through the height of the picture, W = i
  
    for j in range(pic_height):   # loop through the wideth of the picture, H = j
      
      new_pixel = getPixelAt(target_pic, i, j)     # get a pixel object at position (i,j) from target_pic  
      
      if(getColor(new_pixel)==red):  # if the pixel in comp_pic is still pure red (needs processing "flag")
      
        loop_break_flag = false          # tell the algorithm that we are still processing pixel objects this cycle
        process_color = false            # track whether we need to do any color processing from the comparison output
        
        for g in range(3):               # we have (3) sets of triplet reduction groups within our (9) pictures
        
          temp_color = pixelReducer(                        # create a temp_color that is the result of pixelReducer() being run on the (g) set of pictures
                                    pic_list[((g*3)+0)],    # pass in the first picture from the (g) set being reduced
                                    pic_list[((g*3)+1)],    # pass in the second picture from the (g) set being reduced
                                    pic_list[((g*3)+2)],    # pass in the third picture from the (g) set being reduced
                                    i, j, k)                # pass in the (i,j) pixel location to reduce and the (k) radius to test for
                                    
          if(temp_color != red):         # if the returned color is different than the default red
          
            process_color = true         # tell the algorithm that we need to process a positive match
            
            setColor(new_pixel, temp_color)                      # set new_pixel to temp_color so we can extract some values
            
            color_comp[0] = color_comp[0] + getRed(new_pixel)    # get the red value from the pixelReducer() result and store it
            color_comp[1] = color_comp[1] + getGreen(new_pixel)  # get the greeen value from the pixelReducer() result and store it
            color_comp[2] = color_comp[2] + getBlue(new_pixel)   # get the blue value from the pixelReducer() result and store it
            color_comp[3] = color_comp[3] + 1                    # store another index value so we can reduce the magnitudes correctly
            
        if process_color == true:        # if the algorithm needs to process a positive match
        
          setColor(new_pixel, makeColor(                                  # set the color of the current pixel we are working on
                                        (color_comp[0]/color_comp[3]),    # reduce the red components and assign the result
                                        (color_comp[1]/color_comp[3]),    # reduce the green componentes and assign the result
                                        (color_comp[2]/color_comp[3])))   # reduce the blue components and assign the result
                                        
          color_comp = [0,0,0,0]         # reset the array that holds our summed RGB magnitudes and index counter for positive results
          
          hm_pixel = getPixelAt(heat_map, i, j)        # get a handle to a pixel from heat_map at the hit location
          setColor(hm_pixel, makeColor((k*10),0,0))    # write a color value to the heat map
          
      cycle_monitor = cycle_monitor + 1        # increment the cycle monitor
      
      if (cycle_monitor == 12500):             # if the cycle_monitor reaches (x) number of iterations
      
        cycle_monitor = 0            # reset the cycle_monitor variable
        
        repaint(target_pic)   # update comp_pic visual
        repaint(heat_map)     # update heat_map visual
        
        print k             # print k (radius)
        
  if loop_break_flag == true:  # if the processing loop has not engaged for an entire radius cycle
  
    break                      # break out of the loop and stop processing

print time.time()-start_time  # end timing the code's execution at this point << *****BENCHMARK END*****

pic_path = pickAFolder()    # ask the user for a folder path to save the resutlts to

writePictureTo(target_pic, pic_path + "result.png")    # write the final result picture to a folder for future use
writePictureTo(heat_map, pic_path + "heat_map.png")    # write the final heat map to a folder for future use


