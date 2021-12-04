from PIL import Image
import sys

sys.setrecursionlimit(500000)

start_point = [50, 50]
img_array = []
counter_array = []

dopusk = 1

WHITE = [255,255,255]
BLACK = [0,0,0]
RED = (255,0,0)
GREEN = (0,255,0)

img = Image.open('sss.png')
obj = img.load()

color = WHITE

main_arr = [list(obj[x,y]) for y in range(img.height) for x in range(img.width)]

#print(main_arr)

def check_color(pix):
    RGB_R = abs(pix[0] - color[0])
    RGB_G = abs(pix[1] - color[1])
    RGB_B = abs(pix[2] - color[2])
    
#    print(str(RGB_R) + ' ' + str(RGB_G) + ' ' + str(RGB_B))
    
    if RGB_R <= dopusk and RGB_G <= dopusk and RGB_B <= dopusk:
        return True
    else:
#        print('FALSE')
        return False

#print(len(main_arr))


#===============================================================#
def pixel(p_i, p_j):
    return img.width * p_j + p_i
#===============================================================#

def check(p_i, p_j):
#    print('Start check '+str(p_i)+' '+str(p_j))
    if 0 <= p_i < img.width and 0 <= p_j < img.height:
#        print('Passed borders')
        if main_arr[pixel(p_i,p_j)][0] >= 0:
#            print('Pixel '+str(p_i)+' '+str(p_j)+' more than 0')
            if check_color(main_arr[pixel(p_i,p_j)]):
#                print('Pixel '+str(p_i)+' '+str(p_j)+' has ACCEPTED color')
                main_arr[pixel(p_i,p_j)] = (-1, -1, -1)
                img_array.append([p_i, p_j])
                
                check(p_i + 1, p_j)
                check(p_i, p_j + 1)
                check(p_i - 1, p_j)
                check(p_i, p_j - 1)
            else:
#                print('Pixel '+str(p_i)+' '+str(p_j)+' has DECLINE color')
                obj_color = main_arr[pixel(p_i,p_j)]
                main_arr[pixel(p_i,p_j)] = (-2, -2, -2)
#                print('APPEND')
                counter_array.append([[p_i, p_j], obj_color])

#===============================================================#

check(50, 50)

for el in img_array:
    obj[el[0], el[1]] = RED
    
#print(counter_array)
    
for el in counter_array:
    obj[el[0][0], el[0][1]] = GREEN

img.show()
