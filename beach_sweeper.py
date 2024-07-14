from tkinter import *
from Board import Board

# Initialising screen params
SPACE_SIZE = 32
BACKGROUND = "#CAF2FF"


#global score 
score = 0

# LEVEL_PARAMS = {
#     '1' : (10*SPACE_SIZE, 10*SPACE_SIZE+100, pct_mines=0.1),

# }

# LOAD sprites
def get_sprites():
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
    return sprites


def generate_level(height, width, pct_mines = 0.2, pct_surf = 0.45):

    def exit_level(event):
        """
        Terminates window in either game over state.
        """
        # TODO: return to menu
        if board.victory_check():
            window.destroy()
        if board.game_over_text:
            window.destroy()

    # Giving title to the gaming window 
    window = Tk() 
    window.title("Beach Sweeper") 

    # Display of Points Scored in Game 
    # TODO: Fix score update, it's broken
    

    label = Label(window,  
                text="Points:{}".format(score),  
                font=('consolas', 20)) 
    label.pack()  

    canvas = Canvas(window, bg=BACKGROUND,  
                    height=height, width=width) 
    canvas.pack() 
    
    window.update() 

    label = Label(window,  
                text="Points:{}".format(score),  
                font=('consolas', 20)) 
    label.pack()  
    
    window_width = window.winfo_width() 
    window_height = window.winfo_height() 
    screen_width = window.winfo_screenwidth() 
    screen_height = window.winfo_screenheight() 
    
    x = int((screen_width/2) - (window_width/2)) 
    y = int((screen_height/2) - (window_height/2)) 
    
    window.geometry(f"{window_width}x{window_height}+{x}+{y}") 

    sprites = get_sprites()
    board = Board(
        width-100, height, SPACE_SIZE, 
        canvas, sprites,
        pct_mines=pct_mines, pct_surf=pct_surf
    ) 
    window.bind('<Button>',  board.clicked)
    window.bind("<space>", exit_level)
    
    window.mainloop()


def generate_lvl1():
    generate_level(10*SPACE_SIZE, 10*SPACE_SIZE+100, pct_mines=0.1)

def generate_lvl2():
    generate_level(15*SPACE_SIZE, 15*SPACE_SIZE+100)

generate_lvl1()
generate_lvl2()


# # Create the main window
# root = Tk()
# root.title("Main Menu")

# # Create a frame for the main menu
# main_menu = Frame(root)
# main_menu.pack(pady=20)

# # Add a title label
# title_label = Label(main_menu, text="Beachsweeper", font=("Consolas", 24))
# title_label.pack(pady=10)

# # Add a button to go to the shop
# # shop_button = tk.Button(main_menu, text="Shop", command=go_to_shop, width=20, height=2)
# # shop_button.pack(pady=10)

# # Add buttons to start levels
# level1_button = Button(main_menu, text="Level 1", command=generate_lvl1, width=20, height=2)
# level1_button.pack(pady=10)

# level2_button = Button(main_menu, text="Level 2", command=generate_lvl2, width=20, height=2)
# level2_button.pack(pady=10)

# # Run the application
# root.mainloop()
