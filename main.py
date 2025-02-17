import ntcore
import time
import tkinter as tk
from tkinter import *

from functools import partial
from ntcore import DoublePublisher

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
    elevator_sub = table.getDoubleTopic("elevator").publish()
    branch_sub = table.getDoubleTopic("branch").publish()

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
            last_button.config(image=branch[0], bg='blue')
        button.config(image=branch[1], bg='red')
        last_button = button

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

    def set_vals_for_Levels(button, number: int, elevator_sub: DoublePublisher):
        set_elevator_level(number, elevator_sub)
        change_color_for_Level(button)


    def set_vals_for_Branches(button, number: int, branch_sub: DoublePublisher):
        set_branch_number(number, branch_sub)
        change_color(button)

    #images
    level_img = [[PhotoImage(file='img/level/L4.png'),PhotoImage(file='img/level/L3.png'),PhotoImage(file='img/level/L2.png'),PhotoImage(file='img/level/L1.png')],
                [PhotoImage(file='img/level/L4_pressed.png'),PhotoImage(file='img/level/L3_pressed.png'),PhotoImage(file='img/level/L2_pressed.png'),PhotoImage(file='img/level/L1_pressed.png')]]
    
    branch = [PhotoImage(file='img/reef/reef_button.png'),PhotoImage(file='img/reef/reef_button_pressed.png')]
    reef = PhotoImage(file='img/reef/Reef.png')

    feeder = PhotoImage(file='feeder button.png')

    # Add image file 
    bg = PhotoImage(file = "img/DS_bg.png") 
    
    # Create Canvas 
    canvas1 = Canvas( screen, width = 1920, height = 1080) 
    
    canvas1.pack(fill = "both", expand = True) 
    
    # Display image 
    canvas1.create_image( 0, 0, image = bg,  anchor = "nw") 

    Reef = tk.Label(screen, image=reef)
    Reef.place(x=-500,y=-140)
    

    last_button = None
    last_L = None

    # buttons 


    #creating levels
    level_button_maping = [[1070, 60],[1070, 230],[1070, 400],[1070, 570]]
    level_button = [tk.Button(screen),tk.Button(screen),tk.Button(screen),tk.Button(screen)]

    feeder_button = tk.Button(screen,text='feeder', image=feeder,compound='center',font=('Ariel', 50),  border=0, bg='gray1')
    feeder_button.config(command= partial(set_vals_for_Levels,feeder_button,0,elevator_sub))
    feeder_button.place(x=810,y=500)

    for i in range(len(level_button)):
        level_button[i].config(command=partial(set_vals_for_Levels,level_button[i],4-i,elevator_sub),text=('L' + str(4-i)), image=level_img[0][i], compound='center',font=('Ariel', 50),bg='blue')
        level_button[i].place(x=level_button_maping[i][0],y=level_button_maping[i][1])

    #creating branches
    branch_button_loction = [[370, 610],[470, 610],[610, 500],[710, 380],[710, 170],[610, 90],[470, 0],[370, 0],[220, 90],[120, 170],[120, 380],[220, 500]] 
    branch_button = [tk.Button(screen), tk.Button(screen),tk.Button(screen),tk.Button(screen), tk.Button(screen),tk.Button(screen),tk.Button(screen), tk.Button(screen),tk.Button(screen),tk.Button(screen), tk.Button(screen),tk.Button(screen)]

    for i in range(len(branch_button)):
        branch_button[i].config(command=partial(set_vals_for_Branches,branch_button[i], i+1, branch_sub),text=i+1, image=branch[0], compound='center',font=('Ariel',30),bg='blue')
        branch_button[i].place(x=branch_button_loction[i][0],y=branch_button_loction[i][1])


    screen.mainloop()
