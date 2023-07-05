from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import SetLayerStore,AdditiveLayerStore,SequenceLayerStore
class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.
        Should also intialise the brush size to the DEFAULT provided as a class variable.

        Args: draw_style, x, y
        Raises: None
        Returns: None, just initializing variables
        Complexity:
        - Worst case: O(x*y), where x and y are the dimensions of the grid
        - Best case: O(1*1), when x=1 and y=1. Having x=0 or y=0 means no grid will be made.
        """
        self.brush_size=self.DEFAULT_BRUSH_SIZE
        self.draw_style=draw_style
        self.x=x
        self.y=y
        self.grid= self.make_grid(draw_style,x,y)

    def __getitem__(self, key): #this for [x][y]
        """ Returns the object in position index.
        Argument: key which is the index of object
        Raises: out of index
        Returns: object at that index
        complexity: O(1)
        """
        return self.grid[key]

    def make_grid(self,draw_style,x,y): #complexity O(N^2) since this is a for loop inside a for loop
        vert_dim=x #do in reverse because list indexing uses [y][x] while the question wants [x][y]
        hor_dim=y #so x become vertical dimension, y becomes horizontal dimension
        grid = ArrayR(vert_dim) #creating a referential array according to how many rows thereare
        for vert_in in range(vert_dim):
            row=ArrayR(hor_dim) #creating the rows
            grid[vert_in]=row #adding the rows to grid
            for hor_in in range(hor_dim): #adding the layer stores
                if draw_style == 'SET': #determining the layer stores type
                    layer_store_type = SetLayerStore
                elif draw_style == 'ADD':
                    layer_store_type = AdditiveLayerStore
                elif draw_style == 'SEQUENCE':
                    layer_store_type = SequenceLayerStore
                else:
                    raise Exception('wrong draw style')
                grid[vert_in][hor_in]=layer_store_type()#adding layer stores
        return grid

    def increase_brush_size(self): #complexity O(1) only adding 1
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.

        Args: None
        Raises: None
        Returns: None, but changes self.brush size
        Complexity:
        - always O(1), only adding self.brush size by 1
        """
        if self.brush_size<Grid.MAX_BRUSH: #make sure that the brush size always smaller than
            self.brush_size=self.brush_size+1

    def decrease_brush_size(self): #complexity O(1) only decreasing 1
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.

        Args: None
        Raises: None
        Returns: None, but changes self.brush size
        Complexity:
        - always O(1), only decreasing self.brush size by 1
        """
        if self.brush_size>Grid.MIN_BRUSH:
            self.brush_size=self.brush_size-1

    def special(self): #complexity O(N^2) because for loop inside for loop
        """
        Activate the special affect on all grid squares.
        Args: None
        Raises: None
        Returns: None, but does special method on every layer store
        Complexity:
        - Worst: O(X*Y), needs to loop through all the layer stores
        - Best: 0(1), when x=1 and y=1 so only loop through one layer store
        """
        for x in range(self.x): #looping through all the squares and calling the method special in each square
            for y in range(self.y):
                self.grid[x][y].special()
