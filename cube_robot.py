#!/usr/bin/python3
import subprocess
import time
import datetime
import os

def command(step):
    text = ""
    for x in step:
        text = text + "%d,%d;"%(x[0],x[1])
    file_name  = '/dev/step_moter0'
    with open(file_name, 'w') as f:
        f.write(text)
        f.flush()

    
# m1_pos=(162,350,415,480,545,610,675,785)
# 机械位置回零
command([[0,0]])

import cube_robot_image
print("load cube_robot_image.py done")

cap = cube_robot_image.init_camera()
while True:
    if cube_robot_image.wait_and_prevew_camera(cap) == 27:
        break
    
    file_name = "log/"+datetime.datetime.now().isoformat()+".log"
    print("log file is",file_name)
    
    img = [None]*6
    command([[2,800],[1,162],[1,785-162],[1,-785+162]])
    img[0] = cube_robot_image.cap_img(cap)
    command([[1,785-162],[3,800],[1,-785+162]])
    img[1] = cube_robot_image.cap_img(cap)
    command([[1,785-162],[3,800],[1,-785+162]])
    img[2] = cube_robot_image.cap_img(cap)
    command([[1,785-162],[3,800],[1,-785+162]])
    img[3] = cube_robot_image.cap_img(cap)
    command([[2,-800],[1,785-162],[2,800],[1,-785+162]])
    img[4] = cube_robot_image.cap_img(cap)
    command([[1,785-162],[3,1600],[1,-785+162]])
    img[5] = cube_robot_image.cap_img(cap)
    command([[1,-162],[2,-800]])
    
    cube_str = cube_robot_image.get_cube_string(img)

    print(cube_str)
    os.system("python3 rubiks-cube-solver.py --state %s 2>%s | python3 cube_robot_solve.py" %
              (cube_str, file_name))

    
