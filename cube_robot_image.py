import cv2
import numpy as np
from functools import cmp_to_key

cap = None

# 获取魔方图像
def init_camera():
    cap = cv2.VideoCapture(0)
    if cap.isOpened() != True:
        print("camera error")
        return None
    return cap
    
def cap_img(cap):
    for i in range(8):
        ret,preview = cap.read()
        cv2.imshow("preview", preview)
        k = cv2.waitKey(1)
    cap.grab()
    ret,img = cap.retrieve()
    #cv2.imwrite(file_name+"_1.png", img1)
    return img

def wait_and_prevew_camera(cap):
    cv2.namedWindow('preview')
    cv2.setMouseCallback('preview',mouse)
    while True:
        ret,preview = cap.read()
        cv2.imshow("preview", preview)
        k = cv2.waitKey(1)
        if k != 255:
            #cv2.destroyAllWindows()
            print("cv2.waitKey", k)
            break
    if k == 27:
        cv2.destroyAllWindows()
    return k

def mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("mouse click",x,y)

# 图像处理部分
def four_point_transform(image, rect):
    # 获取坐标点，并将它们分离开来
    # 图像尺寸
    maxWidth = 256
    maxHeight = 256
    # 构建新图片的4个坐标点
    edge = 0
    dst = np.array([
        [edge, edge],
        [maxWidth - 1 - edge, edge],
        [maxWidth - 1 - edge, maxHeight - 1 - edge],
        [edge, maxHeight - 1 - edge]], dtype = "float32")
    # 获取仿射变换矩阵并应用它
    M = cv2.getPerspectiveTransform(rect, dst)
    # 进行仿射变换
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # 返回变换后的结果
    return warped

def mark_cube_one_point(img, x_center, y_center):
    half_size = 10
    color = [0,0,0]
    dot_count = 0
    for y in range(x_center-half_size, x_center+half_size,1):
        for x in range(y_center-half_size, y_center+half_size,1):
            color[0] += img[x,y,0]
            color[1] += img[x,y,1]
            color[2] += img[x,y,2]
            dot_count += 1
    color[0] = int(color[0]/dot_count)
    color[1] = int(color[1]/dot_count)
    color[2] = int(color[2]/dot_count)
    cv2.rectangle(img, (x_center-half_size, y_center-half_size),
                  (x_center+half_size, y_center+half_size), (0,0,0))
    cv2.rectangle(img, (x_center-half_size+1, y_center-half_size+1),
                  (x_center+half_size-1, y_center+half_size-1), (255,255,255))
    #cv2.rectangle(img, (x_center-6, y_center-6),
    #              (x_center+6, y_center+6), color,-1)
    return color

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    m = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g-b)/m)*60
        else:
            h = ((g-b)/m)*60 + 360
    elif mx == g:
        h = ((b-r)/m)*60 + 120
    elif mx == b:
        h = ((r-g)/m)*60 + 240
    if mx == 0:
        s = 0
    else:
        s = m/mx
    v = mx
    # h,s,v,值的范围分别是0-360, 0-1, 0-1
    return h, s, v

def mark_cube(img,face):
    color_line = (0,0,0)
    colors = [0]*49
    i = 0
    for y in (32,64,96,128,160,192,224):
        for x in (32,64,96,128,160,192,224):
            colors[i] = mark_cube_one_point(img,x,y)
            i += 1
            
    #cv2.putText(img,str(face), (128-20,128-20), cv2.FONT_HERSHEY_DUPLEX,1,color_line)
    hsv = [0]*49
    for i in range(0,49):
        h,s,v = rgb2hsv(colors[i][2], colors[i][1], colors[i][0]);
        hsv[i] = [h,s,v,face*49 + i]
        
    return hsv

def class_color(hsv_49x5):
    min_std_shift = 0;
    min_std = 1000; # 0 - 360
    hsv_49x5_only_h = []
    for x in hsv_49x5:
        hsv_49x5_only_h.append(x[0])
    
    for shift in range(0,49):
        hsv_49x5_shift = list(hsv_49x5_only_h)
        for i in range(0, shift):
            hsv_49x5_shift[i] += 360
        hsv_49x5_shift = hsv_49x5_shift[shift:49*5] + hsv_49x5_shift[0:shift]
        
        std = [0] * 5
        for i in range(0,5):
            std[i] = np.std(hsv_49x5_shift[i * 49 : i * 49 + 49])
        std_mean = np.mean(std)
        
        if std_mean < min_std:
            min_std_shift = shift
            min_std = std_mean
            
    print("min_std_shift =",min_std_shift,"min_std =",min_std)
    return hsv_49x5[min_std_shift:49*5] + hsv_49x5[0:min_std_shift] 

def get_cube_string(img):
    img[0],img[1],img[2],img[3],img[4],img[5] = img[0],img[3],img[5],img[2],img[1],img[4] 
    pts1 = np.array([[112,35],[517,39],[510,445],[105,440]], dtype = "float32")
    hsv_6_face = []
    angle_list = [180, 90, -90, 0, -90, 90]
    for i in range(6):
        img[i] = four_point_transform(img[i], pts1)
        matRotate = cv2.getRotationMatrix2D((256*0.5, 256*0.5), angle_list[i], 1.0) 
        img[i] = cv2.warpAffine(img[i], matRotate, (256, 256))
        hsv_6_face.extend(mark_cube(img[i],i))

    #根据饱和度挑出白色
    #cube_string = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    cube_string = ['?']*(49*6)
    cube_string_kociemba = ['?']*(49*6)
    hsv_6_face = sorted(hsv_6_face, key=cmp_to_key(lambda x,y: x[1] - y[1]))
    for i in hsv_6_face[0:49]:
        cube_string[i[3]] = 'W'
    #根据色调分离其他颜色
    hsv_6_face = sorted(hsv_6_face[49:], key=cmp_to_key(lambda x,y: x[0] - y[0]))
    hsv_6_face = class_color(hsv_6_face)
    for i in hsv_6_face[0:49]:
        cube_string[i[3]] = 'O'
    for i in hsv_6_face[49:98]:
        cube_string[i[3]] = 'Y'
    for i in hsv_6_face[98:147]:
        cube_string[i[3]] = 'G'
    for i in hsv_6_face[147:196]:
        cube_string[i[3]] = 'B'
    for i in hsv_6_face[196:245]:
        cube_string[i[3]] = 'R'

    # 用于评估效果的图像
    null_img = np.zeros((256, 256, 3), np.uint8)
    row1 = np.hstack((null_img, img[0], null_img, null_img))
    row2 = np.hstack((img[4],   img[2], img[1],   img[5]))
    row3 = np.hstack((null_img, img[3], null_img, null_img))
    img_6in1 = np.vstack((row1, row2, row3))
    color_dict = {'R':(0,0,255), 'G':(0,255,0), 'B':(255,0,0),
                  'O':(0,192,255), 'Y':(0,255,255), 'W':(255,255,255)}
    offset = ((1,0),(2,1),(1,1),(1,2),(0,1),(3,1))
    for i in range(49*6):
        size = 11
        face = i // 49
        index = i % 49
        x = (offset[face][0]*7 + index % 7 )* size + 620
        y = (offset[face][1]*7 + index // 7 )* size + 520
        cv2.rectangle(img_6in1,(x,y),(x+size-1,y+size-1),color_dict[cube_string[i]], -1)
    
    cv2.destroyAllWindows()
    cv2.imshow("cube", img_6in1)
    cv2.namedWindow('cube')
    k = cv2.waitKey(300)
    #cv2.setMouseCallback('cube',mouse)

    # RGBWOY -> URFDLB
    u_color = cube_string[49*0+24]
    r_color = cube_string[49*1+24]
    f_color = cube_string[49*2+24]
    d_color = cube_string[49*3+24]
    l_color = cube_string[49*4+24]
    b_color = cube_string[49*5+24]
    for i in range(0,49*6):
        if cube_string[i] == u_color:
            cube_string_kociemba[i] = 'U'
        elif cube_string[i] == r_color:
            cube_string_kociemba[i] = 'R'
        elif cube_string[i] == f_color:
            cube_string_kociemba[i] = 'F'
        elif cube_string[i] == d_color:
            cube_string_kociemba[i] = 'D'
        elif cube_string[i] == l_color:
            cube_string_kociemba[i] = 'L'
        elif cube_string[i] == b_color:
            cube_string_kociemba[i] = 'B'
    cube_string_kociemba = ''.join(cube_string_kociemba)
    return cube_string_kociemba
