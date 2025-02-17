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


def change_color(button):
    global last_button
    if last_button :
        last_button.config(bg="blue")
    button.config(bg='red')
    last_button = button

def change_color_for_Level(button):
    global last_L
    if last_L :
        last_L.config(bg="blue")
    button.config(bg='red')
    last_L = button

def set_vals_for_Levels(button, number: int, elevator_sub: DoublePublisher):
    set_elevator_level(number, elevator_sub)
    change_color_for_Level(button)


def set_vals_for_Branches(button, number: int, branch_sub: DoublePublisher):
    set_branch_number(number, branch_sub)
    change_color(button)




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

    #img= PhotoImage(file='background.png')
    # Define the PhotoImage Constructor by passing the image file
    #img = tk.PhotoImage(file='background.png', master=screen)
    #img_label = tk.Label(screen, image=img)


    #images
    L1 = PhotoImage(file='L4.png')
    L2 = PhotoImage(file='L3.png')
    L3 = PhotoImage(file='L2.png')
    L4 = PhotoImage(file='L1.png')
    branch = PhotoImage(file='reef_button.png')
    reef = PhotoImage(file='Reef.png')
    
    # static images

    # Add image file 
    bg = PhotoImage(file = "DS_bg.png") 
    
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

    '''reset = tk.Button(screen, text='reset', font=('Ariel', 50), bg='blue', bg='green', activebackground='red')
    reset
    reset.place(x=1000,y=1000)'''

    l4 = tk.Button(screen, text='L4', image=L1, compound='center', font=('Ariel', 50), bg='blue')
    l4.config(command= partial(set_vals_for_Levels,l4,4,elevator_sub))
    l4.pack()
    l4.place(x=1070, y=60)

    l3 = tk.Button(screen, text='L3', image=L2, compound='center', font=('Ariel', 50), bg='blue')
    l3.config(command= partial(set_vals_for_Levels,l3,3, elevator_sub))
    l3.place(x=1070, y=230)

    l2 = tk.Button(screen, text='L2', image=L3, compound='center', font=('Ariel', 50), bg='blue')
    l2.config(command= partial(set_vals_for_Levels,l2,2, elevator_sub))
    l2.place(x=1070, y=400)

    l1 = tk.Button(screen, text='L1', image=L4, compound='center', font=('Ariel', 50), bg='blue')
    l1.config(command= partial(set_vals_for_Levels,l1,1, elevator_sub))
    l1.place(x=1070, y=570)

    branch1 = tk.Button(screen, text='1', image=branch, compound='center',font=('Ariel', 30),bg='blue')
    branch1.config(command=partial(set_vals_for_Branches,branch1, 1, branch_sub))
    branch1.place(x=370, y=610)

    branch2 = tk.Button(screen, text='2', image=branch, compound='center',font=('Ariel', 30), bg='blue')
    branch2.config(command=partial(set_vals_for_Branches,branch2, 2, branch_sub))
    branch2.place(x=470, y=610)

    branch3 = tk.Button(screen, text='3', image=branch, compound='center',font=('Ariel', 30), bg='blue')
    branch3.config(command=partial(set_vals_for_Branches,branch3, 3, branch_sub))
    branch3.place(x=610, y=500)

    branch4 = tk.Button(screen, text='4', image=branch, compound='center',font=('Ariel', 30), bg='blue')
    branch4.config(command=partial(set_vals_for_Branches,branch4, 4, branch_sub))
    branch4.place(x=710, y=380)

    branch5 = tk.Button(screen, text='5', image=branch, compound='center',font=('Ariel', 30), bg='blue')
    branch5.config(command=partial(set_vals_for_Branches,branch5, 5, branch_sub))
    branch5.place(x=710, y=170)

    branch6 = tk.Button(screen, text='6', image=branch, compound='center',font=('Ariel', 30), bg='blue')
    branch6.config(command=partial(set_vals_for_Branches,branch6, 6, branch_sub))
    branch6.place(x=610, y=90)

    branch7 = tk.Button(screen, text='7', image=branch, compound='center',font=('Ariel', 30), bg='blue')
    branch7.config(command=partial(set_vals_for_Branches,branch7, 7, branch_sub))
    branch7.place(x=470, y=0)

    branch8 = tk.Button(screen, text='8', image=branch, compound='center',font=('Ariel', 30), bg='blue')
    branch8.config(command=partial(set_vals_for_Branches,branch8, 8, branch_sub))
    branch8.place(x=370, y=0)

    branch9 = tk.Button(screen, text='9', image=branch, compound='center',font=('Ariel', 30), bg='blue')
    branch9.config(command=partial(set_vals_for_Branches,branch9, 9, branch_sub))
    branch9.place(x=220, y=90)

    branch10 = tk.Button(screen, text='10', image=branch, compound='center',font=('Ariel', 30), bg='blue')
    branch10.config(command=partial(set_vals_for_Branches,branch10, 10, branch_sub))
    branch10.place(x=120, y=170)

    branch11 = tk.Button(screen, text='11', image=branch, compound='center',font=('Ariel', 30), bg='blue')
    branch11.config(command=partial(set_vals_for_Branches,branch11, 11, branch_sub))
    branch11.place(x=120, y=380)

    branch12 = tk.Button(screen, text='12', image=branch, compound='center',font=('Ariel', 30), bg='blue')
    branch12.config(command=partial(set_vals_for_Branches,branch12, 12, branch_sub))
    branch12.place(x=220, y=500)

    

    screen.mainloop()
