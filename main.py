import ntcore
import time
import tkinter as tk
from tkinter import *

from functools import partial
from ntcore import BooleanPublisher, DoublePublisher

current_elevator_level = 1
current_branch_number = 1


def set_elevator_level(level: int, elevator_sub: DoublePublisher):
    global current_elevator_level
    current_elevator_level = level
    elevator_sub.set(level)


def set_branch_number(number: int, branch_sub: DoublePublisher):
    global current_branch_number
    current_branch_number = number
    branch_sub.set(number)



if __name__ == "__main__":
    # Set up coms
    inst = ntcore.NetworkTableInstance.getDefault()
    
    table = inst.getTable("RobotController")
    elevator_pub = table.getDoubleTopic("elevator").publish()
    branch_pub = table.getDoubleTopic("branch").publish()
    feeder_pub = table.getDoubleTopic("feeder").publish()
    inner_pub = table.getBooleanTopic("inner").publish()
    led_pub = table.getBooleanTopic("led").publish()
    allince_sub = table.getBooleanTopic("allince").subscribe(True)

    inst.startClient4("example")
    inst.setServerTeam(7112)
    inst.startDSClient()  # gets the robot IP from the DS

    # Set up screen
    screen = tk.Tk()
    screen.geometry('1920x1080')

    # funcs

    def change_color(button):
        global last_button
        if last_button :
            last_button.config(image=branch[0],bg='blue')
        button.config(image=branch[1], bg='red')
        last_button = button
    
    def change_feeder_color(button):
        global last_feeder
        last_feeder.config(image = feeder[0])
        for i in range(2):
            if button == feeder_button[i]:
                button.config(image=feeder[1])
                last_feeder = button

    def change_color_for_Level(button):
        global last_L
        if last_L :
            for i in range(4):
                if last_L == level_button[i]: 
                    last_L.config(image=level_img[0][i], bg="blue")
        for i in range(4):
            if button == level_button[i]: 
                button.config(image=level_img[1][i], bg='red')
        last_L = button

    def change_inner_color(button):
        global is_inner
        if is_inner == False:
            button.config(image = inner[1] , text = "outer")
            inner_pub.set(False)
            is_inner = True
        else:
            button.config(image = inner[0], text = "inner")
            inner_pub.set(True)
            is_inner = False

    def set_val_for_Led():
        global last_led
        if last_led == False:
            led_pub.set(False)
            last_led = True
        else:
            led_pub.set(True)
            last_led = False

    def set_vals_for_Levels(button, number: int, elevator_sub: DoublePublisher):
        set_elevator_level(number, elevator_sub)
        change_color_for_Level(button)


    def set_vals_for_Branches(button, number: int, branch_sub: DoublePublisher):
        set_branch_number(number, branch_sub)
        change_color(button)
        change_feeder_color(button)
    #images
    level_img = [[PhotoImage(file='img/level/L4.png'),PhotoImage(file='img/level/L3.png'),PhotoImage(file='img/level/L2.png'),PhotoImage(file='img/level/L1.png')],
                [PhotoImage(file='img/level/L4_pressed.png'),PhotoImage(file='img/level/L3_pressed.png'),PhotoImage(file='img/level/L2_pressed.png'),PhotoImage(file='img/level/L1_pressed.png')]]
    
    branch = [PhotoImage(file='img/reef/reef_button.png'),PhotoImage(file='img/reef/reef_button_pressed.png')]
    reef = [PhotoImage(file='img/reef/Reef.png'),PhotoImage(file='img/reef/Reef_red.png')]

    feeder = [PhotoImage(file='feeder button.png'), PhotoImage(file='feeder_button_pressed.png')]

    inner = [PhotoImage(file='inner button.png'),PhotoImage(file='inner button pressed.png') ]


    # Add image file 
    bg = PhotoImage(file = "img/DS_bg.png") 
    
    # Create Canvas 
    canvas1 = Canvas( screen, width = 1920, height = 1080) 
    
    canvas1.pack(fill = "both", expand = True) 
    
    # Display image 
    canvas1.create_image( 0, 0, image = bg,  anchor = "nw") 

    if allince_sub.get():
        Reef = tk.Label(screen, image=reef[0])
    else:
        Reef = tk.Label(screen,image=reef[1])
    Reef.place(x=-250,y=-140)
    

    last_button = None
    last_L = None
    last_feeder = None
    is_inner = False
    last_led =  False

    # buttons 


    feeder_button_maping = [[150,50],[30,50]]
    feeder_button = [tk.Button(screen, text='right', ), tk.Button(screen, text='left')]

    for i in range(2):
        feeder_button[i].config(command=partial(set_vals_for_Branches, feeder_button[i], i+13, feeder_pub),image=branch[0], compound='center',font=('Ariel',20),bg='blue', borderwidth=5)
        feeder_button[i].place(x=feeder_button_maping[i][0],y=feeder_button_maping[i][1])

    feeder_inner_button = tk.Button(screen, text="inner", image=inner[0], compound='center',font=('Ariel',30), borderwidth=0,bg='gray0',activebackground='gray0')
    feeder_inner_button.config(command=partial(change_inner_color, feeder_inner_button))
    feeder_inner_button.place(x=35,y=270)

    led_button = tk.Button(screen, text="led", image=inner[0], compound='center',font=('Ariel',30), borderwidth=0,bg='gray0',activebackground='gray0')
    led_button.config(command=partial(set_val_for_Led))
    led_button.place(x=35,y=500)


    #creating levels

    level_button_maping = [[1070 + 50, 60],[1070 + 50, 230],[1070 + 50, 400],[1070 + 50, 570]]
    level_button = [tk.Button(screen),tk.Button(screen),tk.Button(screen),tk.Button(screen)]


    for i in range(len(level_button)):
        level_button[i].config(command=partial(set_vals_for_Levels,level_button[i],4-i,elevator_pub),text=('L' + str(4-i)), image=level_img[0][i], compound='center',font=('Ariel', 50),bg='blue')
        level_button[i].place(x=level_button_maping[i][0],y=level_button_maping[i][1])

    #creating branches
    branch_button_loction = [[370 + 250, 610],[470 + 250, 610],[610 + 250, 500],[710 + 250, 380],[710 + 250, 170],[610 + 250, 90],[470 + 250, 0],[370 + 250, 0],[220 + 250, 90],[120 + 250, 170],[120 + 250, 380],[220 + 250, 500]] 
    branch_button = [tk.Button(screen), tk.Button(screen),tk.Button(screen),tk.Button(screen), tk.Button(screen),tk.Button(screen),tk.Button(screen), tk.Button(screen),tk.Button(screen),tk.Button(screen), tk.Button(screen),tk.Button(screen)]
    if allince_sub.get():
        for i in range(len(branch_button)):
            branch_button[i].config(command=partial(set_vals_for_Branches,branch_button[i], i+1, branch_pub),text=i+1, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
            branch_button[i].place(x=branch_button_loction[i][0],y=branch_button_loction[i][1])
    else:
        branch_button[0].config(command=partial(set_vals_for_Branches,branch_button[0], 7, branch_pub),text=1, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[1].config(command=partial(set_vals_for_Branches,branch_button[1], 8, branch_pub),text=2, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[2].config(command=partial(set_vals_for_Branches,branch_button[2], 9, branch_pub),text=3, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[3].config(command=partial(set_vals_for_Branches,branch_button[3], 10, branch_pub),text=4, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[4].config(command=partial(set_vals_for_Branches,branch_button[4], 11, branch_pub),text=5, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[5].config(command=partial(set_vals_for_Branches,branch_button[5], 12, branch_pub),text=6, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[6].config(command=partial(set_vals_for_Branches,branch_button[6], 1, branch_pub),text=7, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[7].config(command=partial(set_vals_for_Branches,branch_button[7], 2, branch_pub),text=8, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[8].config(command=partial(set_vals_for_Branches,branch_button[8], 3, branch_pub),text=9, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[9].config(command=partial(set_vals_for_Branches,branch_button[9], 4, branch_pub),text=10, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[10].config(command=partial(set_vals_for_Branches,branch_button[10], 5, branch_pub),text=11, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[11].config(command=partial(set_vals_for_Branches,branch_button[11], 6, branch_pub),text=12, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        for i in range(len(branch_button)):
            branch_button[i].place(x=branch_button_loction[i][0],y=branch_button_loction[i][1])



    screen.mainloop()
