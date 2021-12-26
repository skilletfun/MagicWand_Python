from PIL import Image
import sys

sys.setrecursionlimit(500000)

#===============================================================#
# Colors and init data
#===============================================================#
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = (255,0,0)
GREEN = (0,255,0)
color = WHITE

start_point = [2, 1]
main_array = []
contour_array = []

dopusk = 1

#===============================================================#
# Open image and generate list with changable items
#===============================================================#
img = Image.open('sss.png')
obj = img.load()

# Fill the array with zeros
img_array = []
for _ in range(img.height):
    temp = []
    for _ in range(img.width):
        temp.append([0,0,0])
    img_array.append(temp)
    
# Fill the array with pixels    
for i in range(img.height):
    for j in range(img.width):
        pix = obj[i,j]
        img_array[i][j] = list(pix)

#===============================================================#
# Check color
#===============================================================#
def check_color(pix):
    RGB_R = abs(pix[0] - color[0])
    RGB_G = abs(pix[1] - color[1])
    RGB_B = abs(pix[2] - color[2])
    
    if RGB_R <= dopusk and RGB_G <= dopusk and RGB_B <= dopusk:
        return True
    else:
        return False

#===============================================================#
# Check pixel color
#===============================================================#
def check(p_i, p_j):
    if 0 <= p_i < img.width and 0 <= p_j < img.height:
        if img_array[p_j][p_i][0] >= 0:
            if check_color(img_array[p_j][p_i]):
                img_array[p_j][p_i] = [-1, -1, -1]
                main_array.append([p_j, p_i])
                check(p_i + 1, p_j)
                check(p_i, p_j + 1)
                check(p_i - 1, p_j)
                check(p_i, p_j - 1)
            else:
                img_array[p_j][p_i] = [-2, -2, -2]
                contour_array.append([p_j, p_i])

#===============================================================#

check(50,50)

for el in main_array:
    obj[el[0], el[1]] = RED
    
for el in contour_array:
    obj[el[0], el[1]] = GREEN

contour_array.sort()

print(contour_array)
#img.show()
img.close()





