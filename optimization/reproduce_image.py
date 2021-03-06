import random

import sys

import os
from PIL import Image
from decimal import *

here = sys.path[0]
getcontext().prec = 20
num = 0
gen_x_width = 0
gen_y_width = 0
cross_rate = 1
variation_rate = 0.0001
px = None
step = 0

class blackc():
    def __init__(self, x,y,adaptive):
        self.x = x
        self.y = y
        self.gen_x = bin(x).replace("0b","").zfill(gen_x_width)
        self.gen_y = bin(y).replace("0b","").zfill(gen_y_width)
        self.adaptive = adaptive
        self.fertile = True    #新生无法繁殖要到下一代

    def set_selection_probability(self,selection_probability):
        self.selection_probability = selection_probability.quantize(Decimal('0.00000000000000000000'))


    def set_cumulative_probability(self,floor,ceil):
        self.floor = floor
        self.ceil = ceil

    def is_select(self,num):
        if num >= self.floor and num < self.ceil:
            return True
        else:
            return False

    def reset(self, x,y,adaptive):
        self.x = x
        self.y = y
        self.gen_x = bin(x).replace("0b","").zfill(gen_x_width)
        self.gen_y = bin(y).replace("0b","").zfill(gen_y_width)
        self.adaptive = adaptive

def generate_pic(i,seta):
    im = Image.open('pic.jpg')
    new_px = im.load()
    for blackcc in seta:
        x = blackcc.x
        y = blackcc.y
        new_px[x,y] = (0, 255, 0)
        if i == 100:
            print(px[x, y])

    im.save(os.path.join(here,"pic","{}.jpg".format(i)))

def adaptive(RGB):
    return 0.299*RGB[0] + 0.587*RGB[1] + 0.114*RGB[2]

def generate_first_generation(width,height):
    seta = list()
    while seta.__len__() != num:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        blackcc = blackc(x,y,adaptive(px[x,y]))
        seta.append(blackcc)
    return seta

def select(last_generation):
    select_generation = list()  # 被选中繁殖的那群物种
    while select_generation.__len__() != num:
        chooice = Decimal(random.uniform(0, 1)).quantize(Decimal('0.00000000000000000000'))
        for i in last_generation:
            if i.is_select(chooice):
                select_generation.append(i)
                break
    return select_generation

def oh_babay(select_generation):
    for i in range(int(select_generation.__len__()/2*cross_rate)):    #根据交叉率决定交叉几次
        father = select_generation[random.randint(0,select_generation.__len__()-1)]  #随机选择父亲
        while not father.fertile:       #假如挑选的是被交叉出来的子代，则重新选择
            father = select_generation[random.randint(0, select_generation.__len__()-1)]  # 随机选择父亲

        mother = select_generation[random.randint(0, select_generation.__len__()-1)]  # 随机选择母亲
        while not mother.fertile:  # 假如挑选的是被交叉出来的子代，则重新选择
            mother = select_generation[random.randint(0, select_generation.__len__()-1)]  # 随机选择母亲

        #交叉操作
        father_gen_x = father.gen_x
        mother_gen_x = mother.gen_x

        while(1):
            start_index = random.randint(0, gen_x_width)
            num = random.randint(0, gen_x_width-start_index)

            father_gen_x = father.gen_x
            mother_gen_x = mother.gen_x

            father_part = father_gen_x[start_index:start_index+num+1]
            mother_part = mother_gen_x[start_index:start_index + num + 1]
            # 交换基因

            mother_gen_x = mother_gen_x[:start_index]+father_part+mother_gen_x[start_index+num+1:]
            father_gen_x = father_gen_x[:start_index]+mother_part+father_gen_x[start_index+num+1:]
            if int(mother_gen_x,2) < width and int(father_gen_x,2) < width:
                break

        father_gen_y = father.gen_y
        mother_gen_y = mother.gen_y
        while(1):
            start_index = random.randint(0, gen_y_width)
            num = random.randint(0, gen_y_width - start_index)

            father_gen_y = father.gen_y
            mother_gen_y = mother.gen_y

            father_part = father_gen_y[start_index:start_index + num + 1]
            mother_part = mother_gen_y[start_index:start_index + num + 1]
            # 交换基因

            mother_gen_y = mother_gen_y[:start_index] + father_part + mother_gen_y[start_index + num + 1:]
            father_gen_y = father_gen_y[:start_index] + mother_part + father_gen_y[start_index + num + 1:]
            if int(mother_gen_y,2) < height and int(father_gen_y,2) < height:
                break

        father_new_x = int(father_gen_x,2)
        mother_new_x =  int(mother_gen_x,2)

        father_new_y = int(father_gen_y,2)
        mother_new_y = int(mother_gen_y,2)

        father.reset(father_new_x,father_new_y,adaptive(px[father_new_x,father_new_y]))         #新的基因
        mother.reset(mother_new_x,mother_new_y,adaptive(px[mother_new_x,mother_new_y]))
    return select_generation

def variation(select_generation):
    for i in range(int(variation_rate*select_generation.__len__()*gen_x_width)):
        chooice_x = random.randint(0, select_generation.__len__() - 1)
        gen_x = select_generation[chooice_x].gen_x
        list_gen_x = list(gen_x)

        gen_x_index = random.randint(0,gen_x_width-1)

        if list_gen_x[gen_x_index] == '0':
            list_gen_x[gen_x_index] = '1'
        else:
            list_gen_x[gen_x_index] = '0'

        x = int(''.join(list_gen_x),2)
        y = select_generation[chooice_x].y
        if x < width and y < height:
            select_generation[chooice_x].reset(x,y,adaptive(px[x,y]))

    for i in range(int(variation_rate * select_generation.__len__() * gen_y_width)):
        chooice_y = random.randint(0, select_generation.__len__() - 1)
        gen_y = select_generation[chooice_y].gen_x
        list_gen_y = list(gen_y)

        gen_y_index = random.randint(0, gen_y_width - 1)

        if list_gen_y[gen_y_index] == '0':
            list_gen_y[gen_y_index] = '1'
        else:
            list_gen_y[gen_y_index] = '0'

        x = select_generation[chooice_y].x
        y = int(''.join(list_gen_y), 2)
        if x < width and y < height:
            select_generation[chooice_y].reset(x,y,adaptive(px[x,y]))
    return select_generation

def survival_of_the_fittest(last_generation,width,height):
    #准备阶段，算出选择概论和积累概率
    total_adaptive = 1             #总适应度
    for i in last_generation:
        total_adaptive += i.adaptive
    # print(total_adaptive)

    for i in last_generation:
        i.set_selection_probability(Decimal(i.adaptive)/Decimal(total_adaptive))

    pre = 0
    for i in last_generation:
        i.set_cumulative_probability(pre,pre+i.selection_probability)
        pre = pre + i.selection_probability

    generate_pic(step, last_generation)
    print("照射率：{}%".format((total_adaptive-1)/(num*255)*100))

    # 选择
    step_1 = select(last_generation)

    # 父代交叉，交配吧
    step_2 = oh_babay(step_1)

    #变异
    step_3 = variation(step_2)

    #新生代成熟，从而在下一次能够被选中交配
    for i in step_3:
        i.fertile = True

    return step_3


if __name__ == '__main__':
    if not os.path.exists(os.path.join(here,"pic")):
        os.makedirs(os.path.join(here,"pic"))
    im = Image.open(os.path.join(here,'pic.jpg'))
    px = im.load()
    width, height = im.size
    num = int(width*height/3)
    # print(num)

    gen_x_width = bin(width).replace("0b","").__len__()
    gen_y_width = bin(width).replace("0b","").__len__()

    current_generation = generate_first_generation(width,height)          #第一代

    for i in range(10):
        new_generation = survival_of_the_fittest(current_generation,width,height)        #适者生存产生新的一代
        current_generation = new_generation
        step += 1
