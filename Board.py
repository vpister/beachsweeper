import random
from Tile import *

class Board: 
  
    def __init__(self, 
                 width, height, 
                 space_size, canvas, sprites,
                 pct_surf = 0.45, pct_mines=0.2,): 
        self.tiles = dict()

        self.pct_surf = pct_surf
        self.pct_mines = pct_mines

        self.width, self.height = width, height
        self.space_size = space_size
        self.canvas = canvas
        self.sprites=sprites

        self.tsunami_left = 1
        self.pipeline_left = 1
        self.undo_left = 5
        self.nazare_left = 1

        self.pipeline_active = False
        self.game_over_text = False

        # power locations
        x_increment = self.width + self.space_size*1.5
        y_increment = self.space_size*1.5
        self.tsunami_location = (x_increment, y_increment)
        self.pipeline_location = (x_increment, self.space_size*2 + y_increment)
        self.undo_location = (x_increment, self.space_size*6 + y_increment)
        self.nazare_location = (x_increment, self.space_size*4 + y_increment)

        # TODO: get the resize image working eventually
        # BLANK_TILE = Image.open("New_Piskel/sprite_0.png")
        # BLANK_TILE = BLANK_TILE.resize((SPACE_SIZE,SPACE_SIZE))
        # BLANK_TILE = ImageTK.PhotoImage(BLANK_TILE)
        
        # place power up tiles
        if self.tsunami_left >0:
            self.canvas.create_image( 
                self.tsunami_location,
                image=self.sprites['TSUNAMI_TILE']
            )

        if self.pipeline_left >0:
            self.canvas.create_image( 
                self.pipeline_location,
                image=self.sprites['PIPELINE_TILE']
            )

        if self.undo_left > 0:
            self.canvas.create_image( 
                self.undo_location,
                image=self.sprites['UNDO_TILE']
            )
        
        if self.nazare_left > 0:
            self.canvas.create_image( 
                self.nazare_location,
                image=self.sprites['NAZARE_TILE']
            )

        # inialize all tiles and randomly place mines
        for i in range(0, int(self.width/self.space_size)): 
            for j in range(0, int(height/self.space_size)): 
                
                square = self.canvas.create_image( 
                    (i * self.space_size+ self.space_size/2, j * self.space_size + self.space_size/2) ,
                    image=self.sprites['BLANK_TILE'])
                
                t = Tile(i, j, square, (self.canvas, self.space_size, self.sprites, self))
                t.ismine = random.random() < self.pct_mines

                self.tiles[(i, j)] = t 

        # fill in tile value
        for k, v in self.tiles.items():
            num_mines = sum([int(self.tiles[c].ismine) for c in self.get_adj_coords(*k)])
            if num_mines == 0:
                if random.random() < self.pct_surf:
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
            if c[0] >= 0 and c[0] < self.width//self.space_size and c[1] >= 0 and c[1] < self.height//self.space_size:
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
            self.canvas.create_image( 
                self.tsunami_location,
                image=self.sprites['USED_TILE']
            )
            
    
    def pipeline_update(self):
        """
        Updates power-ups remaining and activates pipeline state.
        """
        if self.pipeline_left <= 1:
            self.canvas.create_image( 
                self.pipeline_location,
                image=self.sprites['USED_TILE']
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
        i, j = (x//self.space_size, y//self.space_size)
        for c in self.get_adj_coords(i,j) + [(i,j)]:
            if not self.tiles[c].ismine:
                self.tiles[c].reveal()

    def undo_operation(self):
        if self.undo_left > 0:
            if self.game_over_text:
                self.canvas.delete(self.game_over_text)
                self.game_over_text = False
                self.undo_left -= 1
            
            if self.undo_left <= 0:
                self.canvas.create_image( 
                    self.undo_location,
                    image=self.sprites['USED_TILE']
                )

    def nazare(self):
        if self.nazare_left > 0:

            self.nazare_left -= 1
            
            if self.nazare_left <= 0:
                self.canvas.create_image( 
                    self.nazare_location,
                    image=self.sprites['USED_TILE']
                )

            w = random.randint(2,self.width//self.space_size - 2)
            h = random.randint(2, self.height//self.space_size - 2)

            while self.tiles[(w,h)].revealed:
                w = random.randint(2,self.width//self.space_size - 2)
                h = random.randint(2, self.height//self.space_size - 2)

            for c in self.get_adj_coords(w,h) \
                + self.get_adj_coords(w+1,h) + self.get_adj_coords(w-1,h) \
                + self.get_adj_coords(w,h + 1) + self.get_adj_coords(w,h - 1)\
                + [(w,h)]:

                if not self.tiles[c].ismine:
                    self.tiles[c].reveal()

    
    def victory_check(self):
        """
        Returns true when all non-mine tiles have been revealed.
        """
        for _, v in self.tiles.items():
            if not v.ismine and not v.revealed:
                return False
            
        return True