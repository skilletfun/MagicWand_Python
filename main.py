from PIL import Image
import sys

sys.setrecursionlimit(500000)

start_point = [50, 50]
img_array = []

dopusk = 5

WHITE = [255,255,255]
BLACK = [0,0,0]
RED = (255,0,0)

img = Image.open('sss.png')
obj = img.load()

color = WHITE

def check_color(pixel):
    RGB_R = abs(pixel[0] - color[0])
    RGB_G = abs(pixel[1] - color[1])
    RGB_B = abs(pixel[2] - color[2])
    
    if RGB_R <= dopusk and RGB_G <= dopusk and RGB_B <= dopusk:
        return True
    else:
        return False

def check(p_i, p_j):
    if 0 <= p_i < img.width and 0 <= p_j < img.height:
        if obj[p_i, p_j][0] >= 0:
            if check_color(obj[p_i, p_j]):
                obj[p_i, p_j] = (-1, -1, -1)
                img_array.append([p_i, p_j])
                
                check(p_i + 1, p_j)
                check(p_i, p_j + 1)
                check(p_i - 1, p_j)
                check(p_i, p_j - 1)


check(50, 50)

for el in img_array:
    obj[el[0], el[1]] = RED

img.show()
#img_array.sort(key=lambda x: x[1])
#
#def get_end_str(value):
#    k = 0
#    for el in img_array:
#        if el[0] == value:
#            k += 1
#        else:
#            return k


#hole = False
#h = img_array[0][1]
#
#pix_stroke = img_array[:get_end_str(h)]
#
#l = len(pix_stroke)
#
#if l > pix_stroke[-1][0] - pix_stroke[0][0]:
#    hole = True
#else:
#    fill_holes






