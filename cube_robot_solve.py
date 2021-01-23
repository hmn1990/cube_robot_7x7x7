#!/usr/bin/python3
import time
import sys
import subprocess
#python3 rubiks-cube-solver.py --state XXX  2>/dev/null | python3 cube_robot_solve.py 


def solve_cube():
    process = subprocess.Popen(['taskset', '-c', '3', 'python3', 'cube_robot_motion.py'], stdin=subprocess.PIPE)
    pipe = process.stdin
    
    steps_555_LR_centers_staged = 0
    steps_555_FB_centers_staged = 0
    steps_555_edges_EOed = 0
    steps_555_first_four_edges_staged = 0
    steps_555_first_four_edges_paired = 0
    steps_555_last_eight_edges_paired = 0
    all_steps = []

#     def w_to_3w(x):
#         for i in range(len(x)):
#             if 'w' in x[i]:
#                 x[i] = '3' + x[i]
#     def w_to_2w(x):
#         for i in range(len(x)):
#             if 'w' in x[i]:
#                 x[i] = '2' + x[i]
    len_old = 0;
    while True:
        line = sys.stdin.readline()
        #print('input',line)
        if not line:
            break
        if "Solution" in line:
            steps = line.split(":")[-1].strip().split(' ')
            solution_id = line.split(":")[0]
            totel_comment = 0
            index_last = 0
            index_CENTERS_SOLVED = 0
            # 截取最新的部分
            for i in range(len(steps)):
                if 'COMMENT' in steps[i]:
                    totel_comment += 1
                    if i != len(steps) - 1:
                        index_last = i + 1
                if 'CENTERS_SOLVED' in steps[i]:
                    index_CENTERS_SOLVED = i + 1
            if totel_comment == 0:
                print("!!! Find solution:", ' '.join(steps))
                if steps != all_steps:
                    print("solution should be:", ' '.join(all_steps))
                    raise Exception("read rubiks-cube-NxNxN-solver steps error.")
            else:
                if solution_id != 'Solution':
                    if len_old != len(steps):
                        len_old = len(steps) #偶尔会出现操作步骤为0的情况，忽略这种
                        comment = steps[-1]
                        steps = steps[index_last:-1]
                        all_steps += steps
                        to_write = ' '.join(steps)
                        pipe.write(bytes( to_write + '\n' , encoding='ascii'))
                        pipe.flush()
                        print("!!! %s: %s"%(solution_id, to_write))
                else:
                    steps = steps[index_CENTERS_SOLVED:-1]
                    steps_temp = []
                    for step in steps:
                        if 'COMMENT' not in step and 'EDGES_GROUPED' not in step:
                            steps_temp.append(step)
                    all_steps += steps_temp
                    to_write = ' '.join(steps_temp)
                    pipe.write(bytes( to_write + '\n' , encoding='ascii'))
                    pipe.flush()
                    print("!!! %s: %s"%(solution_id, to_write))
                    pass
    pipe.close()
    process.wait()
    
# read stdin
solve_cube()




