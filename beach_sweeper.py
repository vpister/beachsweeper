from tkinter import *
# from PIL import Image, ImageTK
import random 

# Initialising screen params
SPACE_SIZE = 32
WIDTH = 25*32 + 100
temp_width = WIDTH - 100
HEIGHT = 25*32
BACKGROUND = "#CAF2FF"
FONTSIZE= 14

# power locations
tsunami_location = (temp_width + SPACE_SIZE*1.5, 0 + SPACE_SIZE*1.5)
pipeline_location = (temp_width + SPACE_SIZE*1.5, SPACE_SIZE*2 + SPACE_SIZE*1.5)

# variable from level to level
PCT_MINES = 0.25
PCT_SURF = 0.45

class Board: 
  
    def __init__(self): 
        self.tiles = dict()
        self.tsunami_left = 1
        self.pipeline_left = 1
        self.pipeline_active = False

        # TODO: get the resize image working eventually
        # BLANK_TILE = Image.open("New_Piskel/sprite_0.png")
        # BLANK_TILE = BLANK_TILE.resize((SPACE_SIZE,SPACE_SIZE))
        # BLANK_TILE = ImageTK.PhotoImage(BLANK_TILE)
        
        # place power up tiles
        square = canvas.create_image( 
            tsunami_location,
            image=TSUNAMI_TILE
        )

        square = canvas.create_image( 
            pipeline_location,
            image=PIPELINE_TILE
        )

        # inialize all tiles and randomly place mines
        for i in range(0, int(temp_width/SPACE_SIZE)): 
            for j in range(0, int(HEIGHT/SPACE_SIZE)): 
                
                square = canvas.create_image( 
                    (i * SPACE_SIZE+ SPACE_SIZE/2, j * SPACE_SIZE + SPACE_SIZE/2) ,
                    image=BLANK_TILE)
                
                t = Tile(i, j, square)
                t.ismine = random.random() < PCT_MINES

                self.tiles[(i, j)] = t 

        # fill in tile value
        for k, v in self.tiles.items():
            num_mines = sum([int(self.tiles[c].ismine) for c in self.get_adj_coords(*k)])
            if num_mines == 0:
                if random.random() < PCT_SURF:
                    v.surfer = True
            v.value = num_mines

    def get_adj_coords(self, x,y):
        """
        Gets adjacent tiles which are within the bounds of the board and 
        have not yet been revealed.
        """
        all_cs = (x+1, y), (x+1, y+1), (x+1, y-1), (x,y+1), (x,y-1), (x-1, y+1), (x-1,y), (x-1,y-1)
        ret_cs = []
        for c in all_cs:
            if c[0] >= 0 and c[0] < temp_width//SPACE_SIZE and c[1] >= 0 and c[1] < HEIGHT//SPACE_SIZE:
                if not self.tiles[c].revealed:
                    ret_cs.append(c)
        return ret_cs
    
    def tsunami(self):
        """
        Reveals all tiles with 0 value and surrounding tiles.
        """
        if self.tsunami_left > 0:
            for _,v in self.tiles.items():
                if v.value == 0 and not v.ismine:
                    v.reveal()

            self.tsunami_left -= 1

        if self.tsunami_left <= 0:
            square = canvas.create_image( 
                tsunami_location,
                image=USED_TILE
            )
            
    
    def pipeline_update(self):
        """
        Updates power-ups remaining and activates pipeline state.
        """
        if self.pipeline_left <= 1:
            square = canvas.create_image( 
                pipeline_location,
                image=USED_TILE
            )
            
        if self.pipeline_left > 0:
            self.pipeline_left -= 1
            self.pipeline_active = True

    def pipeline_action(self,x,y):
        """
        Reveals selected tile and available adjacent tiles.
        Does not reveal mines.
        """
        self.pipeline_active = False
        i, j = (x//SPACE_SIZE, y//SPACE_SIZE)
        for c in self.get_adj_coords(i,j) + [(i,j)]:
            if not board.tiles[c].ismine:
                board.tiles[c].reveal()
    
    def victory_check(self):
        """
        Returns true when all non-mine tiles have been revealed.
        """
        for _, v in self.tiles.items():
            if not v.ismine and not v.revealed:
                return False
            
        return True


class Tile: 
  
    def __init__(self, x, y, square): 
  
        self.coordinates = [x, y] 
        self.square = square
        self.revealed = False
        self.value = None
        self.ismine = None
        self.flagged = False
        self.surfer = False

    def reveal(self):
        """
        Reveals tile object.
        If object is a mine, ends game.
        If object is a non-zero value, reveal value.
        If object value is zero, expand out until non-zero values.
        """

        if self.ismine:
            square = canvas.create_image( 
                (self.coordinates[0] * SPACE_SIZE+ SPACE_SIZE/2, self.coordinates[1] * SPACE_SIZE + SPACE_SIZE/2) ,
                image=SHARK_TILE
            )
            return None
        

        self.revealed = True

        canvas.delete(self.square)

        square = canvas.create_image( 
            (self.coordinates[0] * SPACE_SIZE+ SPACE_SIZE/2, self.coordinates[1] * SPACE_SIZE + SPACE_SIZE/2) ,
            image=SAFE_TILE
        )
        
        self.square = square

        if self.value == 0:
            if self.surfer:
                score.set(score.get()+1)

                self.surfer = False
                square = canvas.create_image( 
                    (self.coordinates[0] * SPACE_SIZE+ SPACE_SIZE/2, self.coordinates[1] * SPACE_SIZE + SPACE_SIZE/2) ,
                    image=SURFER_TILE
                )
            for c in board.get_adj_coords(*self.coordinates):
                board.tiles[c].reveal() 

        else:
            canvas.create_text(
                self.coordinates[0] * SPACE_SIZE + (SPACE_SIZE/2),  
                self.coordinates[1] * SPACE_SIZE + (SPACE_SIZE/2), 
                font=('consolas', FONTSIZE),  
                text=f"{self.value}",  
                fill="black", tag="value"
                ) 
            
    def flag(self):
        """
        Flags or unflags object.
        """
        canvas.delete(self.square)
        if self.flagged:
            square = canvas.create_image( 
                (self.coordinates[0] * SPACE_SIZE+ SPACE_SIZE/2, self.coordinates[1] * SPACE_SIZE + SPACE_SIZE/2) ,
                image=BLANK_TILE
            )

        else:
            square = canvas.create_image( 
                (self.coordinates[0] * SPACE_SIZE+ SPACE_SIZE/2, self.coordinates[1] * SPACE_SIZE + SPACE_SIZE/2) ,
                image=FLAG_TILE
            )
            
        self.square= square
        self.flagged = not self.flagged


def clicked(event): 

    """
    Identify clicked tile and take appropriate action.
    Handles victory and game over state.
    """
  
    x, y, click  = event.x, event.y, event.num
    #print(f"CLICK: {(x,y)}")


    if 0 < x < temp_width and 0<y<HEIGHT:
        if board.pipeline_active:
            board.pipeline_action(x,y)
        elif click == 2:
            board.tiles[(x//SPACE_SIZE, y//SPACE_SIZE)].flag()
        elif click == 1:
            board.tiles[(x//SPACE_SIZE, y//SPACE_SIZE)].reveal()
            if board.tiles[(x//SPACE_SIZE, y//SPACE_SIZE)].ismine:
                canvas.create_text(
                    canvas.winfo_width()/2,  
                    canvas.winfo_height()/2, 
                    font=('consolas', 70),  
                    text="GAME OVER",  
                    fill="red", tag="gameover"
                ) 

        if board.victory_check():
            canvas.create_text(
                    canvas.winfo_width()/2,  
                    canvas.winfo_height()/2, 
                    font=('consolas', 70),  
                    text="!YOU WIN!",  
                    fill="green", tag="gameover"
                ) 
    elif (x//SPACE_SIZE == tsunami_location[0]//SPACE_SIZE) and (y//SPACE_SIZE == tsunami_location[1]//SPACE_SIZE):
        board.tsunami()
    elif (x//SPACE_SIZE == pipeline_location[0]//SPACE_SIZE) and (y//SPACE_SIZE == pipeline_location[1]//SPACE_SIZE):
        board.pipeline_update()
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
  
window_width = window.winfo_width() 
window_height = window.winfo_height() 
screen_width = window.winfo_screenwidth() 
screen_height = window.winfo_screenheight() 
  
x = int((screen_width/2) - (window_width/2)) 
y = int((screen_height/2) - (window_height/2)) 
  
window.geometry(f"{window_width}x{window_height}+{x}+{y}") 

# LOAD sprites
BLANK_TILE = PhotoImage(file="New_Piskel/sprite_0.png")
FLAG_TILE = PhotoImage(file="New_Piskel/sprite_1.png")
SAFE_TILE = PhotoImage(file="New_Piskel/sprite_3.png")
SHARK_TILE = PhotoImage(file="New_Piskel/sprite_5.png")
TSUNAMI_TILE = PhotoImage(file="New_Piskel/sprite_tsunami.png")
PIPELINE_TILE = PhotoImage(file="New_Piskel/sprite_pipeline.png")
USED_TILE = PhotoImage(file="New_Piskel/sprite_used_power.png")
SURFER_TILE = PhotoImage(file="New_Piskel/sprite_4.png")

  
window.bind('<Button>',  clicked) 
  
board = Board() 
  
window.mainloop()