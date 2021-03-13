import math
import time
from tkinter import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np
from Models import Electrical_Bus, Transformator_Z_T_11, SM, Static_load, Electrical_system, AM, KZ_Bus, KZ_single_phase

def create_image_for_menu(pass_obj):
    buff_image = ImageTk.PhotoImage(Image.open(pass_obj))
    width_image = buff_image.width()/10
    image = ImageTk.PhotoImage(Image.open(pass_obj).resize((int(width_image), int((width_image)*buff_image.height()/buff_image.width())), Image.ANTIALIAS))
    #imagesprite2 = canv.create_image(WIDTH/2,HEIGHT/2,image=image2)
    return image

state_enter_parameter = 0
state_menu = False
mouse_x = 0
mouse_y = 0
main_det = []
max_width_voltage_per_bus = []
all_voltage_matrix = []
all_current_matrix = []
y0 = []
test_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
n_fig = 0
t_max = 3
t_del = 500000
t = np.linspace(0, t_max, t_del)

root = Tk() 
root.title("Сборка моделе")
root.state('zoomed')
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
frame=Frame(root,width=WIDTH,height=HEIGHT)
frame.pack(expand=True, fill=BOTH)
canv = Canvas(frame, scrollregion=(0,0,0,0), width = WIDTH, height = HEIGHT, bg = "white", cursor = "pencil")

#canv.create_text(WIDTH/2, HEIGHT/2, text = "Трансформатор", fill = "black", font = ("GOST Type A", "12"), anchor="ne")
mass_model = []
mass_model.append([]) #mass_Electrical_Bus
mass_model.append([]) #mass_Transformator_Z_T_11
mass_model.append([]) #mass_SM
mass_model.append([]) #mass_Static_load
mass_model.append([]) #mass_Electrical_system
mass_model.append([]) #mass_AM
mass_model.append([]) #mass_KZ_Bus
mass_model.append([]) #mass_KZ_single_phase
example_for_menu = [Electrical_Bus(2*WIDTH, 2*HEIGHT, canv, root),
                   Transformator_Z_T_11(2*WIDTH, 2*HEIGHT, canv, root),
                   SM(2*WIDTH, 2*HEIGHT, canv, root),
                   AM(2*WIDTH, 2*HEIGHT, canv, root),
                   Static_load(2*WIDTH, 2*HEIGHT, canv, root),
                   Electrical_system(2*WIDTH, 2*HEIGHT, canv, root),
                   KZ_Bus(2*WIDTH, 2*HEIGHT, canv, root),
                   KZ_single_phase(2*WIDTH, 2*HEIGHT, canv, root)
]
mass_image_menu_data = [create_image_for_menu("Image/Main menu/Electrical_Bus.png"),
create_image_for_menu("Image/Main menu/Transformator_Z_T_11.png"),
create_image_for_menu("Image/Main menu/SM.png"),
create_image_for_menu("Image/Main menu/AM.png"),
create_image_for_menu("Image/Main menu/Static_load.png"),
create_image_for_menu("Image/Main menu/Electrical_system.png"),
create_image_for_menu("Image/Main menu/KZ_three_phase.png"),
create_image_for_menu("Image/Main menu/KZ_single_phase.png")
]
mass_image_menu = [canv.create_image(2*WIDTH, 2*HEIGHT ,image = mass_image_menu_data[0], anchor = 'nw'),
canv.create_image(2*WIDTH, 2*HEIGHT ,image =  mass_image_menu_data[1], anchor = 'nw'),
canv.create_image(2*WIDTH, 2*HEIGHT ,image =  mass_image_menu_data[2], anchor = 'nw'),
canv.create_image(2*WIDTH, 2*HEIGHT ,image =  mass_image_menu_data[3], anchor = 'nw'),
canv.create_image(2*WIDTH, 2*HEIGHT ,image =  mass_image_menu_data[4], anchor = 'nw'),
canv.create_image(2*WIDTH, 2*HEIGHT ,image =  mass_image_menu_data[5], anchor = 'nw'),
canv.create_image(2*WIDTH, 2*HEIGHT ,image =  mass_image_menu_data[6], anchor = 'nw'),
canv.create_image(2*WIDTH, 2*HEIGHT ,image =  mass_image_menu_data[7], anchor = 'nw')
]
width_object_menu = create_image_for_menu("Image/Main menu/Electrical_Bus.png").width()

def return_graph():
    for m in range(len(mass_model)):
        for i in range(len(mass_model[m])):
            if (mass_model[m][i] != 0):
                if (m == 0):
                    mass_model[m][i].y -= HEIGHT
                    canv.coords(mass_model[m][i].image_model, mass_model[m][i].x, mass_model[m][i].y)
                    canv.coords(mass_model[m][i].model_text, mass_model[m][i].x, mass_model[m][i].y)
                else:
                    if (mass_model[m][i].state_change_parameter == 1):
                        for n in range(len(mass_model[m][i].mass_canv_text)):
                            canv.delete(mass_model[m][i].mass_canv_text[n])
                        for n in range(len(mass_model[m][i].var_text)):
                            mass_model[m][i].mass_entry[n].delete(0, END)
                            mass_model[m][i].mass_entry[n].pack()
                            mass_model[m][i].state_change_parameter = 0
                        mass_model[m][i].list_example.place(x = WIDTH/2, y = HEIGHT)
                    mass_model[m][i].y -= HEIGHT
                    canv.coords(mass_model[m][i].image_model, mass_model[m][i].x, mass_model[m][i].y) 

def graphics(w_index, num):
    global n_fig
    global ww
    global t
    if (num == 1):
        Iat = []
        for i in range(len(t)):
            Iat.append(-ww[:, 0 + w_index][i] + ww[:, 2 + w_index][i])
        plt.figure(n_fig)
        plt.subplot(1, 1, 1)
        n_fig += 1
        plt.plot(t, Iat, linewidth=1, color='red', label = 'Ток фазы А на стороне треугольника')
        plt.plot(t, ww[:, 3 + w_index], linewidth=1, color='blue', label = 'Ток фазы А на стороне звезды')
        plt.xlabel('Время, с', fontsize=12, color='black')
        plt.ylabel('Токи, А', fontsize=12, color='black')
        plt.legend()
        plt.grid(True)

        plt.show()
    if (num == 2):
        plt.figure(n_fig)
        plt.subplot(2, 1, 1)
        n_fig += 1
        plt.plot(t, ww[:, 0 + w_index], linewidth=1, color='red')
        plt.xlabel('Время, с', fontsize=12, color='black')
        plt.ylabel('Ток фазы А, А', fontsize=12, color='black')
        plt.grid(True)
        
        f_g = []

        for i in range(len(t)):
            f_g.append(ww[:, 3 + w_index][i]/2/math.pi)

        plt.subplot(2, 1, 2)
        plt.plot(t, f_g, linewidth=1, color='red')
        plt.xlabel('Время, с', fontsize=12, color='black')
        plt.ylabel('Частота, Гц', fontsize=12, color='black')
        plt.grid(True)

        delta_mass = []
        for i in range(len(t)):
            delta_mass.append(ww[:, 4 + w_index][i]*180/math.pi - 360*50*t[i])

        plt.figure(n_fig)
        plt.subplot(2, 1, 1)
        n_fig += 1
        plt.plot(t, ww[:, 2 + w_index], linewidth=1, color='red')
        plt.xlabel('Время, с', fontsize=12, color='black')
        plt.ylabel('Ток возбуждения, А', fontsize=12, color='black')
        plt.grid(True)
        plt.subplot(2, 1, 2)
        plt.plot(t, delta_mass, linewidth=1, color='red')
        plt.xlabel('Время, с', fontsize=12, color='black')
        plt.ylabel('Взаимный угол, градус', fontsize=12, color='black')
        plt.grid(True)
        plt.show()

    if (num == 5):
        plt.figure(n_fig)
        plt.subplot(3, 1, 1)
        n_fig += 1
        plt.plot(t, ww[:, 0 + w_index], linewidth=1, color='red')
        plt.xlabel('Время, с', fontsize=12, color='black')
        plt.ylabel('Ток фазы А статора, А', fontsize=12, color='black')
        plt.grid(True)

        plt.subplot(3, 1, 2)
        plt.plot(t, ww[:, 3 + w_index], linewidth=1, color='red')
        plt.xlabel('Время, с', fontsize=12, color='black')
        plt.ylabel('Ток фазы А ротора, А', fontsize=12, color='black')
        plt.grid(True)

        f_g = []

        for i in range(len(t)):
            f_g.append(ww[:, 6 + w_index][i]/2/math.pi)

        plt.subplot(3, 1, 3)
        plt.plot(t, f_g, linewidth=1, color='red')
        plt.xlabel('Время, с', fontsize=12, color='black')
        plt.ylabel('Частота вращения ротора, Гц', fontsize=12, color='black')
        plt.grid(True)

        plt.show()

def delete_model(event):
    for m in mass_model:
        for i in range(len(m)):
            if (m[i] != 0):         
                if (m[i].state_click == 1):
                    m.insert(i, 0)
                    del m[i + 1]
                    #print(m)

def click_1(event):
    global state_menu
    if (state_menu == True):
        state_menu = False
        index_return_element = 0
        for i in range(len(example_for_menu)):
            if (example_for_menu[i].menu_click(event.x, event.y, width_object_menu) == True):
                index_return_element = i
        print(index_return_element)
        for i in range(len(example_for_menu)):
            canv.coords(mass_image_menu[i], WIDTH*1, HEIGHT*1)

        for m in range(len(mass_model)):
            for i in range(len(mass_model[m])):
                if (mass_model[m][i] != 0):
                    if (m == 0):
                        mass_model[m][i].y -= HEIGHT
                        canv.coords(mass_model[m][i].image_model, mass_model[m][i].x, mass_model[m][i].y)
                        canv.coords(mass_model[m][i].model_text, mass_model[m][i].x, mass_model[m][i].y)
                    else:
                        mass_model[m][i].y -= HEIGHT
                        canv.coords(mass_model[m][i].image_model, mass_model[m][i].x, mass_model[m][i].y) 

        if (index_return_element == 0):
            mass_model[0].append(Electrical_Bus(WIDTH*2, HEIGHT*2, canv, root))
        if (index_return_element == 1):
            mass_model[1].append(Transformator_Z_T_11(WIDTH*2, HEIGHT*2, canv, root))
        if (index_return_element == 2):
            mass_model[2].append(SM(WIDTH*2, HEIGHT*2, canv, root))
        if (index_return_element == 3):
            mass_model[3].append(AM(WIDTH*2, HEIGHT*2, canv, root))
        if (index_return_element == 4):
            mass_model[4].append(Static_load(WIDTH*2, HEIGHT*2, canv, root))
        if (index_return_element == 5):
            mass_model[5].append(Electrical_system(WIDTH*2, HEIGHT*2, canv, root))
        if (index_return_element == 6):
            mass_model[6].append(KZ_Bus(WIDTH*2, HEIGHT*2, canv, root))
        if (index_return_element == 7):
            mass_model[7].append(KZ_single_phase(WIDTH*2, HEIGHT*2, canv, root))
        if (index_return_element == 0):
            mass_model[0][-1].state_click = 1
            mass_model[0][-1].delta_x = 5
            mass_model[0][-1].delta_y = 5
        else:
            mass_model[index_return_element][-1].state_click = 1
            mass_model[index_return_element][-1].delta_x = mass_model[index_return_element][-1].k_click*mass_model[index_return_element][-1].image_width + 5
            mass_model[index_return_element][-1].delta_y = mass_model[index_return_element][-1].k_click*mass_model[index_return_element][-1].image_height + 5

    if (state_menu == False):
        for m in mass_model:
            for i in range(len(m)):
                if (m[i] != 0):
                    m[i].set_state_click(event.x, event.y)
        for i in mass_model[0]:
            if (i != 0):
                i.control_connection(mass_model)
                print(i.list_connection)
def mouse_motion(event):
    global mouse_x
    global mouse_y
    mouse_x = event.x
    mouse_y = event.y
    for m in mass_model:
        for i in range(len(m)):
            if (m[i] != 0):
                m[i].move_model(event.x, event.y)

def expand_bus(event):
    for i in mass_model[0]:
        if (i != 0):
            i.expand_image_model(event.x, event.y)

def click_2(event):
    global n_fig
    global t
    for m in range(len(mass_model)):
        if (m != 0):
            for i in range(len(mass_model[m])):
                if (mass_model[m][i] != 0):
                    if (mass_model[m][i].view_result(event.x, event.y) == True):
                        w_index = 0
                        for j in help_matrix:
                            if ((j[0] == m) and (j[1] == i)):
                                break
                            if (j[0] == 1):
                                w_index += 6
                            if (j[0] == 2):
                                w_index += 5
                            if (j[0] == 3):
                                w_index += 3
                            if (j[0] == 4):
                                w_index += 3
                            if (j[0] == 5):
                                w_index += 8
                            if (j[0] == 6):
                                w_index += 3
                            if (j[0] == 7):
                                w_index += 1
                        graphics(w_index, m)
    
    for i in range(len(mass_model[0])):
        if (mass_model[0][i] != 0):
            if (mass_model[0][i].view_result(event.x, event.y) == True):
                for j in range(len(help_matrix_bus)):
                    if (help_matrix_bus[j][0] == i):
                        data_graphics = voltage_bus[j][0:]
                plt.figure(n_fig)
                plt.subplot(1, 1, 1)
                n_fig += 1
                plt.plot(t_d, data_graphics[0], linewidth=1, color='red')
                plt.xlabel('Время, с', fontsize=12, color='black')
                plt.ylabel('Напряжения, В', fontsize=12, color='black')
                plt.grid(True)

                plt.show()


def change_parameter(event):
    global state_enter_parameter
    state = 0
    state_enter_parameter = 1
    for m in range(len(mass_model)):
        for i in range(len(mass_model[m])):
            if (mass_model[m][i] != 0):
                if (m == 0):
                    mass_model[m][i].y += HEIGHT
                    canv.coords(mass_model[m][i].image_model, mass_model[m][i].x, mass_model[m][i].y)
                    canv.coords(mass_model[m][i].model_text, mass_model[m][i].x, mass_model[m][i].y)
                else:
                    mass_model[m][i].change_parameter_in_model(mouse_x, mouse_y, WIDTH)
                    mass_model[m][i].y += HEIGHT
                    canv.coords(mass_model[m][i].image_model, mass_model[m][i].x, mass_model[m][i].y)

    for m in range(len(mass_model)):
        for i in range(len(mass_model[m])):
            if (mass_model[m][i] != 0):
                if (m != 0):
                    if (mass_model[m][i].state_change_parameter == 1):
                        state += 1
    print(state)
    if (state == 0):
        return_graph() 

def enter_inf(event):
    global state_enter_parameter
    state_enter_parameter = 0
    for m in range(len(mass_model)):
        for i in range(len(mass_model[m])):
            if (mass_model[m][i] != 0):
                if (m != 0):
                    if (mass_model[m][i].state_change_parameter == 1):
                        mass_model[m][i].set_parameter_in_model()
    return_graph() 

def set_potation_position(event):
    for m in range(len(mass_model)):
        for i in range(len(mass_model[m])):
            if (mass_model[m][i] != 0):
                mass_model[m][i].rotation(mouse_x, mouse_y) 

def start(event):
    global ww
    global voltage_bus
    global t_d
    voltage_bus = []
    t_d = []
    get_time_interrupt()
    get_y0()
    get_all_U_and_I_matrix()
    ww = odeint(f, y0, t)


def add_Electrical_Bus(event):
    global state_enter_parameter
    if (state_enter_parameter == 0):
        mass_model[0].append(Electrical_Bus(mouse_x, mouse_y, canv, root))
def add_Transformator_Z_T_11(event):
    global state_enter_parameter
    if (state_enter_parameter == 0):
        mass_model[1].append(Transformator_Z_T_11(mouse_x, mouse_y, canv, root))
def add_SM(event):
    global state_enter_parameter
    if (state_enter_parameter == 0):
        mass_model[2].append(SM(mouse_x, mouse_y, canv, root))
def add_Static_load(event):
    global state_enter_parameter
    if (state_enter_parameter == 0):
        mass_model[3].append(Static_load(mouse_x, mouse_y, canv, root))
def add_Electrical_system(event):
    global state_enter_parameter
    if (state_enter_parameter == 0):
        mass_model[4].append(Electrical_system(mouse_x, mouse_y, canv, root))
def add_AM(event):
    global state_enter_parameter
    if (state_enter_parameter == 0):
        mass_model[5].append(AM(mouse_x, mouse_y, canv, root))
def add_KZ_Bus(event):
    global state_enter_parameter
    if (state_enter_parameter == 0):
        mass_model[6].append(KZ_Bus(mouse_x, mouse_y, canv, root))
def add_KZ_single_phase(event):
    global state_enter_parameter
    if (state_enter_parameter == 0):
        mass_model[7].append(KZ_single_phase(mouse_x, mouse_y, canv, root))

def main_menu(event):
    global state_menu
    state_menu = True
    colomn = 6
    size_empty_space = 10
    x_start = (WIDTH - width_object_menu*colomn - (colomn-1)*size_empty_space)/2
    y_start = 50
    for m in range(len(mass_model)):
        for i in range(len(mass_model[m])):
            if (mass_model[m][i] != 0):
                if (m == 0):
                    mass_model[m][i].y += HEIGHT
                    canv.coords(mass_model[m][i].image_model, mass_model[m][i].x, mass_model[m][i].y)
                    canv.coords(mass_model[m][i].model_text, mass_model[m][i].x, mass_model[m][i].y)
                else:
                    mass_model[m][i].y += HEIGHT
                    canv.coords(mass_model[m][i].image_model, mass_model[m][i].x, mass_model[m][i].y)
    for i in range(len(example_for_menu)):
        if ((i)%colomn == 0):
            x = x_start + i*width_object_menu - i//colomn*colomn*width_object_menu
        else:
            x = x_start + i*(width_object_menu + size_empty_space) - i//colomn*colomn*width_object_menu - i//colomn*colomn*size_empty_space
        example_for_menu[i].x_menu = x
        example_for_menu[i].y_menu = (i)//colomn*(size_empty_space + width_object_menu) + y_start
        canv.coords(mass_image_menu[i], x, (i)//colomn*(size_empty_space + width_object_menu) + y_start)

def add_zero_matrix(w_matrix, h_matrix):
    global main_det
    buff_matrix = []
    if (len(main_det) == 0):
        for i in range(w_matrix):
            buff_matrix.append(0)
        for i in range(h_matrix):
            main_det.append(buff_matrix[0:])
    else:
        for i in range(len(main_det[-1])):
            buff_matrix.append(0)
        for i in range(h_matrix):
            main_det.append(buff_matrix[0:])
        for i in range(len(main_det)):
            for j in range(w_matrix):
                main_det[i].append(0)

def get_time_interrupt():
    global time_interrupt
    global time_interrupt_state
    time_interrupt = []
    time_interrupt_state = []

    for i in range(len(mass_model)):
        if (i != 0):
            for j in range(len(mass_model[i])):
                if (mass_model[i][j] != 0):
                    for k in mass_model[i][j].time_interrupt():
                        time_interrupt.append(k)
    
    for i in range(len(time_interrupt)):
        for j in range(len(time_interrupt)):
            if ((time_interrupt[i] == time_interrupt[j]) and (time_interrupt[j] == -1) and (time_interrupt[i] == -1)):
                time_interrupt[j] = -1
    for i in range(len(time_interrupt)):
        if ((time_interrupt[len(time_interrupt) - 1 - i] == -1)):
            del time_interrupt[len(time_interrupt) - 1 - i]
  
    print(time_interrupt)
    for i in time_interrupt:
        time_interrupt_state.append(False)

        

def get_all_U_and_I_matrix():
    global mass_model
    global all_voltage_matrix
    global all_current_matrix
    global help_matrix
    global help_matrix_bus
    global voltage_bus
    help_matrix_bus = []
    all_voltage_matrix = []    
    all_current_matrix = []  
    help_matrix = []
    for i in range(len(mass_model)):
        use_k = []
        for j in range(len(mass_model[0])):
            if (mass_model[0][j] != 0):
                mass_iteraion = mass_model[0][j].list_connection[i][0:]
                for m in range(len(mass_iteraion)):
                    for n in use_k:
                        if (n == m):
                            mass_iteraion[m] = "none"
                for k in range(len(mass_iteraion)):
                    if (mass_iteraion[k] != "none"):
                        help_matrix.append([i, k])
                        use_k.append(k)     

    for i in range(len(mass_model[0])):
        help_voltage_matrix = []    
        help_current_matrix = [[], [], []] 
        wait_index = 0
        if (mass_model[0][i] != 0):
            for j in range(len(help_matrix)):
                if ((mass_model[0][i].list_connection[help_matrix[j][0]][help_matrix[j][1]] != "none") and (mass_model[0][i].list_connection[help_matrix[j][0]][help_matrix[j][1]].split(":")[1] == "ON_SWITCH")):
                    for o in range(len(mass_model[help_matrix[j][0]][help_matrix[j][1]].get_voltage_matrix(mass_model[0][i].list_connection[help_matrix[j][0]][help_matrix[j][1]].split(":")[0]))):
                        help_voltage_matrix.append([])
                        for p in range(len(mass_model[help_matrix[j][0]][help_matrix[j][1]].get_voltage_matrix(mass_model[0][i].list_connection[help_matrix[j][0]][help_matrix[j][1]].split(":")[0])[o])):
                            help_voltage_matrix[o + wait_index].append(mass_model[help_matrix[j][0]][help_matrix[j][1]].get_voltage_matrix(mass_model[0][i].list_connection[help_matrix[j][0]][help_matrix[j][1]].split(":")[0])[o][p])
                    wait_index += len(mass_model[help_matrix[j][0]][help_matrix[j][1]].get_voltage_matrix(mass_model[0][i].list_connection[help_matrix[j][0]][help_matrix[j][1]].split(":")[0]))
                else:
                    for o in range(len(mass_model[help_matrix[j][0]][help_matrix[j][1]].get_main_determinant(test_y))):
                        help_voltage_matrix.append([])
                        for p in range(3):
                            help_voltage_matrix[o + wait_index].append(0)
                    wait_index += len(mass_model[help_matrix[j][0]][help_matrix[j][1]].get_main_determinant(test_y))
                
                if ((mass_model[0][i].list_connection[help_matrix[j][0]][help_matrix[j][1]] != "none") and (mass_model[0][i].list_connection[help_matrix[j][0]][help_matrix[j][1]].split(":")[1] == "ON_SWITCH")):
                    for o in range(len(mass_model[help_matrix[j][0]][help_matrix[j][1]].get_current_matrix(mass_model[0][i].list_connection[help_matrix[j][0]][help_matrix[j][1]].split(":")[0]))):
                        for p in range(len(mass_model[help_matrix[j][0]][help_matrix[j][1]].get_current_matrix(mass_model[0][i].list_connection[help_matrix[j][0]][help_matrix[j][1]].split(":")[0])[o])):
                            help_current_matrix[o].append(mass_model[help_matrix[j][0]][help_matrix[j][1]].get_current_matrix(mass_model[0][i].list_connection[help_matrix[j][0]][help_matrix[j][1]].split(":")[0])[o][p])
                else:
                    for o in range(3):
                        for p in range(len(mass_model[help_matrix[j][0]][help_matrix[j][1]].get_main_determinant(test_y)[0])):
                            help_current_matrix[o].append(0)


            width_matrix_buff = 0
            for n in range(len(help_voltage_matrix)):
                if (len(help_voltage_matrix[n]) > width_matrix_buff):
                    width_matrix_buff = len(help_voltage_matrix[n])
            for n in range(len(help_voltage_matrix)):
                while (len(help_voltage_matrix[n]) != width_matrix_buff):
                    help_voltage_matrix[n].append(0)

            mass_repeat = []
            for ii in range(len(help_voltage_matrix[0])):
                repeat_num = 0
                for j in range(len(help_voltage_matrix)):
                    if ((help_voltage_matrix[j][ii] == 1) or (help_voltage_matrix[j][ii] == -1)):
                        repeat_num = 1
                if (repeat_num == 0):
                    mass_repeat.append(ii)

            for ii in mass_repeat:
                for j in range(len(help_voltage_matrix)):
                    del help_voltage_matrix[j][ii]
            
            help_matrix_bus.append([i, len(help_voltage_matrix[0])])

            if (len(help_voltage_matrix[0]) == 2):
                del help_current_matrix[-1]

            if (len(all_voltage_matrix) == 0):
                for ii in range(len(help_voltage_matrix)):
                    all_voltage_matrix.append([])

            for ii in range(len(help_voltage_matrix)):
                for j in range(len(help_voltage_matrix[ii])):
                    all_voltage_matrix[ii].append(help_voltage_matrix[ii][j])

            for ii in help_current_matrix:
                all_current_matrix.append(ii[0:])
    
    for i in range(len(help_matrix_bus)):
        voltage_bus.append([])
        for j in range(help_matrix_bus[i][1]):
            voltage_bus[i].append([])

   #print(help_matrix_bus)
    for i in range(len(mass_model[0])):
        if (mass_model[0][i] != 0):
            for j in range(len(mass_model[0][i].list_connection)):
                for k in range(len(mass_model[0][i].list_connection[j])):
                    if ((mass_model[0][i].list_connection[j][k] != "none") and (mass_model[0][i].list_connection[j][k].split(":")[1] == "OFF_SWITCH")):
                        help_voltage_matrix = []    
                        help_current_matrix = [[], [], []] 
                        wait_index = 0
                        for n in range(len(help_matrix)):
                            if ((help_matrix[n][0] == j) and (help_matrix[n][1] == k)):
                                for o in range(len(mass_model[help_matrix[n][0]][help_matrix[n][1]].get_voltage_matrix(mass_model[0][i].list_connection[help_matrix[n][0]][help_matrix[n][1]].split(":")[0]))):
                                    help_voltage_matrix.append([])
                                    for p in range(len(mass_model[help_matrix[n][0]][help_matrix[n][1]].get_voltage_matrix(mass_model[0][i].list_connection[help_matrix[n][0]][help_matrix[n][1]].split(":")[0])[o])):
                                        help_voltage_matrix[o + wait_index].append(mass_model[help_matrix[n][0]][help_matrix[n][1]].get_voltage_matrix(mass_model[0][i].list_connection[help_matrix[n][0]][help_matrix[n][1]].split(":")[0])[o][p])
                                wait_index += len(mass_model[help_matrix[n][0]][help_matrix[n][1]].get_voltage_matrix(mass_model[0][i].list_connection[help_matrix[n][0]][help_matrix[n][1]].split(":")[0]))
                                for o in range(len(mass_model[help_matrix[n][0]][help_matrix[n][1]].get_current_matrix(mass_model[0][i].list_connection[help_matrix[n][0]][help_matrix[n][1]].split(":")[0]))):
                                    for p in range(len(mass_model[help_matrix[n][0]][help_matrix[n][1]].get_current_matrix(mass_model[0][i].list_connection[help_matrix[n][0]][help_matrix[n][1]].split(":")[0])[o])):
                                        help_current_matrix[o].append(mass_model[help_matrix[n][0]][help_matrix[n][1]].get_current_matrix(mass_model[0][i].list_connection[help_matrix[n][0]][help_matrix[n][1]].split(":")[0])[o][p])
                            else:
                                for o in range(len(mass_model[help_matrix[n][0]][help_matrix[n][1]].get_main_determinant(test_y))):
                                    help_voltage_matrix.append([])
                                    for p in range(3):
                                        help_voltage_matrix[o + wait_index].append(0)
                                wait_index += len(mass_model[help_matrix[n][0]][help_matrix[n][1]].get_main_determinant(test_y))
                                for o in range(3):
                                    for p in range(len(mass_model[help_matrix[n][0]][help_matrix[n][1]].get_main_determinant(test_y)[0])):
                                        help_current_matrix[o].append(0)
                        
                        for qwerwqer in help_voltage_matrix:
                            print(qwerwqer)

                        width_matrix_buff = 0
                        for n in range(len(help_voltage_matrix)):
                            if (len(help_voltage_matrix[n]) > width_matrix_buff):
                                width_matrix_buff = len(help_voltage_matrix[n])
                        for n in range(len(help_voltage_matrix)):
                            while (len(help_voltage_matrix[n]) != width_matrix_buff):
                                help_voltage_matrix[n].append(0)

                        mass_repeat = []
                        for ii in range(len(help_voltage_matrix[0])):
                            repeat_num = 0
                            for jj in range(len(help_voltage_matrix)):
                                if ((help_voltage_matrix[jj][ii] == 1) or (help_voltage_matrix[jj][ii] == -1)):
                                    repeat_num = 1
                            if (repeat_num == 0):
                                mass_repeat.append(ii)
                        
                        buff_mass_repeat = []
                        buf_width = len(mass_repeat)
                        for i in range(len(mass_repeat)):
                            buff_mass_repeat.append(mass_repeat[buf_width-1 - i])

                        for ii in buff_mass_repeat:
                            for jj in range(len(help_voltage_matrix)):
                                del help_voltage_matrix[jj][ii]

                        if (len(help_voltage_matrix[0]) == 2):
                            del help_current_matrix[-1]
                        if (len(help_voltage_matrix[0]) == 1):
                            del help_current_matrix[-2]
                            del help_current_matrix[-1]

                        if (len(all_voltage_matrix) == 0):
                            for ii in range(len(help_voltage_matrix)):
                                all_voltage_matrix.append([])
    
                        for ii in range(len(help_voltage_matrix)):
                            for jj in range(len(help_voltage_matrix[ii])):
                                all_voltage_matrix[ii].append(help_voltage_matrix[ii][jj])

                        for ii in help_current_matrix:
                            all_current_matrix.append(ii[0:])


    for ii in range(len(all_current_matrix)):
        for j in range(len(all_voltage_matrix[0])):
            all_current_matrix[ii].append(0)
    

    #for ii in all_voltage_matrix:
        #print(ii)

    #for ii in all_current_matrix:
        #print(ii)
    
def get_y0():
    global y0
    y0 = []
    for i in range(len(mass_model)):
        use_k = []
        for j in range(len(mass_model[0])):
                if (mass_model[0][j] != 0):
                    mass_iteraion = mass_model[0][j].list_connection[i][0:]
                    for m in range(len(mass_iteraion)):
                        for n in use_k:
                            if (n == m):
                                mass_iteraion[m] = "none"
                    for k in range(len(mass_iteraion)):
                        if (mass_iteraion[k] != "none"):
                            for qwe in mass_model[i][k].get_first():
                                y0.append(qwe)
                            use_k.append(k)

    #print(y0)

def f(y, t):
    global all_voltage_matrix
    global all_current_matrix
    global help_matrix_bus
    global voltage_bus
    global t_d
    global main_det
    global time_interrupt
    global time_interrupt_state
    #t0 = time.time()
    for i in mass_model[7]:
        i.get_position_switches(t)
    for i in mass_model[6]:
        i.get_position_switches(t)
    for i in mass_model[5]:
        i.get_position_switches(t)
    for i in mass_model[1]:
        i.get_position_switches(t)
    
    for i in mass_model[0]:
        if (i != 0):
            i.control_connection(mass_model)
    
    interrupt_index = -1
    delta_time = 1000
    for i in range(len(time_interrupt)):
        if ((t - time_interrupt[i]) >= 0 and ((t - time_interrupt[i]) < delta_time)):
            delta_time = (t - time_interrupt[i])
            interrupt_index = i

    if ((interrupt_index != -1) and (time_interrupt_state[interrupt_index] == False)):
        time_interrupt_state[interrupt_index] = True
        get_all_U_and_I_matrix()
        for i in range(len(time_interrupt_state)):
            if (i != interrupt_index):
                time_interrupt_state[i] = False

    #t1 = time.time()
    main_det = []
    wait_index = 0
    current_index = [0, 0]
    own_matrix = []
    ouput_matrix = []
    for i in range(len(mass_model)):
        if (i == 1):
            width_matrix = 6
            height_matrix = 6
            width_input = 6
        if (i == 2):
            width_matrix = 3
            height_matrix = 3
            width_input = 5
        if (i == 3):
            width_matrix = 3
            height_matrix = 3
            width_input = 3
        if (i == 4):
            width_matrix = 3
            height_matrix = 3
            width_input = 3
        if (i == 5):
            width_matrix = 6
            height_matrix = 6
            width_input = 8
        if (i == 6):
            width_matrix = 3
            height_matrix = 3
            width_input = 3
        if (i == 7):
            width_matrix = 1
            height_matrix = 1
            width_input = 1
        use_k = []
        for j in range(len(mass_model[0])):
            if (mass_model[0][j] != 0):
                mass_iteraion = mass_model[0][j].list_connection[i][0:]
                for m in range(len(mass_iteraion)):
                    for n in use_k:
                        if (n == m):
                            mass_iteraion[m] = "none"
                for k in range(len(mass_iteraion)):
                    if (mass_iteraion[k] != "none"):
                        for qwe in mass_model[i][k].get_own_matrix(y[wait_index:(wait_index+width_input)], t)[0:]:
                            own_matrix.append(qwe)
                        add_zero_matrix(width_matrix, height_matrix)
                        buff_matrix = mass_model[i][k].get_main_determinant(y[wait_index:(wait_index+width_input)])
                        for m in range(height_matrix):
                            for n in range(width_matrix):
                                main_det[m + current_index[0]][n + current_index[1]] = buff_matrix[m][n]
                        current_index[0] += height_matrix
                        current_index[1] += width_matrix
                        wait_index += width_input  
                        use_k.append(k)
    
    range_main_det_without = len(main_det[0])

    for i in range(len(all_voltage_matrix)):
        for j in range(len(all_voltage_matrix[i])):
            main_det[i].append(all_voltage_matrix[i][j])

    for i in range(len(all_current_matrix)):
        main_det.append(all_current_matrix[i][0:])

    for i in range(len(all_current_matrix)):
        own_matrix.append(0)
   
    solve_matrix = np.linalg.solve(main_det, own_matrix)

    #dm = np.linalg.det(main_det)
    if (len(t_d) != 0):
        if (t_d[-1] > t):
            while (t_d[-1] > t):
                wait_index = 0
                for i in range(len(help_matrix_bus)):
                    for j in range(help_matrix_bus[i][1]):
                        del voltage_bus[i][j][-1]
                        wait_index += 1
                del t_d[-1]

    wait_index = 0
    for i in range(len(help_matrix_bus)):
        for j in range(help_matrix_bus[i][1]):
            voltage_bus[i][j].append(solve_matrix[range_main_det_without + wait_index])
            wait_index += 1
    t_d.append(t)

    wait_index = 0
    qwe_i = 0
    for i in range(len(mass_model)):
        use_k = []
        for j in range(len(mass_model[0])):
            if (mass_model[0][j] != 0):
                mass_iteraion = mass_model[0][j].list_connection[i][0:]
                for m in range(len(mass_iteraion)):
                    for n in use_k:
                        if (n == m):
                            mass_iteraion[m] = "none"
                for k in range(len(mass_iteraion)):
                    if (mass_iteraion[k] != "none"):
                        if (i == 1):
                            width_input = 6
                            for m in range(len(mass_model[i][k].get_main_determinant(y[wait_index:(wait_index+width_input)])[0])):
                                #ouput_matrix.append(np.linalg.det(swap_own(main_det, own_matrix, qwe_i))/dm)
                                ouput_matrix.append(solve_matrix[qwe_i])
                                qwe_i += 1
                            wait_index += width_input
                        if (i == 2):
                            width_input = 5
                            for m in range(3):
                                #ouput_matrix.append(np.linalg.det(swap_own(main_det, own_matrix, qwe_i))/dm)   
                                ouput_matrix.append(solve_matrix[qwe_i])       
                                qwe_i += 1              
                            ouput_matrix.append(mass_model[i][k].get_derw(y[wait_index:(wait_index+width_input)], t))
                            ouput_matrix.append(mass_model[i][k].get_w(y[wait_index:(wait_index+width_input)]))                       
                            wait_index += width_input                        
                        if (i == 3):
                            width_input = 3
                            for m in range(len(mass_model[i][k].get_main_determinant(y[wait_index:(wait_index+width_input)])[0])):
                                #ouput_matrix.append(np.linalg.det(swap_own(main_det, own_matrix, qwe_i))/dm)
                                ouput_matrix.append(solve_matrix[qwe_i])
                                qwe_i += 1
                            wait_index += width_input
                        if (i == 4):
                            width_input = 3
                            for m in range(len(mass_model[i][k].get_main_determinant(y[wait_index:(wait_index+width_input)])[0])):
                                #ouput_matrix.append(np.linalg.det(swap_own(main_det, own_matrix, qwe_i))/dm)
                                ouput_matrix.append(solve_matrix[qwe_i])
                                qwe_i += 1
                            wait_index += width_input
                        if (i == 5):
                            width_input = 8
                            for m in range(6):
                                #ouput_matrix.append(np.linalg.det(swap_own(main_det, own_matrix, qwe_i))/dm)   
                                ouput_matrix.append(solve_matrix[qwe_i])       
                                qwe_i += 1              
                            ouput_matrix.append(mass_model[i][k].get_derw(y[wait_index:(wait_index+width_input)], t))
                            ouput_matrix.append(mass_model[i][k].get_w(y[wait_index:(wait_index+width_input)]))                       
                            wait_index += width_input  
                        if (i == 6):
                            width_input = 3
                            for m in range(len(mass_model[i][k].get_main_determinant(y[wait_index:(wait_index+width_input)])[0])):
                                #ouput_matrix.append(np.linalg.det(swap_own(main_det, own_matrix, qwe_i))/dm)
                                ouput_matrix.append(solve_matrix[qwe_i])
                                qwe_i += 1
                            wait_index += width_input
                        if (i == 7):
                            width_input = 1
                            for m in range(len(mass_model[i][k].get_main_determinant(y[wait_index:(wait_index+width_input)])[0])):
                                #ouput_matrix.append(np.linalg.det(swap_own(main_det, own_matrix, qwe_i))/dm)
                                ouput_matrix.append(solve_matrix[qwe_i])
                                qwe_i += 1
                            wait_index += width_input

                        use_k.append(k)
    
    print(str(round(t/t_max*100, 3)), end = "\r")
    

    return ouput_matrix
    #for i in main_det:
        #print(i)
def close_window(event): 
    root.destroy()

canv.bind('<Button-1>', click_1)
canv.bind('<Button-3>', click_2)
canv.bind('<Motion>', mouse_motion)
root.bind('e', expand_bus)
root.bind('r', set_potation_position)
root.bind('<Delete>', delete_model)
root.bind('<Escape>', close_window)
root.bind('<Return>', enter_inf)
root.bind('s', start)
root.bind('m', main_menu)
root.bind('p', change_parameter)
root.bind('1', add_Electrical_Bus)
root.bind('2', add_Transformator_Z_T_11)
root.bind('3', add_SM)
root.bind('4', add_AM)
root.bind('5', add_Static_load)
root.bind('6', add_Electrical_system)
root.bind('7', add_KZ_Bus)
root.bind('8', add_KZ_single_phase)
canv.pack() 
root.mainloop()