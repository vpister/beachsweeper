class Tile(): 
  
    def __init__(self, x, y, square, env_factors): 
  
        self.coordinates = [x, y] 
        self.square = square
        self.FONTSIZE = 15
        self.canvas, self.space_size, self.sprites, self.board = env_factors 
        
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
            self.canvas.create_image( 
                (self.coordinates[0] * self.space_size+ self.space_size/2, 
                 self.coordinates[1] * self.space_size + self.space_size/2) ,
                image=self.sprites['SHARK_TILE']
            )
            return None
        

        self.revealed = True

        self.canvas.delete(self.square)

        square = self.canvas.create_image( 
            (self.coordinates[0] * self.space_size+ self.space_size/2, 
             self.coordinates[1] * self.space_size + self.space_size/2) ,
            image=self.sprites['SAFE_TILE']
        )
        
        self.square = square

        if self.value == 0:
            if self.surfer:
                #score.set(score.get()+1)

                self.surfer = False
                square = self.canvas.create_image( 
                    (self.coordinates[0] * self.space_size+ self.space_size/2, 
                     self.coordinates[1] * self.space_size + self.space_size/2) ,
                    image=self.sprites['SURFER_TILE']
                )
            for c in self.board.get_adj_coords(*self.coordinates):
                self.board.tiles[c].reveal() 

        else:
            self.canvas.create_text(
                self.coordinates[0] * self.space_size + (self.space_size/2),  
                self.coordinates[1] * self.space_size + (self.space_size/2), 
                font=('consolas', self.FONTSIZE),  
                text=f"{self.value}",  
                fill="black", tag="value"
                ) 
            
    def flag(self):
        """
        Flags or unflags object.
        """
        self.canvas.delete(self.square)
        if self.flagged:
            square = self.canvas.create_image( 
                (self.coordinates[0] * self.space_size+ self.space_size/2, 
                 self.coordinates[1] * self.space_size + self.space_size/2) ,
                image=self.sprites['BLANK_TILE']
            )

        else:
            square = self.canvas.create_image( 
                (self.coordinates[0] * self.space_size+ self.space_size/2, 
                 self.coordinates[1] * self.space_size + self.space_size/2) ,
                image=self.sprites['FLAG_TILE']
            )
            
        self.square= square
        self.flagged = not self.flagged