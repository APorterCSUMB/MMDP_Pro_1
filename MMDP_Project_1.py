import time

pic_list = []
final_comp = []
for i in range (3):
  pic_list.append(makePicture(pickAFile()))

start_time = time.time()
pic_height = getHeight(pic_list[1])
pic_width = getWidth(pic_list[1])

comp_pic = makeEmptyPicture(pic_width, pic_height, red)
heat_map = makeEmptyPicture(pic_width, pic_height, black)

print 'The picture is ' + str(pic_height) + ' pixels high and ' + str(pic_width) + ' pixels wide.'

show(comp_pic)
show(heat_map)
intL = 0

for k in range(250):
  
  loop_break_flag = true
  for i in range(pic_height):
    for j in range(pic_width):
      heat_pixel = getPixelAt(heat_map, j, i)
      new_pixel = getPixelAt(comp_pic, j, i)
      
      if(getRed(new_pixel) == 255 and getGreen(new_pixel) == 0 and getBlue(new_pixel) == 0):
      
        loop_break_flag = false
      
        old_pixel1 = getPixelAt(pic_list[0], j, i)
        old_pixel2 = getPixelAt(pic_list[1], j, i)
        old_pixel3 = getPixelAt(pic_list[2], j, i)
      
        old_pixel1_red = getRed(old_pixel1)
        old_pixel2_red = getRed(old_pixel2)
        old_pixel3_red = getRed(old_pixel3)
      
        old_pixel1_green = getGreen(old_pixel1)
        old_pixel2_green = getGreen(old_pixel2)
        old_pixel3_green = getGreen(old_pixel3)
      
        old_pixel1_blue = getBlue(old_pixel1)
        old_pixel2_blue = getBlue(old_pixel2)
        old_pixel3_blue = getBlue(old_pixel3)
        
        old_pixel1_color = getColor(old_pixel1)
        old_pixel2_color = getColor(old_pixel2)
        old_pixel3_color = getColor(old_pixel3)
      
        if distance(old_pixel1_color,old_pixel2_color) < k:
          setColor(new_pixel, makeColor(((old_pixel1_red + old_pixel2_red)/2),
                                        ((old_pixel1_green + old_pixel2_green)/2),
                                        ((old_pixel1_blue + old_pixel2_blue)/2)))
          setColor(heat_pixel, makeColor(2*k, 0, 0))
        if distance(old_pixel2_color,old_pixel3_color) < k:
          setColor(new_pixel, makeColor(((old_pixel2_red + old_pixel3_red)/2),
                                        ((old_pixel2_green + old_pixel3_green)/2),
                                        ((old_pixel2_blue + old_pixel3_blue)/2)))
          setColor(heat_pixel, makeColor(2*k, 0, 0))
        if distance(old_pixel1_color,old_pixel3_color) < k:
          setColor(new_pixel, makeColor(((old_pixel1_red + old_pixel3_red)/2),
                                        ((old_pixel1_green + old_pixel3_green)/2),
                                        ((old_pixel1_blue + old_pixel3_blue)/2)))
          setColor(heat_pixel, makeColor(2*k, 0, 0))
      intL = intL + 1
      if (intL == 10000):
        intL = 0
        repaint(heat_map)
        repaint(comp_pic)
        print k
      
  if loop_break_flag == true:
    break

file_loc = r"C:\Users\Andrew\Desktop\TrialPics\Results\temp.jpg"
hm_loc = r"C:\Users\Andrew\Desktop\TrialPics\Results\hm_temp.jpg"
writePictureTo(comp_pic, file_loc)
writePictureTo(heat_map, hm_loc)
print (time.time()-start_time)
