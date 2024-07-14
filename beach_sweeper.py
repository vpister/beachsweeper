from tkinter import *
from Board import Board

# from PIL import Image, ImageTK
import random 

# Initialising screen params
SPACE_SIZE = 32
WIDTH = 25*32 + 100
HEIGHT = 25*32
BACKGROUND = "#CAF2FF"
FONTSIZE= 14

def clicked(event): 

    """
    Identify clicked tile and take appropriate action.
    Handles victory and game over state.
    """
  
    x, y, click  = event.x, event.y, event.num
    if (x//SPACE_SIZE == board.undo_location[0]//SPACE_SIZE) \
        and (y//SPACE_SIZE == board.undo_location[1]//SPACE_SIZE):
        board.undo_operation()

    elif board.game_over_text:
        return
    
    elif 0 < x < board.width and 0<y<HEIGHT:
        if board.pipeline_active:
            board.pipeline_action(x,y)
        elif click == 2:
            board.tiles[(x//SPACE_SIZE, y//SPACE_SIZE)].flag()
        elif click == 1:
            board.tiles[(x//SPACE_SIZE, y//SPACE_SIZE)].reveal()
            if board.tiles[(x//SPACE_SIZE, y//SPACE_SIZE)].ismine:
                board.game_over_text = canvas.create_text(
                    canvas.winfo_width()/2,  
                    canvas.winfo_height()/2, 
                    font=('consolas', 70),  
                    text="GAME OVER",  
                    fill="red", tag="gameover"
                ) 
                #board.kill_tile = (x//SPACE_SIZE, y//SPACE_SIZE)

        if board.victory_check():
            canvas.create_text(
                    canvas.winfo_width()/2,  
                    canvas.winfo_height()/2, 
                    font=('consolas', 70),  
                    text="!YOU WIN!",  
                    fill="green", tag="gameover"
                ) 
            
    elif (x//SPACE_SIZE == board.tsunami_location[0]//SPACE_SIZE) \
        and (y//SPACE_SIZE == board.tsunami_location[1]//SPACE_SIZE):
        board.tsunami()

    elif (x//SPACE_SIZE == board.pipeline_location[0]//SPACE_SIZE) \
        and (y//SPACE_SIZE == board.pipeline_location[1]//SPACE_SIZE):
        board.pipeline_update()
    
    elif (x//SPACE_SIZE == board.nazare_location[0]//SPACE_SIZE) \
        and (y//SPACE_SIZE == board.nazare_location[1]//SPACE_SIZE):
        board.nazare()

    else:
        pass

  

# Giving title to the gaming window 
window = Tk() 
window.title("Beach Sweeper") 

# Display of Points Scored in Game 
# TODO: Fix score update, it's broken
score = IntVar()

label = Label(window,  
            text="Points:{}".format(score.get()),  
            font=('consolas', 20)) 
label.pack()  

canvas = Canvas(window, bg=BACKGROUND,  
                height=HEIGHT, width=WIDTH) 
canvas.pack() 
  
window.update() 

label = Label(window,  
            text="Points:{}".format(score.get()),  
            font=('consolas', 20)) 
label.pack()  
  
window_width = window.winfo_width() 
window_height = window.winfo_height() 
screen_width = window.winfo_screenwidth() 
screen_height = window.winfo_screenheight() 
  
x = int((screen_width/2) - (window_width/2)) 
y = int((screen_height/2) - (window_height/2)) 
  
window.geometry(f"{window_width}x{window_height}+{x}+{y}") 

# LOAD sprites
sprites = dict()
sprites['BLANK_TILE'] = PhotoImage(file="New_Piskel/sprite_0.png")
sprites['FLAG_TILE'] = PhotoImage(file="New_Piskel/sprite_1.png")
sprites['SAFE_TILE'] = PhotoImage(file="New_Piskel/sprite_3.png")
sprites['SHARK_TILE'] = PhotoImage(file="New_Piskel/sprite_5.png")
sprites['TSUNAMI_TILE'] = PhotoImage(file="New_Piskel/sprite_tsunami.png")
sprites['PIPELINE_TILE'] = PhotoImage(file="New_Piskel/sprite_pipeline.png")
sprites['USED_TILE'] = PhotoImage(file="New_Piskel/sprite_used_power.png")
sprites['SURFER_TILE'] = PhotoImage(file="New_Piskel/sprite_4.png")
sprites['UNDO_TILE'] = PhotoImage(file="New_Piskel/sprite_undo.png")
sprites['NAZARE_TILE'] = PhotoImage(file="New_Piskel/sprite_nazare.png")

  
window.bind('<Button>',  clicked) 
  
board = Board(WIDTH-100, HEIGHT, SPACE_SIZE, canvas, sprites) 
  
window.mainloop()