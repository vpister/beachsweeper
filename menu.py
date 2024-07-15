

from tkinter import *
from beach_sweeper import *

BACKGROUND = "#CAF2FF"

marker = None
level = 0

def menu():


    def change_level(arg):
        global level, marker
        locations = [(100,380), (270,410), (410,450), (560,440), (680,390)]

        if(marker):
            canvasMenu.delete(marker)
        level += arg
        level = max(min(level,len(locations)-1),0)
        marker = canvasMenu.create_image( 
                locations[level] ,
                image=guy
        )
    
    def select_level():
        global level
        if(level == 0):
            window.destroy()
            generate_lvl1(callback = menu)
        elif(level == 1):
            window.destroy()
            generate_lvl2(callback = menu)

    # Giving title to the gaming window 
    window = Tk() 
    window.title("Beach Sweeper") 

    # Display of Points Scored in Game 
    # TODO: Fix score update, it's broken
    

    label = Label(window,  
                text="Beach Sweeper Menu",  
                font=('consolas', 20)) 
    label.pack()  

    canvasMenu = Canvas(window, bg=BACKGROUND,  
                    height=640, width=800) 
    canvasMenu.pack() 
    
    window.update() 

    label = Label(window,  
                text="Beach Sweeper Menu",  
                font=('consolas', 20)) 
    label.pack()   
    
    window_width = window.winfo_width() 
    window_height = window.winfo_height() 
    screen_width = window.winfo_screenwidth() 
    screen_height = window.winfo_screenheight() 
    
    x = int((screen_width/2) - (window_width/2)) 
    y = int((screen_height/2) - (window_height/2)) 
    
    window.geometry(f"{window_width}x{window_height}+{x}+{y}") 

    bg_img = PhotoImage(file="menu.png")
    guy = PhotoImage(file="guy.png")
    canvasMenu.create_image( 
                (400, 
                 320) ,
                image=bg_img
            )

    window.bind('<Left>',lambda event,arg=-1:change_level(arg))
    window.bind('<Right>',lambda event,arg=1:change_level(arg))
    window.bind('<space>',lambda event:select_level())
    change_level(0)

    window.mainloop()


    

   



menu()