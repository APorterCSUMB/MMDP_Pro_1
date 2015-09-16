# ----- pictureReducer() begin
def pictureReducer(pic_a, pic_b, pic_c, i, j, k):
  
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
  
  red_val = 0        # setup a way to track the total magnitude of red inputs per pixel
  green_val = 0      # setup a way to track the total magnitude of green inputs per pixel
  blue_val = 0       # setup a way to track the total magnitude of blue inputs per pixel
  tot_vals = 0       # setup a way to track the number of inputs per pixel
       
  if distance(pixel_1_color,pixel_2_color) < k:     # if pixel_1 and pixel_2 have colors within radius k (hit)                                                   
    red_val = red_val + ((pixel_1_red +   pixel_2_red)  /2)        # add the average values of the two red channels to the magnitude tracker
    green_val = green_val + ((pixel_1_green + pixel_2_green)/2)    # add the average values of the two green channels to the magnitude tracker
    blue_val = blue_val + ((pixel_1_blue +  pixel_2_blue) /2)      # add the average values of the two blue channels to the magnitude tracker
    tot_vals = tot_vals + 1
  if distance(pixel_2_color,pixel_3_color) < k:     # if pixel_2 and pixel_3 have colors within radius k (hit)
    red_val = red_val + ((pixel_2_red +   pixel_3_red)  /2)        # add the average values of the two red channels to the magnitude tracker
    green_val = green_val + ((pixel_2_green + pixel_3_green)/2)    # add the average values of the two green channels to the magnitude tracker
    blue_val = blue_val + ((pixel_2_blue +  pixel_3_blue) /2)      # add the average values of the two blue channels to the magnitude tracker
    tot_vals = tot_vals + 1
  if distance(pixel_1_color,pixel_3_color) < k:     # if pixel_1 and pixel_3 have colors within radius k (hit)
    red_val = red_val + ((pixel_1_red +   pixel_3_red)  /2)        # add the average values of the two red channels to the magnitude tracker
    green_val = green_val + ((pixel_1_green + pixel_3_green)/2)    # add the average values of the two green channels to the magnitude tracker
    blue_val = blue_val + ((pixel_1_blue +  pixel_3_blue) /2)      # add the average values of the two blue channels to the magnitude tracker
    tot_vals = tot_vals + 1
  
  if (tot_vals>0):                                                                       # if there is at least one hit during the process
    return makeColor((red_val/tot_vals),(green_val/tot_vals),(blue_val/tot_vals))        # return color that is the average of the channel magnitudes across the number of inputs
    
  return red    # without a hit just return red
# ----- pictureReducer() end




import time          # import the time library for code benchmarking

pic_list = []               # setup an array to hold the pictures being compared
color_comp = [0,0,0,0]      # setup an array to hold intermediate color results


for i in range (9):                          # open up (x) number of pictures
  pic_list.append(makePicture(pickAFile()))  # and put the pictures in the comparison list

start_time = time.time()   # begin timing the code's execution from this point << **BENCHMARK BEGIN**
cycle_monitor = 0  # "int" counter to handle tasks not necessary every "cycle"

pic_height = getHeight(pic_list[1])    # get the height of the first picture in the comparison list (should all be same)
pic_width = getWidth(pic_list[1])      # get the width of the first picture in the comparison list (should all be same)
print 'The picture is ' + str(pic_height) + ' pixels high and ' + str(pic_width) + ' pixels wide.'  # HxW console output, formatted
  
target_pic = makeEmptyPicture(pic_width, pic_height, red)    # make a new HxW picture to hold the final result
heat_map = makeEmptyPicture(pic_width, pic_height, red)

show(target_pic)  # show the final result as it is being processed
show(heat_map)

for k in range(255):              # algorithm based on "distance radius" concept, so lets step up to 255 (max distance)
  loop_break_flag = true          # bool to track whether we need any more image processing
  for i in range(pic_width):      # loop through the height of the picture, W = i
    for j in range(pic_height):   # loop through the wideth of the picture, H = j
      
      new_pixel = getPixelAt(target_pic, i, j)     # get a pixel object at position (i,j) from target_pic  
      
      if(getColor(new_pixel)==red):  # if the pixel in comp_pic is still pure red (needs processing "flag")
      
        loop_break_flag = false      # tell the algorithm that we are still processing pixel objects this cycle
        process_color = false        # track whether we need to do any color processing from the comparison output
        
        for g in range(3):
        
          temp_color = pictureReducer(pic_list[((g*3)+0)],
                                      pic_list[((g*3)+1)], 
                                      pic_list[((g*3)+2)], 
                                      i, j, k)
          
          if(temp_color != red):
            process_color = true
            setColor(new_pixel, temp_color)
            color_comp[0] = color_comp[0] + getRed(new_pixel)
            color_comp[1] = color_comp[1] + getGreen(new_pixel)
            color_comp[2] = color_comp[2] + getBlue(new_pixel)
            color_comp[3] = color_comp[3] + 1
            
        if process_color == true:
          setColor(new_pixel, makeColor((color_comp[0]/color_comp[3]),
                                        (color_comp[1]/color_comp[3]),
                                        (color_comp[2]/color_comp[3])))
          color_comp = [0,0,0,0]
          hm_pixel = getPixelAt(heat_map, i, j)
          setColor(hm_pixel, makeColor((k*10),0,0))
          
      cycle_monitor = cycle_monitor + 1        # increment the cycle monitor
      if (cycle_monitor == 10000):             # if the cycle_monitor reaches (x) number of iterations
        cycle_monitor = 0            # reset the cycle_monitor variable
        repaint(target_pic)   # update comp_pic visual
        repaint(heat_map)
        print k             # print k (radius)
        
  if loop_break_flag == true:  # if the processing loop has not engaged for an entire radius cycle
    break                      # break out of the loop and stop processing

print time.time()-start_time
