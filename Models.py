import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

k_size = 6
state_menu = 0
def create_image_for_model(pass_obj):
    buff_image = ImageTk.PhotoImage(Image.open(pass_obj))
    width_image = buff_image.width()/k_size
    image = ImageTk.PhotoImage(Image.open(pass_obj).resize((int(width_image), int((width_image)*buff_image.height()/buff_image.width())), Image.ANTIALIAS))
    #imagesprite2 = canv.create_image(WIDTH/2,HEIGHT/2,image=image2)
    return image

n_fig = 1
###
def ksi_dif(H):
    return 70

def B_delta(Ica, Icb, Icc, Ira, Irb, Irc, x, phi, mu0, delta, wc, wr, tau, p):
    return (2*mu0/(math.pi*delta)*(wc*Ica*math.cos(math.pi/tau*x)+wc*Icb*math.cos(math.pi/tau*x-2*math.pi/3)+wc*Icc*math.cos(math.pi/tau*x+2*math.pi/3)+wr*Ira*math.cos(math.pi/tau*x-phi*p)+wr*Irb*math.cos(math.pi/tau*x-phi*p-2*math.pi/3)+wr*Irc*math.cos(math.pi/tau*x-phi*p+2*math.pi/3)))

def moment_pd(t, t0, t2, M_max):
    t1 = t0 + t2
    if ((t >= t0) and (t <= t1)):
        return ((M_max)/(t1-t0)*t - (M_max)/(t1-t0)*t0)
    if (t < t0):
        return 0
    if (t > t1):
        return M_max

def get_wc(Xc, delta, S):
    mu0 = 4 * math.pi * (10 ** (-7))
    return math.sqrt(Xc*math.pi*delta*math.pi/(100*math.pi*2*mu0*2*S*1.5))

def get_wr(wc, delta, S, Pn, cosfi, Un, Ifn, Xc, Rc):
    mu0 = 4 * math.pi * (10 ** (-7))
    return ((math.sqrt((Pn/math.sqrt(3)/cosfi/Un*1000*math.sqrt(2)*Xc)**2 + (Un*1000/math.sqrt(3)*math.sqrt(2))**2 + 2*Pn/math.sqrt(3)/cosfi/Un*1000*math.sqrt(2)*Xc*Un*1000/math.sqrt(3)*math.sqrt(2)*math.sin(math.fabs(math.acos(cosfi)))))*(math.pi*delta*math.pi)/(100*math.pi*wc*Ifn*mu0*4*S))

def get_R_Z_T_11(Pkz, UnZ, Sn):
    return (Pkz/1000*(UnZ*UnZ)/(Sn*Sn))
def get_Z_Z_T_11(Uk, UnZ, Sn):
    return (Uk/100*(UnZ**2)/Sn)


###
class Electrical_Bus:
    state_click = 0
    k_expand = 6
    list_connection = []
    connectivity_to_bus = 0
    number_of_connection = 0
    position = 0

    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.image_model_data = create_image_for_model("Image/Electrical Bus/" + str(self.position) + ".png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')
        self.model_text = self.canv.create_text(self.x, self.y, text = str(self.number_of_connection), fill = "black", font = ("GOST Type A", "14"), anchor="sw")   
  

    def __del__(self):
        self.canv.delete(self.model_text)
    
    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def control_connection(self, models):
        if (self.state_click  == 0):
            self.list_connection = []
            self.number_of_connection = 0
            for i in range(len(models)):
                self.list_connection.append([])
                for j in models[i]:
                    if (j != 0):
                        if (j.connectivity_to_bus == 1):
                            self.list_connection[i].append(j.set_connection(self.x, self.y, self.image_width, self.image_height))
                        else:
                            self.list_connection[i].append("none")
                    else:
                        self.list_connection[i].append("none")

            for i in self.list_connection:
                for j in i:
                    if (j != "none"):
                        self.number_of_connection += 1

            self.canv.delete(self.model_text)
            self.model_text = self.canv.create_text(self.x, self.y, text = str(self.number_of_connection), fill = "black", font = ("GOST Type A", "14"), anchor="sw")
           #print(self.list_connection)
    def set_state_click(self, m_x, m_y):
        if ((m_x > self.x) and (m_x < self.x + self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0

    def rotation(self, m_x, m_y):
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 1):
                self.position = 0
            self.image_model_data = create_image_for_model("Image/Electrical Bus/" + str(self.position) + ".png")
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = 5
            self.delta_y = 5 
            self.image_model = self.canv.create_image(m_x - self.delta_x, m_y - self.delta_y,image = self.image_model_data, anchor = 'nw')



    def view_result(self, m_x, m_y):
        if ((m_x > self.x) and (m_x < self.x + self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            return True

    def expand_image_model(self, m_x, m_y):
        if (self.state_click == 1):
            if (self.position == 0):
                buff_image = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/0.png"))
                width_image = buff_image.width()/k_size
                height_image = self.image_model_data.height() + self.k_expand
                self.image_model_data = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/0.png").resize((int(width_image), int(height_image)), Image.ANTIALIAS))
                self.x = m_x - self.delta_x
                self.y = m_y - self.delta_y
                self.image_width = self.image_model_data.width()
                self.image_height = self.image_model_data.height()
                self.canv.delete(self.image_model)
                self.image_model = self.canv.create_image(self.x, self.y ,image = self.image_model_data, anchor = 'nw')
            if (self.position == 1):
                buff_image = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/1.png"))
                height_image = (buff_image.width()/k_size)*buff_image.height()/buff_image.width()
                width_image = self.image_model_data.width() + self.k_expand
                self.image_model_data = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/1.png").resize((int(width_image), int(height_image)), Image.ANTIALIAS))
                self.x = m_x - self.delta_x
                self.y = m_y - self.delta_y
                self.image_width = self.image_model_data.width()
                self.image_height = self.image_model_data.height()
                self.canv.delete(self.image_model)
                self.image_model = self.canv.create_image(self.x, self.y ,image = self.image_model_data, anchor = 'nw')
        
    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.canv.coords(self.model_text, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x           
            self.y = m_y - self.delta_y

class Transformator_Z_T_11:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    position = 0
    switch_time_T = [[],[]]
    position_switch_T = True
    help_var_switch_T = False
    toff_T = 0
    switch_time_Z = [[],[]]
    position_switch_Z = True
    help_var_switch_Z = False
    toff_Z = 0
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    UnZ = 121
    UnT = 6.3
    L = 1
    ra = 0.4
    R_t = 0.1
    lm = 2*(L + ra)
    S = math.pi*R_t**2
    R1 = 0.0009612
    R2 = 0.355
    Ls1 = 0.000087
    Ls2 = 0.032
    w1 = 100*int(121/(math.sqrt(3)*6.3))
    w2 = 100
    Roff_T = 0
    Roff_Z = 0

    var_text = ["Номинальное напряжение обмотки треугольника, кВ:",
    "Номинальное напряжение обмотки звезды, кВ:",
    "Активное сопротивление обмотки треугольника, Ом:",
    "Активное сопротивление обмотки звезды, Ом:",
    "Индуктивность поля рассеяния обмотки треугольника, Гн:",
    "Индуктивность поля рассеяния обмотки звезды, Гн:",
    "Высота катушек, м:",
    "Расстояние между осями катушек, м:",
    "Моменты времени, при которых контакты выключателя на стороне Y замыкаются, с:",
    "Моменты времени, при которых контакты выключателя на стороне Y размыкаются, с:", 
    "Моменты времени, при которых контакты выключателя на стороне D замыкаются, с:",
    "Моменты времени, при которых контакты выключателя на стороне D размыкаются, с:" 
    ]
    
    example_Transformator_Z_T_11 = [[80, 121, 6.3, 310, 85, 11, 0.6],
    [80, 121, 15, 310, 85, 11, 0.6],
    [125, 121, 10.5, 400, 120, 10.5, 0.55],
    [200, 121, 15.75, 550, 170, 10.5, 0.5],
    [250, 121, 15.75, 640, 200, 10.5, 0.5],
    [400, 121, 20, 900, 320, 10.5, 0.45],
    [2.5, 110, 6.6, 22, 5.5, 10.5, 1.55],
    [2.5, 110, 11, 22, 5.5, 10.5, 1.55],
    [6.3, 115, 6.6, 44, 10, 10.5, 1],
    [6.3, 115, 11, 44, 10, 10.5, 1],
    [10, 115, 6.6, 58, 14, 10.5, 0.9],
    [10, 115, 11, 58, 14, 10.5, 0.9],
    [16, 115, 6.6, 85, 18, 10.5, 0.7],
    [16, 115, 11, 85, 18, 10.5, 0.7],
    [16, 115, 22, 85, 18, 10.5, 0.7],
    [16, 115, 34.5, 85, 18, 10.5, 0.7],
    [25, 115, 38.5, 120, 25, 10.5, 0.65],
    [40, 115, 38.5, 170, 34, 10.5, 0.55],
    [63, 115, 38.5, 245, 50, 10.5, 0.5],
    [80, 115, 38.5, 310, 58, 10.5, 0.45],
    [80, 242, 6.3, 315, 79, 11, 0.45],
    [80, 242, 10.5, 315, 79, 11, 0.45],
    [125, 242, 10.5, 380, 120, 11, 0.55],
    [200, 242, 15.75, 660, 130, 11, 0.4],
    [250, 242, 15.75, 600, 207, 11, 0.5],
    [400, 242, 15.75, 880, 330, 11, 0.4],
    [400, 242, 20, 880, 330, 11, 0.4],
    [630, 242, 15.75, 1200, 400, 12.5, 0.35],
    [630, 242, 20, 1200, 400, 12.5, 0.35],
    [630, 242, 24, 1200, 400, 12.5, 0.35],
    [1000, 242, 24, 2200, 480, 11.5, 0.4],
    [125, 347, 10.5, 380, 125, 11, 0.55],
    [200, 347, 15.75, 520, 180, 11, 0.5],
    [250, 347, 15.75, 605, 214, 11, 0.5],
    [400, 347, 20, 790, 300, 11.5, 0.45],
    [630, 347, 15.75, 1300, 345, 11.5, 0.35],
    [630, 347, 20, 1300, 345, 11.5, 0.35],
    [630, 347, 24, 1300, 345, 11.5, 0.35],
    [1000, 347, 24, 2200, 480, 11.5, 0.4],
    [1250, 347, 24, 2200, 715, 14.5, 0.55],
    [250, 525, 15.75, 590, 205, 13, 0.45],
    [250, 525, 20, 590, 205, 13, 0.45],
    [400, 525, 15.75, 790, 315, 13, 0.45],
    [400, 525, 20, 790, 315, 13, 0.45],
    [630, 525, 15.75, 1210, 420, 14, 0.4],
    [630, 525, 20, 1210, 420, 14, 0.4],
    [630, 525, 24, 1210, 420, 14, 0.4],
    [1000, 525, 24, 1800, 570, 14.5, 0.45],
    ]

    mass_entry = []
    mass_var = []

    def __init__(self, init_x, init_y, canv, root):
        print(self.example_Transformator_Z_T_11)
        self.canv = canv
        self.root = root
        self.list_example = ttk.Combobox(self.root, values = [
        "Пользовательский",
        "ТДЦ-80000/121/6,3",
        "ТДЦ-80000/121/15",
        "ТДЦ-1250000/121/10,5",
        "ТДЦ-200000/121/15,75",
        "ТДЦ-250000/121/15,75",
        "ТДЦ-400000/121/20",
        "ТМН-2500/110/6,6",
        "ТМН-2500/110/11",
        "ТМН-6300/115/6,6",
        "ТМН-6300/115/11",
        "ТДН-10000/115/6,6",
        "ТДН-10000/115/11",
        "ТДН-16000/115/6,6",
        "ТДН-16000/115/11",
        "ТДН-16000/115/22",
        "ТДН-16000/115/34,5",
        "ТДН-25000/115/38,5",
        "ТДН-40000/115/38,5",
        "ТДН-63000/115/38,5",
        "ТДН-80000/115/38,5",
        "ТД-80000/242/6,3",
        "ТД-80000/242/10,5",
        "ТДЦ-125000/242/10,5",
        "ТДЦ-200000/242/15,75",
        "ТДЦ-250000/242/15,75",
        "ТДЦ-400000/242/15,75",
        "ТДЦ-400000/242/20",
        "ТНЦ-630000/242/15,75",
        "ТНЦ-630000/242/20",
        "ТНЦ-630000/242/24",
        "ТНЦ-1000000/242/24",
        "ТДЦ-125000/347/10,5",
        "ТДЦ-200000/347/15,75",
        "ТДЦ-250000/347/10,5",
        "ТДЦ-400000/347/20",
        "ТНЦ-630000/347/15,75",
        "ТНЦ-630000/347/20",
        "ТНЦ-630000/347/24",
        "ТНЦ-1000000/347/24",
        "ТНЦ-1250000/347/24",
        "ТДЦ-250000/525/15,75",
        "ТДЦ-250000/525/20",
        "ТДЦ-400000/525/15,75",
        "ТДЦ-400000/525/20",
        "ТЦ-630000/525/15,75",
        "ТЦ-630000/525/20",
        "ТЦ-630000/525/24",
        "ТНЦ-1000000/525/24",
        ])
        self.list_example.current(0)
        self.image_model_data = create_image_for_model("Image/Transformator/" + str(self.position) + ".png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')

    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def get_first(self):
        return ([0, 0, 0, 0, 0, 0])

    def get_main_determinant(self, input_variable):
        main_determinant = [[self.Ls1 - self.w1*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0, 0, 0, self.w1*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0],
                            [0, self.Ls1 - self.w1*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5]), 0, 0, 0, self.w1*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5])],
                            [0, 0, self.Ls1 - self.w1*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), self.w1*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), 0, 0],
                            [self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0, -self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), -self.Ls2 + self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), self.Ls2 - self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0],
                            [-self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5]), 0, 0, -self.Ls2 + self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), self.Ls2 - self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5])],
                            [0, -self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5]), 0, 0, 0, -self.Ls2 + self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5])]
                            ]

        return main_determinant
    
    def get_own_matrix(self, input_variable, t):
        if (self.position_switch_T == False):
            self.Roff_T = 10000000/0.1*(t - self.toff_T)
        if (self.position_switch_Z == False):
            self.Roff_Z = 1000000/0.1*(t - self.toff_Z)
        own_matrix = [-input_variable[0]*self.R1 + (input_variable[2] - input_variable[0])*self.Roff_T - (input_variable[0] - input_variable[1])*self.Roff_T,
                    -input_variable[1]*self.R1 + (input_variable[0] - input_variable[1])*self.Roff_T - (input_variable[1] - input_variable[2])*self.Roff_T,
                    -input_variable[2]*self.R1 + (input_variable[1] - input_variable[2])*self.Roff_T - (input_variable[2] - input_variable[0])*self.Roff_T,
                    input_variable[3]*self.R2 - input_variable[4]*self.R2 + (input_variable[3] - input_variable[4])*self.Roff_Z,
                    input_variable[4]*self.R2 - input_variable[5]*self.R2 + (input_variable[4] - input_variable[5])*self.Roff_Z,
                    input_variable[5]*self.R2 + input_variable[5]*self.Roff_Z
                    ] 

        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "T"):
            voltage_matrix = [[1, 0],
                        [0, 1],
                        [-1, -1], 
                        [0, 0], 
                        [0, 0],
                        [0, 0]
                        ] 
            return voltage_matrix

        if (parameter == "Z"):
            voltage_matrix = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0],
                        [-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1]
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "T"):
            current_matrix = [[1, 0, -1, 0, 0, 0],
                        [-1, 1, 0, 0, 0, 0],
                        [0, -1, 1, 0, 0, 0]
                        ] 
            return current_matrix

        if (parameter == "Z"):
            current_matrix = [[0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 1]
                        ] 
            return current_matrix

    def get_position_switches(self, t):
        delta_time_swicth = 1000 #dlya nachalnogo sravneniya
        index_switcth = 0
        for i in range(len(self.switch_time_T)):
            for j in self.switch_time_T[i]:
                if (((t - j) > 0) and ((t - j) < delta_time_swicth)):           
                    delta_time_swicth = (t - j)
                    index_switcth = i
        if (index_switcth == 0):
            self.position_switch_T = True
            self.help_var_switch_T = False
            self.Roff_T = 0
        elif (index_switcth == 1):
            self.position_switch_T = False
            if (self.help_var_switch_T == False):
                self.toff_T = t
                self.help_var_switch_T = True


        delta_time_swicth = 1000 #dlya nachalnogo sravneniya
        index_switcth = 0
        for i in range(len(self.switch_time_Z)):
            for j in self.switch_time_Z[i]:
                if (((t - j) > 0) and ((t - j) < delta_time_swicth)):           
                    delta_time_swicth = (t - j)
                    index_switcth = i
        if (index_switcth == 0):
            self.position_switch_Z = True
            self.help_var_switch_Z = False
            self.Roff_Z = 0
        elif (index_switcth == 1):
            self.position_switch_Z = False
            if (self.help_var_switch_Z == False):
                self.toff_Z = t
                self.help_var_switch_Z = True

    def time_interrupt(self):
        list_time_interrupt = []
        for i in range(len(self.switch_time_T)):
            for j in self.switch_time_T[i]:
                if (i == 0):
                    list_time_interrupt.append(j)
                if (i == 1):
                    list_time_interrupt.append(j + 0.1)
        for i in range(len(self.switch_time_Z)):
            for j in self.switch_time_Z[i]:
                if (i == 0):
                    list_time_interrupt.append(j)
                if (i == 1):
                    list_time_interrupt.append(j + 0.1)
        return list_time_interrupt


    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if (self.position == 0):
            if ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_Z == False):
                    return ("Z:OFF_SWITCH")
                return ("Z:ON_SWITCH")
            elif ((self.x > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_T == False):
                    return ("T:OFF_SWITCH")
                return ("T:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 1):
            if ((self.x + self.image_width/2 > bus_x) and (self.y + self.image_height > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
                if (self.position_switch_Z == False):
                    return ("Z:OFF_SWITCH")
                return ("Z:ON_SWITCH")
            elif ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
                if (self.position_switch_T == False):
                    return ("T:OFF_SWITCH")
                return ("T:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 2):
            if ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_T == False):
                    return ("T:OFF_SWITCH")
                return ("T:ON_SWITCH")
            elif ((self.x > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_Z == False):
                    return ("Z:OFF_SWITCH")
                return ("Z:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 3):
            if ((self.x + self.image_width/2 > bus_x) and (self.y + self.image_height > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
                if (self.position_switch_T == False):
                    return ("T:OFF_SWITCH")
                return ("T:ON_SWITCH")
            elif ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
                if (self.position_switch_Z == False):
                    return ("Z:OFF_SWITCH")
                return ("Z:ON_SWITCH")
            else:
                return ("none")

    def set_state_click(self, m_x, m_y):
        if ((m_x >= self.x + self.k_click*self.image_width) and (m_x <= self.x + self.image_width - self.k_click*self.image_width) and (m_y >= self.y + self.k_click*self.image_height) and (m_y <= self.y + self.image_height - self.k_click*self.image_height)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0

    def rotation(self, m_x, m_y):
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 3):
                self.position = 0
            self.image_model_data = create_image_for_model("Image/Transformator/" + str(self.position) + ".png")
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = self.k_click*self.image_width
            self.delta_y = self.k_click*self.image_height
            self.image_model = self.canv.create_image(m_x - self.k_click*self.image_width, m_y - self.k_click*self.image_height,image = self.image_model_data, anchor = 'nw')


    def view_result(self, m_x, m_y):
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            return True

    def change_parameter_in_model(self, m_x, m_y, WIDTH):
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            self.state_change_parameter = 1
            self.mass_entry = []
            self.mass_var = []
            self.switch_time_Z_on_string = ""
            for i in self.switch_time_Z[0]:
                self.switch_time_Z_on_string = self.switch_time_Z_on_string + str(i) + ", "
            self.switch_time_Z_off_string = ""
            for i in self.switch_time_Z[1]:
                self.switch_time_Z_off_string = self.switch_time_Z_off_string + str(i) + ", "
            self.switch_time_T_on_string = ""
            for i in self.switch_time_T[0]:
                self.switch_time_T_on_string = self.switch_time_T_on_string + str(i) + ", "
            self.switch_time_T_off_string = ""
            for i in self.switch_time_T[1]:
                self.switch_time_T_off_string = self.switch_time_T_off_string + str(i) + ", "
            current_var = [self.w1,self.w2, self.R1,self.R2,self.Ls1,self.Ls2,self.L,self.ra, self.switch_time_Z_on_string, self.switch_time_Z_off_string, self.switch_time_T_on_string, self.switch_time_T_off_string]
            for i in range(len(self.var_text)):
                self.mass_var.append(StringVar(value=str(current_var[i])))
                self.mass_entry.append(Entry(textvariable = self.mass_var[i], width = 12, relief = SOLID, borderwidth = 1, justify = CENTER))
            self.mass_canv_text = []
            for i in range(len(self.var_text)):
                self.mass_canv_text.append(self.canv.create_text(WIDTH/2, i*25, text = self.var_text[i], fill = "black", font = ("GOST Type A", "16"), anchor="ne"))
                self.mass_entry[i].place(x = WIDTH/2+ 20, y = i*25)

    def set_parameter_in_model(self):
        for i in range(len(self.mass_var)):
            if (i == 0):
                self.w1 = float(self.mass_var[i].get())
            elif (i == 1):
                self.w2 = float(self.mass_var[i].get())
            elif (i == 2):
                self.R1 = float(self.mass_var[i].get())
            elif (i == 3):
                self.R2 = float(self.mass_var[i].get())
            elif (i == 4):
                self.Ls1 = float(self.mass_var[i].get())
            elif (i == 5):
                self.Ls2 = float(self.mass_var[i].get())
            elif (i == 6):
                self.L = float(self.mass_var[i].get())
            elif (i == 7):
                self.ra = float(self.mass_var[i].get())
            elif (i == 8):
                self.switch_time_Z = []
                self.switch_time_Z.append([])
                self.switch_time_Z.append([])
                for j in self.mass_var[i].get().split(", "):
                    if (j != ""):
                        self.switch_time_Z[0].append(float(j))  
            elif (i == 9):
                for j in self.mass_var[i].get().split(", "):
                    if (j != ""):
                        self.switch_time_Z[1].append(float(j)) 
            elif (i == 10):
                self.switch_time_T = []
                self.switch_time_T.append([])
                self.switch_time_T.append([])
                for j in self.mass_var[i].get().split(", "):
                    if (j != ""):
                        self.switch_time_T[0].append(float(j))  
            elif (i == 11):
                for j in self.mass_var[i].get().split(", "):
                    if (j != ""):
                        self.switch_time_T[1].append(float(j)) 

    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y

class SM:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    position = 0
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    Un = 6.38
    Ur = 350
    tau = 1.2
    l = 1
    wc = 14
    wr = 72
    mu0 = 4 * math.pi * (10 ** (-7))
    delta = 0.015
    Rs = 0.005
    Rr = 0.5
    Ls = 0.004
    Lrs = 0.005
    J = 3000
    D = 2*tau/math.pi
    M_max = -50000
    t0 = 1
    t2 = 1
    Ir_start = Ur/Rr
    w_start = 2*50*math.pi
    phi_start = 0
    Urxx = Un/math.sqrt(3)*1000*Rr*math.pi*delta*math.pi/(100*math.pi*math.sqrt(2)*wc*wr*mu0*2*tau*l)
    Ir_start = Urxx/Rr
    var_text = ["Номинальное напряжение, кВ:",
    "Напряжение возбуждения, В:",
    "Момент инерции ротора, кг*м2:",
    "Активное сопротивление обмотки статора, Ом:",
    "Активное сопротивление обмотки возбуждения, Ом:",
    "Индуктивность поля рассеяния обмотки статора, Гн:",
    "Индуктивность поля рассеяния обмотки ротора, Гн:",
    "Длина машины, м:",
    "Полюсное деление машины, м:",
    "Длина воздушного зазора, м:",
    "Число витков обмотки , шт:",
    "Число витков обмотки ротора, шт:",
    "Момент ПД, Н*м:",
    "Время, при котором начинается подача момента, с:",
    "Время подачи момента ПД, с:",
    "Значение тока возбуждения в начальный момент времени, А:",
    "Значение циклической частоты вращения ротора в начальный момент времени, Гц:",
    "Значение начального угла поворота ротора в начальный момент времени, градус:"  
    ]

    example_SM = [[10.5, 139.61, 2615, 0.002, 0.0953, 0.0001, 0.0002, 3.1, 1.075*math.pi/2, 0.0425, get_wc(2.118, 0.0425, 3.1*1.075*math.pi/2), get_wr(get_wc(2.118, 0.0425, 3.1*1.075*math.pi/2), 0.0425, 3.1*1.075*math.pi/2, 63, 0.8, 10.5, 1465, 2.118, 0)],
    [10.5, 219.24, 3750, 0.00104, 0.126, 0.0001, 0.0002, 3.1, 1.128*math.pi/2, 0.064, get_wc(1.636, 0.064, 3.1*1.128*math.pi/2), get_wr(get_wc(1.636, 0.064, 3.1*1.128*math.pi/2), 0.064, 3.1*1.128*math.pi/2, 110, 0.8, 10.5, 1740, 1.636, 0)],
    [10.5, 205.8, 3750, 0.00104, 0.12, 0.0001, 0.0002, 3.1, 1.128*math.pi/2, 0.064, get_wc(1.402, 0.064, 3.1*1.128*math.pi/2), get_wr(get_wc(1.402, 0.064, 3.1*1.128*math.pi/2), 0.064, 3.1*1.128*math.pi/2, 120, 0.8, 10.5, 1715, 1.402, 0)],
    [15.75, 274.72, 4375, 0.0024, 0.136, 0.0001, 0.0002, 3.85, 1.17*math.pi/2, 0.085, get_wc(2.257, 0.085, 3.85*1.17*math.pi/2), get_wr(get_wc(2.257, 0.085, 3.85*1.17*math.pi/2), 0.085,  3.85*1.17*math.pi/2, 160, 0.85, 15.75, 2020, 2.257, 0)],
    [15.75, 327.12, 6070, 0.00115, 0.174, 0.0001, 0.0002, 4.3, 1.235*math.pi/2, 0.080, get_wc(1.99, 0.080, 4.3*1.235*math.pi/2), get_wr(get_wc(1.99, 0.080, 4.3*1.235*math.pi/2), 0.080, 4.3*1.235*math.pi/2, 200, 0.85, 15.75, 1880, 1.99, 0)],
    [20, 332.05, 7950, 0.001335, 0.1145, 0.0001, 0.0002, 6, 1.265*math.pi/2, 0.095, get_wc(1.804, 0.095, 6*1.265*math.pi/2), get_wr( get_wc(1.804, 0.095, 6*1.265*math.pi/2), 0.095, 6*1.265*math.pi/2, 320, 0.85, 20, 2900, 1.804, 0)],
    [20, 299.154, 10280, 0.0011, 0.0683, 0.0001, 0.0002, 6.3, 1.315*math.pi/2, 0.095, get_wc(1.467, 0.095, 6.3*1.315*math.pi/2), get_wr(get_wc(1.467, 0.095, 6.3*1.315*math.pi/2), 0.095, 6.3*1.315*math.pi/2, 500, 0.85, 20, 4380, 1.467, 0)],
    [18, 439.9616, 8670, 0.00084, 0.2644, 0.0001, 0.0002, 5.3, 1.29*math.pi/2, 0.0824, get_wc(1.62, 0.0824, 5.3*1.29*math.pi/2), get_wr(get_wc(1.62, 0.0824, 5.3*1.29*math.pi/2), 0.0824, 5.3*1.29*math.pi/2, 400, 0.95, 18, 1667, 1.62, 0)]
    ]

    mass_entry = []
    mass_var = []

    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.list_example = ttk.Combobox(self.root, values = [
        "Пользовательский",
        "ТВФ-63-2УЗ",
        "ТВФ-110-2ЕУЗ",
        "ТВФ-120-2УЗ",
        "ТВВ-160-2ЕУЗ",
        "ТГВ-200-2УЗ",
        "ТВВ-320-2ЕУЗ",
        "ТГВ-500-4УЗ",
        "390H"
        ])
        self.list_example.current(0)
        self.image_model_data = create_image_for_model("Image/SM/" + str(self.position) + ".png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')
    
    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def get_first(self):
        return ([0, 0, self.Ir_start, self.w_start, self.phi_start])

    def get_main_determinant(self, input_variable):
        main_determinant = [[-(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(1 + (-1)*math.sin(math.pi/2 - 2*math.pi/3) - (-1)*math.sin(math.pi/6) - (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3)) - self.Ls, -(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 + 2*math.pi/3) + (-1)*math.sin(math.pi/2 - 2*math.pi/3) - (-1)*math.sin(math.pi/6 - 2*math.pi/3) - (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3)) + self.Ls, -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2+input_variable[4]) - (-1)*math.sin(math.pi/6-input_variable[4]))],
    	                   [-(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6) + (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3) - math.sin(-math.pi/6) - (-1)*math.sin(-math.pi/6 + 2*math.pi/3))  - self.Ls, -(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6 - 2*math.pi/3) + (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3) - math.sin(-math.pi/6 - 2*math.pi/3) - (-1)*math.sin(-math.pi/6 + 2*math.pi/3)) - self.Ls - self.Ls, -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6-input_variable[4]) - math.sin(-math.pi/6-input_variable[4]))],
    	                   [-(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 - input_variable[4]) + (-1)*math.sin(math.pi/2 - input_variable[4] - 2*math.pi/3)), -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 - input_variable[4] + 2*math.pi/3) + (-1)*math.sin(math.pi/2 - input_variable[4] - 2*math.pi/3)), -(2*self.wr*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2)) - self.Lrs]
    	                  ]                      
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        own_matrix = [input_variable[0]*self.Rs - input_variable[1]*self.Rs + input_variable[3]*(2*self.wc*self.wr*input_variable[2]*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.cos(math.pi/2 + input_variable[4]) + (-1)*math.cos(math.pi/6 - input_variable[4])),
                    input_variable[1]*self.Rs - (-input_variable[0]-input_variable[1])*self.Rs + input_variable[3]*(2*self.wc*self.wr*input_variable[2]*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(-(-1)*math.cos(math.pi/6 - input_variable[4]) + math.cos(-math.pi/6 - input_variable[4])),
                   input_variable[2]*self.Rr - self.Urxx - moment_pd(t, self.t0, self.t2, self.Ur - self.Urxx) - input_variable[3]*(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(input_variable[0]*math.cos(math.pi/2 - input_variable[4]) + input_variable[1]*math.cos(math.pi/2 - input_variable[4] + 2*math.pi/3) + (-input_variable[0]-input_variable[1])*math.cos(math.pi/2 - input_variable[4] - 2*math.pi/3))]        
        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[-1, 0],
                        [0, -1],
                        [0, 0]
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[1, 0, 0],
                        [0, 1, 0],
                        [-1, -1, 0]
                        ] 
            return current_matrix

    def get_derw(self, input_variable, t):
        Melmag = (self.D - 0*self.delta)*self.wr*(2*self.wc*input_variable[2]*self.l*self.mu0)/(math.pi*self.delta)*(input_variable[0]*math.cos(math.pi/2 - input_variable[4]) + input_variable[1]*math.cos(math.pi/2 - input_variable[4] + 2*math.pi/3) + (-input_variable[0]-input_variable[1])*math.cos(math.pi/2 - input_variable[4] - 2*math.pi/3))
        derw = (moment_pd(t, self.t0, self.t2, self.M_max) - Melmag)/self.J
        return derw
    
    def get_w(self, input_variable):
        return input_variable[3]

    def time_interrupt(self):
        return []

    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if (self.position == 0):
            if ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 1):
            if ((self.x + self.image_width/2 > bus_x) and (self.y + self.image_height > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 2):
            if ((self.x> bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 3):
            if ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")

    def set_state_click(self, m_x, m_y):
        self.k_click = 0.1
        if ((m_x >= self.x + self.k_click*self.image_width) and (m_x <= self.x + self.image_width - self.k_click*self.image_width) and (m_y >= self.y + self.k_click*self.image_height) and (m_y <= self.y + self.image_height - self.k_click*self.image_height)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0 

    def rotation(self, m_x, m_y):
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 3):
                self.position = 0
            self.image_model_data = create_image_for_model("Image/SM/" + str(self.position) + ".png")
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = self.k_click*self.image_width
            self.delta_y = self.k_click*self.image_height
            self.image_model = self.canv.create_image(m_x - self.k_click*self.image_width, m_y - self.k_click*self.image_height,image = self.image_model_data, anchor = 'nw')

        
    def view_result(self, m_x, m_y):
        global n_fig
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):               
            return True
    
    def change_parameter_in_model(self, m_x, m_y, WIDTH):
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            self.state_change_parameter = 1
            self.mass_entry = []
            self.mass_var = []
            current_var = [self.Un,self.Ur,self.J, self.Rs,self.Rr,self.Ls,self.Lrs,self.l,self.tau, self.delta, self.wc, self.wr, self.M_max, self.t0, self.t2, self.Ir_start, self.w_start/2/math.pi, self.phi_start*180/math.pi]
            for i in range(len(self.var_text)):
                self.mass_var.append(StringVar(value=str(round(current_var[i], 3))))
                self.mass_entry.append(Entry(textvariable = self.mass_var[i], width = 12, relief = SOLID, borderwidth = 1, justify = CENTER))
            self.mass_canv_text = []
            for i in range(len(self.var_text)):
                self.mass_canv_text.append(self.canv.create_text(WIDTH/2, i*25, text = self.var_text[i], fill = "black", font = ("GOST Type A", "16"), anchor="ne"))
                self.mass_entry[i].place(x = WIDTH/2+ 20, y = i*25)
            self.mass_canv_text.append(self.canv.create_text(WIDTH/2, len(self.var_text)*25 + 25, text = "Синхронное индуктивное сопротивление в УР, Ом: " + str(round(100*math.pi*((2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)+(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*math.sin(math.pi/2-2*math.pi/3)*math.cos(2*math.pi/3)+(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*math.sin(math.pi/2+2*math.pi/3)*math.cos(2*math.pi/3) + self.Ls), 3)), fill = "black", font = ("GOST Type A", "16"), anchor="center"))
            self.mass_canv_text.append(self.canv.create_text(WIDTH/2, (1+len(self.var_text))*25 + 25, text = "Действующее значение ЭДС генератора в УР, кВ: " + str(round(100/1000*math.pi*(math.sqrt(2)*self.wc*self.wr*self.Ur/self.Rr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi), 3)), fill = "black", font = ("GOST Type A", "16"), anchor="center"))
            self.mass_canv_text.append(self.canv.create_text(WIDTH/2, (2+len(self.var_text))*25 + 25, text = "Выбор существующего генератора", fill = "black", font = ("GOST Type A", "16"), anchor="center"))
            self.list_example.place(x = WIDTH/2 - 50, y = (3+len(self.var_text))*25 + 25)

    def set_parameter_in_model(self):
        print(self.list_example.get())
        if (self.list_example.get() == "Пользовательский"):
            for i in range(len(self.mass_var)):
                if (i == 0):
                    self.Un = float(self.mass_var[i].get())
                elif (i == 1):
                    self.Ur = float(self.mass_var[i].get())
                elif (i == 2):
                    self.J = float(self.mass_var[i].get())
                elif (i == 3):
                    self.Rs = float(self.mass_var[i].get())
                elif (i == 4):
                    self.Rr = float(self.mass_var[i].get())
                elif (i == 5):
                    self.Ls = float(self.mass_var[i].get())
                elif (i == 6):
                    self.Lrs = float(self.mass_var[i].get())
                elif (i == 7):
                   self.l = float(self.mass_var[i].get())
                elif (i == 8):
                    self.tau = float(self.mass_var[i].get())
                elif (i == 9):
                    self.delta = float(self.mass_var[i].get())
                elif (i == 10):
                    self.wc = float(self.mass_var[i].get())
                elif (i == 11):
                    self.wr = float(self.mass_var[i].get())
                elif (i == 12):
                    self.M_max = float(self.mass_var[i].get())
                elif (i == 13):
                    self.t0 = float(self.mass_var[i].get())
                elif (i == 14):
                    self.t2 = float(self.mass_var[i].get())
                elif (i == 15):
                    self.Ir_start = float(self.mass_var[i].get())
                elif (i == 16):
                    self.w_start = float(self.mass_var[i].get()) * 2 * math.pi
                elif (i == 17):
                    self.phi_start = float(self.mass_var[i].get()) * math.pi / 180
        else:
            if (self.list_example.get() == "ТВФ-63-2УЗ"):
                current_index = 0
            if (self.list_example.get() == "ТВФ-110-2ЕУЗ"):
                current_index = 1
            if (self.list_example.get() == "ТВФ-120-2УЗ"):
                current_index = 2
            if (self.list_example.get() == "ТВВ-160-2ЕУЗ"):
                current_index = 3
            if (self.list_example.get() == "ТГВ-200-2УЗ"):
                current_index = 4
            if (self.list_example.get() == "ТВВ-320-2ЕУЗ"):
                current_index = 5
            if (self.list_example.get() == "ТГВ-500-4УЗ"):
                current_index = 6
            if (self.list_example.get() == "390H"):
                current_index = 7
            for i in range(len(self.mass_var)):
                if (i == 0):
                    self.Un = self.example_SM[current_index][i]
                elif (i == 1):
                    self.Ur = self.example_SM[current_index][i]
                elif (i == 2):
                    self.J = self.example_SM[current_index][i]
                elif (i == 3):
                    self.Rs = self.example_SM[current_index][i]
                elif (i == 4):
                    self.Rr = self.example_SM[current_index][i]
                elif (i == 5):
                    self.Ls = self.example_SM[current_index][i]
                elif (i == 6):
                    self.Lrs = self.example_SM[current_index][i]
                elif (i == 7):
                   self.l = self.example_SM[current_index][i]
                elif (i == 8):
                    self.tau = self.example_SM[current_index][i]
                elif (i == 9):
                    self.delta = self.example_SM[current_index][i]
                elif (i == 10):
                    self.wc = self.example_SM[current_index][i]
                elif (i == 11):
                    self.wr = self.example_SM[current_index][i]
                elif (i == 12):
                    self.M_max = float(self.mass_var[i].get())
                elif (i == 13):
                    self.t0 = float(self.mass_var[i].get())
                elif (i == 14):
                    self.t2 = float(self.mass_var[i].get())
                elif (i == 15):
                    self.Ir_start = float(self.mass_var[i].get())
                elif (i == 16):
                    self.w_start = float(self.mass_var[i].get()) * 2 * math.pi
                elif (i == 17):
                    self.phi_start = float(self.mass_var[i].get()) * math.pi / 180

            self.Urxx = self.Un/math.sqrt(3)*1000*self.Rr*math.pi*self.delta*math.pi/(100*math.pi*math.sqrt(2)*self.wc*self.wr*self.mu0*2*self.tau*self.l)
            self.Ir_start = self.Urxx/self.Rr
        self.D = 2*self.tau/math.pi
    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y

class Static_load:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    position = 0
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    #R = 733.8/100
    R = 60
    Lc = 0

    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.list_example = ttk.Combobox(self.root, values = [
        "Пользовательский",
        ])
        self.list_example.current(0)
        self.image_model_data = create_image_for_model("Image/Static Load/" + str(self.position) + ".png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')
    
    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def get_first(self):
        return ([0, 0, 0])

    def get_main_determinant(self, input_variable):
        main_determinant = [[-self.Lc, self.Lc, 0],
                            [0, -self.Lc, self.Lc],
                            [0, 0, -self.Lc]
                            ]     	                    
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        own_matrix = [input_variable[0]*self.R - input_variable[1]*self.R,
                    input_variable[1]*self.R - input_variable[2]*self.R,
                    input_variable[2]*self.R
                    ]  
        return own_matrix
    
    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1],
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1],
                        ] 
            return current_matrix

    def time_interrupt(self):
        return []

    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if (self.position == 0):
            if ((self.x > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 1):
            if ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 2):
            if ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 3):
            if ((self.x + self.image_width/2 > bus_x) and (self.y + self.image_height > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")


    def set_state_click(self, m_x, m_y):
        self.k_click = 0.1
        if ((m_x >= self.x + self.k_click*self.image_width) and (m_x <= self.x + self.image_width - self.k_click*self.image_width) and (m_y >= self.y + self.k_click*self.image_height) and (m_y <= self.y + self.image_height - self.k_click*self.image_height)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0

    def rotation(self, m_x, m_y):
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 3):
                self.position = 0
            self.image_model_data = create_image_for_model("Image/Static Load/" + str(self.position) + ".png")
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = self.k_click*self.image_width
            self.delta_y = self.k_click*self.image_height
            self.image_model = self.canv.create_image(m_x - self.k_click*self.image_width, m_y - self.k_click*self.image_height,image = self.image_model_data, anchor = 'nw')

        
    def view_result(self, m_x, m_y):
        pass

    def change_parameter_in_model(self, m_x, m_y, WIDTH):
        pass

    def set_parameter_in_model(self):
        pass


    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y

class Electrical_system:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    position = 0
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    Lc = 0.2/(100*math.pi)
    Uc = 6386.3621*math.sqrt(3)*10
    fc = 50
    phic = -1*math.pi/6

    var_text = ["Действующее значение напряженя, кВ:",
    "Частота, Гц:",
    "Начальная фаза напряжения, градус:",
    "Индуктивное сопротивление сети, Ом:",
    ]

    mass_entry = []
    mass_var = []

    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.list_example = ttk.Combobox(self.root, values = [
        "Пользовательский",
        ])
        self.list_example.current(0)
        self.image_model_data = create_image_for_model("Image/Electrical System/" + str(self.position) + ".png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')
    
    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def get_first(self):
        return ([0, 0, 0])

    def get_main_determinant(self, input_variable):
        main_determinant = [[-self.Lc, self.Lc, 0],
                            [0, -self.Lc, self.Lc],
                            [0, 0, -self.Lc]
                            ]                           
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        own_matrix = [self.Uc*math.sqrt(2)*math.sin(2*math.pi*self.fc*t + 0 + self.phic) - self.Uc*math.sqrt(2)*math.sin(2*math.pi*self.fc*t - 2*math.pi/3 + self.phic),
                    self.Uc*math.sqrt(2)*math.sin(2*math.pi*self.fc*t - 2*math.pi/3 + self.phic) - self.Uc*math.sqrt(2)*math.sin(2*math.pi*self.fc*t + 2*math.pi/3 + self.phic),
                    self.Uc*math.sqrt(2)*math.sin(2*math.pi*self.fc*t + 2*math.pi/3 + self.phic)
                    ]  
        return own_matrix
    
    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1],
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1],
                        ] 
            return current_matrix

    def time_interrupt(self):
        return []

    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if (self.position == 0):
            if ((self.x > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 1):
            if ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 2):
            if ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 3):
            if ((self.x + self.image_width/2 > bus_x) and (self.y + self.image_height > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")

    def set_state_click(self, m_x, m_y):
        self.k_click = 0.1
        if ((m_x >= self.x + self.k_click*self.image_width) and (m_x <= self.x + self.image_width - self.k_click*self.image_width) and (m_y >= self.y + self.k_click*self.image_height) and (m_y <= self.y + self.image_height - self.k_click*self.image_height)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0

    def rotation(self, m_x, m_y):
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 3):
                self.position = 0
            self.image_model_data = create_image_for_model("Image/Electrical System/" + str(self.position) + ".png")
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = self.k_click*self.image_width
            self.delta_y = self.k_click*self.image_height
            self.image_model = self.canv.create_image(m_x - self.k_click*self.image_width, m_y - self.k_click*self.image_height,image = self.image_model_data, anchor = 'nw')

        
    def view_result(self, m_x, m_y):
        pass

    def change_parameter_in_model(self, m_x, m_y, WIDTH):
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            self.state_change_parameter = 1
            self.mass_entry = []
            self.mass_var = []
            current_var = [self.Uc/1000,self.fc, self.phic*180/math.pi,self.Lc*self.fc*2*math.pi]
            for i in range(len(self.var_text)):
                self.mass_var.append(StringVar(value=str(round(current_var[i], 3))))
                self.mass_entry.append(Entry(textvariable = self.mass_var[i], width = 12, relief = SOLID, borderwidth = 1, justify = CENTER))
            self.mass_canv_text = []
            for i in range(len(self.var_text)):
                self.mass_canv_text.append(self.canv.create_text(WIDTH/2, i*25, text = self.var_text[i], fill = "black", font = ("GOST Type A", "16"), anchor="ne"))
                self.mass_entry[i].place(x = WIDTH/2+ 20, y = i*25)  

    def set_parameter_in_model(self):
        for i in range(len(self.mass_var)):
            if (i == 0):
                self.Uc = float(self.mass_var[i].get())*1000
            elif (i == 1):
                self.fc = float(self.mass_var[i].get())
            elif (i == 2):
                self.phic = float(self.mass_var[i].get())*math.pi/180
            elif (i == 3):
                self.Lc = float(self.mass_var[i].get())/self.fc/2/math.pi

    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y

class AM:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    position = 0
    switch_time_Q = [[],[]]
    position_switch_Q = True
    help_var_switch_Q = False
    toff= 0
    delta_x = 0
    delta_y = 0
    k_click = 0.1

    p = 2
    tau = 1.775
    l = 3.5
    wc = 14
    wr = 24
    mu0 = 4 * math.pi * (10 ** (-7))
    delta = 0.065
    Rc = 1
    Rr = 2
    Roff = 0
    Lcs = 0.00126
    Lrs = 0.00126*5
    J = 0.1
    D = 2*tau/math.pi

    var_text = [
    "Число пар полюсов, шт:",
    "Момент инерции ротора, кг*м2:",
    "Активное сопротивление обмотки статора, Ом:",
    "Активное сопротивление обмотки ротора, Ом:",
    "Индуктивность поля рассеяния обмотки статора, Гн:",
    "Индуктивность поля рассеяния обмотки ротора, Гн:",
    "Длина машины, м:",
    "Полюсное деление машины, м:",
    "Длина воздушного зазора, м:",
    "Число витков обмотки статора, шт:",
    "Число витков обмотки ротора, шт:",
    "Моменты времени, при которых контакты выключателя замыкаются, с:",
    "Моменты времени, при которых контакты выключателя размыкаются, с:"  
    ]

    mass_entry = []
    mass_var = []

    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.list_example = ttk.Combobox(self.root, values = [
        "Пользовательский",
        ])
        self.list_example.current(0)
        self.image_model_data = create_image_for_model("Image/AM/" + str(self.position) + ".png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')
    
    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def get_first(self):
        return ([0, 0, 0, 0, 0, 0, 0, 0])

    def get_main_determinant(self, input_variable):
        main_determinant = [[-(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2) - (-1)*math.sin(math.pi/6)) - self.Lcs, -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 + 2*math.pi/3) - (-1)*math.sin(math.pi/6 - 2*math.pi/3)) + self.Lcs, -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 - 2*math.pi/3) - (-1)*math.sin(math.pi/6 + 2*math.pi/3)), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 + input_variable[7]*self.p) - (-1)*math.sin(math.pi/6 - input_variable[7]*self.p)), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 + input_variable[7]*self.p + 2*math.pi/3) - (-1)*math.sin(math.pi/6 - input_variable[7]*self.p - 2*math.pi/3)), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 + input_variable[7]*self.p - 2*math.pi/3) - (-1)*math.sin(math.pi/6 - input_variable[7]*self.p + 2*math.pi/3))],
                    [-(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6) - math.sin(-math.pi/6)), -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6 - 2*math.pi/3) - math.sin(-math.pi/6 - 2*math.pi/3)) - self.Lcs, -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6 + 2*math.pi/3) - math.sin(-math.pi/6 + 2*math.pi/3)) + self.Lcs, -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6 - input_variable[7]*self.p) - math.sin(-math.pi/6 - input_variable[7]*self.p)), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6 - input_variable[7]*self.p - 2*math.pi/3) - math.sin(-math.pi/6 - input_variable[7]*self.p - 2*math.pi/3)), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6 - input_variable[7]*self.p + 2*math.pi/3) - math.sin(-math.pi/6 - input_variable[7]*self.p + 2*math.pi/3))],
                    [-(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6), -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6 - 2*math.pi/3), -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6 + 2*math.pi/3) - self.Lcs, -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6 - input_variable[7]*self.p), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6 - input_variable[7]*self.p - 2*math.pi/3), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6 - input_variable[7]*self.p + 2*math.pi/3)],
                    [-(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(math.pi/2-input_variable[7]*self.p-0), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(math.pi/2-input_variable[7]*self.p+2*math.pi/3), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(math.pi/2-input_variable[7]*self.p-2*math.pi/3), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(math.pi/2-0) - self.Lrs, -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(math.pi/2+2*math.pi/3), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(math.pi/2-2*math.pi/3)],
                    [-(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(-1)*math.sin(math.pi/6+input_variable[7]*self.p-0), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(-1)*math.sin(math.pi/6+input_variable[7]*self.p-2*math.pi/3), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(-1)*math.sin(math.pi/6+input_variable[7]*self.p+2*math.pi/3), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(-1)*math.sin(math.pi/6+0), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(-1)*math.sin(math.pi/6-2*math.pi/3) - self.Lrs, -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(-1)*math.sin(math.pi/6+2*math.pi/3)],
                    [-(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6+input_variable[7]*self.p-0), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6+input_variable[7]*self.p-2*math.pi/3), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6+input_variable[7]*self.p+2*math.pi/3), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6+0), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6-2*math.pi/3), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*math.sin(-math.pi/6+2*math.pi/3) - self.Lrs]
                   ]                   
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        if (self.position_switch_Q == False):
            self.Roff = 50000/0.01*(t - self.toff)
        own_matrix = [input_variable[0]*(self.Rc + self.Roff) - input_variable[1]*(self.Rc + self.Roff) + (4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*input_variable[6]*self.p*(input_variable[3]*math.cos(math.pi/2 + input_variable[7]*self.p) + input_variable[4]*math.cos(math.pi/2 + input_variable[7]*self.p + 2*math.pi/3) + input_variable[5]*math.cos(math.pi/2 + input_variable[7]*self.p - 2*math.pi/3) + (-1)*input_variable[3]*math.cos(math.pi/6 - input_variable[7]*self.p) + (-1)*input_variable[4]*math.cos(math.pi/6 - input_variable[7]*self.p - 2*math.pi/3) + (-1)*input_variable[5]*math.cos(math.pi/6 - input_variable[7]*self.p + 2*math.pi/3)),
                    input_variable[1]*(self.Rc + self.Roff) - input_variable[2]*(self.Rc + self.Roff) + (4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*input_variable[6]*self.p*(input_variable[3]*math.cos(math.pi/6 - input_variable[7]*self.p) + input_variable[4]*math.cos(math.pi/6 - input_variable[7]*self.p - 2*math.pi/3) + input_variable[5]*math.cos(math.pi/6 - input_variable[7]*self.p + 2*math.pi/3) + input_variable[3]*math.cos(-math.pi/6 - input_variable[7]*self.p) + input_variable[4]*math.cos(-math.pi/6 - input_variable[7]*self.p - 2*math.pi/3) + input_variable[5]*math.cos(-math.pi/6 - input_variable[7]*self.p + 2*math.pi/3)),
                    input_variable[2]*(self.Rc + self.Roff) - (4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*input_variable[6]*self.p*(input_variable[3]*math.cos(-math.pi/6 - input_variable[7]*self.p) + input_variable[4]*math.cos(-math.pi/6 - input_variable[7]*self.p - 2*math.pi/3) + input_variable[5]*math.cos(-math.pi/6 - input_variable[7]*self.p + 2*math.pi/3)),
                    input_variable[3]*self.Rr-input_variable[6]*self.p*(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(input_variable[0]*math.cos(math.pi/2-input_variable[7]*self.p)+input_variable[1]*math.cos(math.pi/2-input_variable[7]*self.p+2*math.pi/3)+input_variable[2]*math.cos(math.pi/2-input_variable[7]*self.p-2*math.pi/3)),
                    input_variable[4]*self.Rr+input_variable[6]*self.p*(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(-1)*(input_variable[0]*math.cos(math.pi/6+input_variable[7]*self.p)+input_variable[1]*math.cos(math.pi/6+input_variable[7]*self.p-2*math.pi/3)+input_variable[2]*math.cos(math.pi/6+input_variable[7]*self.p+2*math.pi/3)),
                    input_variable[5]*self.Rr+input_variable[6]*self.p*(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(math.pi*self.delta*math.pi)*(input_variable[0]*math.cos(-math.pi/6+input_variable[7]*self.p)+input_variable[1]*math.cos(-math.pi/6+input_variable[7]*self.p-2*math.pi/3)+input_variable[2]*math.cos(-math.pi/6+input_variable[7]*self.p+2*math.pi/3))
                    ]
        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[1, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0]
                        ] 
            return current_matrix

    def get_derw(self, input_variable, t):
        Melmag = self.p*self.D*self.l*self.wr*(input_variable[3]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/math.pi*input_variable[7]*self.p-self.tau/2, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p)+input_variable[4]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/math.pi*input_variable[7]*self.p+self.tau/6, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p)+input_variable[5]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/math.pi*input_variable[7]*self.p-7*self.tau/6, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p))
        derw = (-0*math.tanh(input_variable[6]) - Melmag)/self.J
        return derw
    
    def get_w(self, input_variable):
        return input_variable[6]

    def get_position_switches(self, t):
        delta_time_swicth = 1000 #dlya nachalnogo sravneniya
        index_switcth = 0
        for i in range(len(self.switch_time_Q)):
            for j in self.switch_time_Q[i]:
                if (((t - j) > 0) and ((t - j) < delta_time_swicth)):           
                    delta_time_swicth = (t - j)
                    index_switcth = i
        if (index_switcth == 0):
            self.position_switch_Q = True
            self.help_var_switch_Q == False
            self.Roff = 0
        elif (index_switcth == 1):
            self.position_switch_Q = False
            if (self.help_var_switch_Q == False):
                self.toff = t
                self.help_var_switch_Q = True

    def time_interrupt(self):
        list_time_interrupt = []
        for i in range(len(self.switch_time_Q)):
            for j in self.switch_time_Q[i]:
                if (i == 0):
                    list_time_interrupt.append(j)
                if (i == 1):
                    if (j == 0):
                        list_time_interrupt.append(j)
                    else:
                        list_time_interrupt.append(j + 0.01)
        return list_time_interrupt


    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if (self.position == 0):
            if ((self.x > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_Q == False):
                    return ("Q:OFF_SWITCH")
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 1):
            if ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
                if (self.position_switch_Q == False):
                    return ("Q:OFF_SWITCH")
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 2):
            if ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_Q == False):
                    return ("Q:OFF_SWITCH")
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 3):
            if ((self.x + self.image_width/2 > bus_x) and (self.y + self.image_height > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
                if (self.position_switch_Q == False):
                    return ("Q:OFF_SWITCH")
                return ("Q:ON_SWITCH")
            else:
                return ("none")

    def set_state_click(self, m_x, m_y):
        self.k_click = 0.1
        if ((m_x >= self.x + self.k_click*self.image_width) and (m_x <= self.x + self.image_width - self.k_click*self.image_width) and (m_y >= self.y + self.k_click*self.image_height) and (m_y <= self.y + self.image_height - self.k_click*self.image_height)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0 

    def rotation(self, m_x, m_y):
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 3):
                self.position = 0
            self.image_model_data = create_image_for_model("Image/AM/" + str(self.position) + ".png")
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = self.k_click*self.image_width
            self.delta_y = self.k_click*self.image_height
            self.image_model = self.canv.create_image(m_x - self.k_click*self.image_width, m_y - self.k_click*self.image_height,image = self.image_model_data, anchor = 'nw')

        
    def view_result(self, m_x, m_y):
        global n_fig
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):               
            return True
    
    def change_parameter_in_model(self, m_x, m_y, WIDTH):
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            self.state_change_parameter = 1
            self.mass_entry = []
            self.mass_var = []
            switch_time_Q_on_string = ""
            for i in self.switch_time_Q[0]:
                switch_time_Q_on_string = switch_time_Q_on_string + str(i) + ", "
            switch_time_Q_off_string = ""
            for i in self.switch_time_Q[1]:
                switch_time_Q_off_string = switch_time_Q_off_string + str(i) + ", "
            current_var = [self.p, self.J, self.Rc,self.Rr,self.Lcs,self.Lrs,self.l,self.tau, self.delta, self.wc, self.wr, switch_time_Q_on_string, switch_time_Q_off_string]
            for i in range(len(self.var_text)):
                self.mass_var.append(StringVar(value=str(current_var[i])))
                self.mass_entry.append(Entry(textvariable = self.mass_var[i], width = 12, relief = SOLID, borderwidth = 1, justify = CENTER))
            self.mass_canv_text = []
            for i in range(len(self.var_text)):
                self.mass_canv_text.append(self.canv.create_text(WIDTH/2, i*25, text = self.var_text[i], fill = "black", font = ("GOST Type A", "16"), anchor="ne"))
                self.mass_entry[i].place(x = WIDTH/2+ 20, y = i*25)

    def set_parameter_in_model(self):
        for i in range(len(self.mass_var)):
            if (i == 0):
                self.p = float(self.mass_var[i].get())
            elif (i == 1):
                self.J = float(self.mass_var[i].get())
            elif (i == 2):
                self.Rc = float(self.mass_var[i].get())
            elif (i == 3):
                self.Rr = float(self.mass_var[i].get())
            elif (i == 4):
                self.Lcs = float(self.mass_var[i].get())
            elif (i == 5):
                self.Lrs = float(self.mass_var[i].get())
            elif (i == 6):
                self.l = float(self.mass_var[i].get())
            elif (i == 7):
                self.tau = float(self.mass_var[i].get())
            elif (i == 8):
                self.delta = float(self.mass_var[i].get())
            elif (i == 9):
                self.wc = float(self.mass_var[i].get())
            elif (i == 10):
                self.wr = float(self.mass_var[i].get())
            elif (i == 11):
                self.switch_time_Q[0] = []
                for j in self.mass_var[i].get().split(", "):
                    if (j != ""):
                        self.switch_time_Q[0].append(float(j))  
            elif (i == 12):
                self.switch_time_Q[1] = []
                for j in self.mass_var[i].get().split(", "):
                    if (j != ""):
                        self.switch_time_Q[1].append(float(j)) 

    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y

class KZ_Bus:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    switch_time_Q = [[7],[0]]
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    position_switch_Q = True
    help_var_switch_Q = False
    help_var_switch_Qon = False
    toff= 0
    ton = 0
    R = 0.0001
    Roff = 0
    Lc = 0.0002
    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.image_model_data = create_image_for_model("Image/KZ_Bus.png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')
    
    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def get_first(self):
        return ([0, 0, 0])

    def get_main_determinant(self, input_variable):
        main_determinant = [[-self.Lc, self.Lc, 0],
                            [0, -self.Lc, self.Lc],
                            [0, 0, -self.Lc]
                            ]                             
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        if ((self.position_switch_Q == False) and ((t - self.toff) < 0.01)):
            self.Lc= 50000/0.01*(t - self.toff)
        if ((self.position_switch_Q == False) and ((t - self.toff) > 0.01)):
            self.Lc = 0  
        if ((self.position_switch_Q == True) and ((t - self.ton) < 0.01)):
            self.Lc= -0.0005/0.01*(t - self.ton) + 0.0005
        if ((self.position_switch_Q == True) and ((t - self.ton) > 0.01)):
            self.Lc = 0
        self.Roff = 0
        own_matrix = [input_variable[0]*(self.R+self.Roff) - input_variable[1]*(self.R+self.Roff),
                    input_variable[1]*(self.R+self.Roff) - input_variable[2]*(self.R+self.Roff),
                    input_variable[2]*(self.R+self.Roff)
                    ]  
        return own_matrix
    
    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1],
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1],
                        ] 
            return current_matrix

    def get_position_switches(self, t):
        delta_time_swicth = 1000 #dlya nachalnogo sravneniya
        index_switcth = 0
        for i in range(len(self.switch_time_Q)):
            for j in self.switch_time_Q[i]:
                if (((t - j) >= 0) and ((t - j) < delta_time_swicth)):           
                    delta_time_swicth = (t - j)
                    index_switcth = i
        if (index_switcth == 0):
            self.position_switch_Q = True
            self.help_var_switch_Q == False
            if (self.help_var_switch_Qon == True):
                self.ton = t
                self.help_var_switch_Qon = False
            self.Roff = 0
        elif (index_switcth == 1):
            self.position_switch_Q = False
            self.help_var_switch_Qon = True
            if (self.help_var_switch_Q == False):
                self.toff = t
                self.help_var_switch_Q = True
        print(self.position_switch_Q)

    def time_interrupt(self):
        list_time_interrupt = []
        for i in range(len(self.switch_time_Q)):
            for j in self.switch_time_Q[i]:
                if (i == 0):
                    list_time_interrupt.append(j)
                if (i == 1):
                    if (j == 0):
                        list_time_interrupt.append(j)
                    else:
                        list_time_interrupt.append(j + 0.01)
        return list_time_interrupt

    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if ((self.x > bus_x) and (self.y + self.image_height > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
            if (self.position_switch_Q == False):
                    return ("Q:OFF_SWITCH")
            return ("Q:ON_SWITCH")
        else:
            return ("none")


    def set_state_click(self, m_x, m_y):
        self.k_click = 0.1
        if ((m_x >= self.x + self.k_click*self.image_width) and (m_x <= self.x + self.image_width - self.k_click*self.image_width) and (m_y >= self.y + self.k_click*self.image_height) and (m_y <= self.y + self.image_height - self.k_click*self.image_height)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0

    def rotation(self, m_x, m_y):
        pass
        
    def view_result(self, m_x, m_y):
        pass

    def change_parameter_in_model(self, m_x, m_y, WIDTH):
        pass

    def set_parameter_in_model(self):
        pass


    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y

class KZ_single_phase:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    switch_time_Q = [[7],[0]]
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    position_switch_Q = True
    help_var_switch_Q = False
    help_var_switch_Qon = False
    toff= 0
    ton = 0
    R = 0.0001
    Roff = 0
    Lc = 0.0002
    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.image_model_data = create_image_for_model("Image/KZ_single_phase.png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')
    
    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def get_first(self):
        return ([0])

    def get_main_determinant(self, input_variable):
        main_determinant = [[self.Lc]
                            ]                             
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        if ((self.position_switch_Q == False) and ((t - self.toff) < 0.01)):
            self.Lc= 50000/0.01*(t - self.toff)
        if ((self.position_switch_Q == False) and ((t - self.toff) > 0.01)):
            self.Lc = 0  
        if ((self.position_switch_Q == True) and ((t - self.ton) < 0.01)):
            self.Lc= -0.005/0.01*(t - self.ton) + 0.005
        if ((self.position_switch_Q == True) and ((t - self.ton) > 0.01)):
            self.Lc = 0
        self.Roff = 0
        own_matrix = [-input_variable[0]*(self.R+self.Roff)
                    ]  
        return own_matrix
    
    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            if (self.position_switch_Q == True):
                voltage_matrix = [[-1, -1, -1]
                            ] 
            if (self.position_switch_Q == False):
                voltage_matrix = [[-1]
                            ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            if (self.position_switch_Q == True):
                current_matrix = [[-1],
                            [0],
                            [0]
                            ] 
            if (self.position_switch_Q == False):
                current_matrix = [[-1],
                [0],
                [0]
                            ] 
            return current_matrix

    def get_position_switches(self, t):
        delta_time_swicth = 1000 #dlya nachalnogo sravneniya
        index_switcth = 0
        for i in range(len(self.switch_time_Q)):
            for j in self.switch_time_Q[i]:
                if (((t - j) >= 0) and ((t - j) < delta_time_swicth)):           
                    delta_time_swicth = (t - j)
                    index_switcth = i
        if (index_switcth == 0):
            self.position_switch_Q = True
            self.help_var_switch_Q == False
            if (self.help_var_switch_Qon == True):
                self.ton = t
                self.help_var_switch_Qon = False
            self.Roff = 0
        elif (index_switcth == 1):
            self.position_switch_Q = False
            self.help_var_switch_Qon = True
            if (self.help_var_switch_Q == False):
                self.toff = t
                self.help_var_switch_Q = True
        #print(self.position_switch_Q)

    def time_interrupt(self):
        list_time_interrupt = []
        for i in range(len(self.switch_time_Q)):
            for j in self.switch_time_Q[i]:
                if (i == 0):
                    list_time_interrupt.append(j)
                if (i == 1):
                    if (j == 0):
                        list_time_interrupt.append(j)
                    else:
                        list_time_interrupt.append(j + 0.01)
        return list_time_interrupt

    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
            if (self.position_switch_Q == False):
                    return ("Q:OFF_SWITCH")
            return ("Q:ON_SWITCH")
        else:
            return ("none")


    def set_state_click(self, m_x, m_y):
        self.k_click = 0.1
        if ((m_x >= self.x + self.k_click*self.image_width) and (m_x <= self.x + self.image_width - self.k_click*self.image_width) and (m_y >= self.y + self.k_click*self.image_height) and (m_y <= self.y + self.image_height - self.k_click*self.image_height)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0

    def rotation(self, m_x, m_y):
        pass
        
    def view_result(self, m_x, m_y):
        pass

    def change_parameter_in_model(self, m_x, m_y, WIDTH):
        pass

    def set_parameter_in_model(self):
        pass


    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y
