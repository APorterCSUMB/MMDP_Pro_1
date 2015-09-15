import time          # import the time library for code benchmarking

pic_list = []        # setup an array to hold the pictures being compared
final_comp = []      # setup an array to hold intermediate results
hm_comp = []         # setup an array to hold heat map results

for i in range (3):                          # open up (x) number of pictures
  pic_list.append(makePicture(pickAFile()))  # and put the pictures in the comparison list

start_time = time.time()   # begin timing the code's execution from this point << **BENCHMARK BEGIN**

pic_height = getHeight(pic_list[1])    # get the height of the first picture in the comparison list (should all be same)
pic_width = getWidth(pic_list[1])      # get the width of the first picture in the comparison list (should all be same)
print 'The picture is ' + str(pic_height) + ' pixels high and ' + str(pic_width) + ' pixels wide.'  # HxW console output, formatted
  
comp_pic = makeEmptyPicture(pic_width, pic_height, red)    # make a new HxW picture to hold the intermediate result
heat_map = makeEmptyPicture(pic_width, pic_height, red)  # make a new HxW picture to hold an accuracy heat map

show(comp_pic)  # show the intermediate result as it is being processed
show(heat_map)  # show the heat map as it is generated

cycle_monitor = 0  # "int" counter to handle tasks not necessary every "cycle"

for k in range(255):              # algorithm based on "distance radius" concept, so lets step up to 255 (max distance)
  
  loop_break_flag = true          # bool to track whether we need any more image processing
  
  for i in range(pic_width):      # loop through the height of the picture, H = i
    for j in range(pic_height):   # loop through the wideth of the picture, W = j
    
      new_pixel = getPixelAt(comp_pic, i, j)     # get a pixel object at position (i,j) from comp_pic
      heat_pixel = getPixelAt(heat_map, i, j)    # get a pixel object at position (i,j) from heat_map
      
      
      if(getRed(new_pixel) == 255 and getGreen(new_pixel) == 0 and getBlue(new_pixel) == 0):  # if the pixel in comp_pic is still pure red (needs processing "flag")
      
        loop_break_flag = false                      # tell the algorithm that we are still processing pixel objects this cycle
      
        pixel_1 = getPixelAt(pic_list[0], i, j)      # get a pixel object at position (i,j) from pic_list[0]
        pixel_2 = getPixelAt(pic_list[1], i, j)      # get a pixel object at position (i,j) from pic_list[0]
        pixel_3 = getPixelAt(pic_list[2], i, j)      # get a pixel object at position (i,j) from pic_list[0]
      
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
        
        if distance(pixel_1_color,pixel_2_color) < k:                           # if pixel_1 and pixel_2 have colors within radius k (hit)                                                   
          setColor(heat_pixel, makeColor(2*k, 0, 0))                            # set the Red value of the heat_map pixel to (2) times the value of k
          setColor(new_pixel, makeColor(((pixel_1_red +   pixel_2_red)  /2),    # set the new_pixel color to the average of the pixel_1 and pixel_2 RGB values
                                        ((pixel_1_green + pixel_2_green)/2),
                                        ((pixel_1_blue +  pixel_2_blue) /2)))
        if distance(pixel_2_color,pixel_3_color) < k and hit_flag == false:     # if pixel_2 and pixel_3 have colors within radius k (hit) and this is the first hit
          setColor(heat_pixel, makeColor(2*k, 0, 0))                            # set the Red value of the heat_map pixel to (2) times the value of k
          setColor(new_pixel, makeColor(((pixel_2_red +   pixel_3_red)  /2),    # set the new_pixel color to the average of the pixel_2 and pixel_3 RGB values
                                        ((pixel_2_green + pixel_3_green)/2),
                                        ((pixel_2_blue +  pixel_3_blue) /2)))
        if distance(pixel_1_color,pixel_3_color) < k and hit_flag == false:     # if pixel_1 and pixel_3 have colors within radius k (hit) and this is the first hit
          setColor(heat_pixel, makeColor(2*k, 0, 0))                            # set the Red value of the heat_map pixel to (2) times the value of k
          setColor(new_pixel, makeColor(((pixel_1_red +   pixel_3_red)  /2),    # set the new_pixel color to the average of the pixel_1 and pixel_3 RGB values
                                        ((pixel_1_green + pixel_3_green)/2),
                                        ((pixel_1_blue +  pixel_3_blue) /2)))
                                        
      cycle_monitor = cycle_monitor + 1        # increment the cycle monitor
      if (cycle_monitor == 10000):             # if the cycle_monitor reaches (x) number of iterations
        cycle_monitor = 0            # reset the cycle_monitor variable
        repaint(heat_map)   # update heat_map visual
        repaint(comp_pic)   # update comp_pic visual
        print k             # print k (radius)
      
  if loop_break_flag == true:  # if the processing loop has not engaged for an entire radius cycle
    break                      # break out of the loop and stop processing

file_loc = r"C:\Users\Andrew\Documents\CODE\SCHOOL\MMDP\Project 1\TrialPics\Results\temp.jpg"    # setup a w"r"iteable file path fot the final result
hm_loc = r"C:\Users\Andrew\Documents\CODE\SCHOOL\MMDP\Project 1\TrialPics\Results\hm_temp.jpg"   # setup a w"r"iteable file path for the final heat map
writePictureTo(comp_pic, file_loc)    # write the final result in comp_pic to file_loc
writePictureTo(heat_map, hm_loc)      # write the final heat map in heat_map to hm_loc

print (time.time()-start_time)        # print out the finished execution time << **BENCHMARK END**