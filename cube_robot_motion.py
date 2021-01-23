#!/usr/bin/python3
#import subprocess
import time
import sys

# def command(text):
#     process = subprocess.Popen("./step",stdin=subprocess.PIPE)
#     pipe = process.stdin
#     pipe.write(bytes(text, encoding='ascii'))
#     pipe.close()
#     process.wait()# 运行过程避免IO操作（USB、TF等等），容易丢步


# 2021-01-17 更新，解决偶尔丢步问题，定时精度正负1us左右
def command(text):
    # 分段执行，每隔一段时间从内核态返回用户态，可以随时终止程序
    splited_text = text.split(';')
    file_name  = '/dev/step_moter0'
    with open(file_name, 'w') as f:
        #f.write(text)
        for x in splited_text:
            f.write(x)
            f.flush()
            print('.',end='')
            sys.stdout.flush()
            #time.sleep(0.001)
        
    
def decode_cube_str(x):
    direction = None # 1 顺时针 -1 逆时针 2 两圈
    face = None      # U R F D L B
    layer = None     # 1 2 3
    if x[-1] == "'":
        direction = -1
    elif x[-1] == "2":
        direction = 2
    else:
        direction = 1
        
    for item in ('U', 'R', 'F', 'D', 'L', 'B'):
        if item in x:
            face = item
    
    if 'w' in x:
        if x[0] == '2':
            layer = 2
        elif x[0] == '3':
            layer = 3
        else:
            layer = 2
    else:
        layer = 1
    
    return face,layer,direction
    
    
# test = "U' 3Fw' L' 3Bw2 3Uw 3Bw 3Dw' R' 3Fw' 3Rw' 3Dw U Fw' Uw' 3Uw2 F 3Fw2 3Bw2 3Rw2 3Lw' D' 3Fw2 3Lw' 3Rw R2 Rw2 Dw' Lw Uw Lw Fw' Uw' L Fw 3Rw2 F' 3Lw' B' 3Rw' F' 3Bw2 U' 3Lw Lw2 F 3Dw2 3Lw2 Lw' U' 3Dw2 3Bw2 Lw' 3Dw2 U F Bw2 Lw' Rw' F' D' Lw2 U Rw 3Fw2 Uw2 3Bw2 L' Uw2 3Uw2 L 3Uw2 R U2 3Bw2 U2 Fw2 3Fw2 Lw2 3Lw2 Rw2 Fw2 U' Bw2 Uw2 Rw2 F Rw2 3Uw2 B' Uw2 F2 Rw2 Uw2 F 3Lw2 3Dw2 R B L 3Dw2 B' 3Dw2 R D' U2 F 3Uw2 3Rw2 U2 3Lw2 F' L2 3Rw2 D2 F U2 F' B 3Uw2 F2 D 3Lw2 3Rw2 3Fw2 B2 U' L2 U L2 U2 R2 3Fw2 3Rw2 U' 3Fw2 2Uw2 R F' 2Rw2 2Uw2 F2 D R U' U2 2Rw2 U2 B 2Rw2 U2 2Uw2 2Lw2 R2 F' 2Rw2 F B2 2Uw2 2Fw2 2Uw2 U' D' 2Bw2 2Lw2 D' R2 D 2Rw2 U' F2 U' F2 2Lw2 2Fw2 B2 2Bw2 2Lw2 U F B R' L F' B2 U B2 L' F U2 R2 U F2 B2 L2 B2 U B2 U2"
# test = test.split(' ')
# for x in test:
#     face,layer,direction = decode_cube_str(x)
#     print(x,face,layer,direction)

#face_top/front : (f0, f1, cw, ccw, cw2)
cube_dict = {
    'UR': ('RD', 'LU', 'UB', 'UF', 'UL'),
    'UB': ('BD', 'FU', 'UL', 'UR', 'UF'),
    'UL': ('LD', 'RU', 'UF', 'UB', 'UR'),
    'UF': ('FD', 'BU', 'UR', 'UL', 'UB'),
    'RB': ('BL', 'FR', 'RU', 'RD', 'RF'),
    'RD': ('DL', 'UR', 'RB', 'RF', 'RU'),
    'RF': ('FL', 'BR', 'RD', 'RU', 'RB'),
    'RU': ('UL', 'DR', 'RF', 'RB', 'RD'),
    'FR': ('RB', 'LF', 'FU', 'FD', 'FL'),
    'FD': ('DB', 'UF', 'FR', 'FL', 'FU'),
    'FL': ('LB', 'RF', 'FD', 'FU', 'FR'),
    'FU': ('UB', 'DF', 'FL', 'FR', 'FD'),
    'DR': ('RU', 'LD', 'DF', 'DB', 'DL'),
    'DB': ('BU', 'FD', 'DR', 'DL', 'DF'),
    'DL': ('LU', 'RD', 'DB', 'DF', 'DR'),
    'DF': ('FU', 'BD', 'DL', 'DR', 'DB'),
    'LD': ('DR', 'UL', 'LF', 'LB', 'LU'),
    'LB': ('BR', 'FL', 'LD', 'LU', 'LF'),
    'LU': ('UR', 'DL', 'LB', 'LF', 'LD'),
    'LF': ('FR', 'BL', 'LU', 'LD', 'LB'),
    'BR': ('RF', 'LB', 'BD', 'BU', 'BL'),
    'BD': ('DF', 'UB', 'BL', 'BR', 'BU'),
    'BL': ('LF', 'RB', 'BU', 'BD', 'BR'),
    'BU': ('UF', 'DB', 'BR', 'BL', 'BD')}

def can_route(now, need):
    if (need == 'U' or need == 'D') and (now[0] == 'U' or now[0] == 'D'):
        return True
    if (need == 'L' or need == 'R') and (now[0] == 'L' or now[0] == 'R'):
        return True
    if (need == 'F' or need == 'B') and (now[0] == 'F' or now[0] == 'B'):
        return True
    return False

#test = "U' 3Bw R2 3Bw' 3Lw2 U' 3Fw' 3Lw' 3Dw' 3Rw2 3Fw Uw Bw'"

z_now = 0
filp_now = 0
flip_type_now = 1
cube_now = "FL"
exit_flag = False
while True:
    step = []
    test = sys.stdin.readline()
    if not test:
        # 方便取出还原好的魔方
        print('cube solved.')
        step.append('zz')
        step.append('f0')
        exit_flag = True
    else:
        test = test.strip()
        test = test.split()
        
        for item in test:
            # 解析魔方指令
            face,layer,direction = decode_cube_str(item)
            # 将期望的面翻转到上方或者下方
            if can_route(cube_now, face):
                #print(item,'need not route')
                pass
            elif can_route(cube_dict[cube_now][flip_type_now], face):
                #print(item,'need route f0')
                cube_now = cube_dict[cube_now][flip_type_now]
                step.append('z1')
                step.append('zf')
                if flip_type_now == 0:
                    step.append('f0')
                    flip_type_now = 1
                else:
                    step.append('f1')
                    flip_type_now = 0
                #print(cube_now)
            else:
                #print(item,'need route cw f0')
                temp = cube_dict[cube_now][2]
                step.append('z7')
                step.append('cw')
                cube_now = cube_dict[temp][flip_type_now]
                step.append('z1')
                step.append('zf')
                if flip_type_now == 0:
                    step.append('f0')
                    flip_type_now = 1
                else:
                    step.append('f1')
                    flip_type_now = 0
                #print(cube_now)
            # 旋转指令中描述的层
            if cube_now[0] == face:
                if layer == 1:
                    step.append('z1')
                elif layer == 2:
                    step.append('z2')
                elif layer == 3:
                    step.append('z3')
                if direction == 1:
                    step.append('cw')
                elif direction == -1:
                    step.append('ccw')
                elif direction == 2:
                    step.append('cw2')
            else:
                if layer == 1:
                    step.append('z6')
                elif layer == 2:
                    step.append('z5')
                elif layer == 3:
                    step.append('z4')
                if direction == 1:
                    step.append('cw')
                    cube_now = cube_dict[cube_now][2]
                elif direction == -1:
                    step.append('ccw')
                    cube_now = cube_dict[cube_now][3]
                elif direction == 2:
                    step.append('cw2')
                    cube_now = cube_dict[cube_now][4]

    #print(step)
    
    z_list = (162,350,415,480,545,610,675,785)
    text = ""
    for item in step:
        if item == 'zf': # for filp
            if 50 - z_now != 0:
                text = text + "%d,%d;" % (1, 50 - z_now)
            z_now = 50
        elif item == 'zz':
            if z_now != 0:
                text = text + "%d,%d;" % (1, 0 - z_now)
            z_now = 0
        elif item[0] == 'z': # up or down
            num = z_list[ int(item[1]) ]
            if num - z_now != 0:
                text = text + "%d,%d;" % (1, num - z_now)
            z_now = num;
        elif item == 'cw':
            text = text + "3,800;"
        elif item == 'ccw':
            text = text + "3,-800;"
        elif item == 'cw2':
            text = text + "3,1600;"
        elif item == 'ccw2':# cw2 等价于 ccw2
            text = text + "3,-1600;"
        elif item[0] == 'f': # 翻转flip
            if 50 < z_now < 415:
                print("filp not allowed when 50 < z_now < 415")
                pass
            else:
                if item[1] == '0':
                    if filp_now == 1:
                        text = text + "2,-800;"
                        filp_now = 0
                    else:
                        pass
                        #print("filp 0 not allowed")
                elif item[1] == '1':
                    if filp_now == 0:
                        text = text + "2,800;"
                        filp_now = 1
                    else:
                        pass
                        #print("filp 1 not allowed")
        else:
            printf("unknown command",item)


    t1=time.time()
    command(text)
    t2=time.time()
    print("time cost %.2fs"%(t2-t1))
    sys.stdout.flush()
    
    if exit_flag:
        print('exit.')
        break