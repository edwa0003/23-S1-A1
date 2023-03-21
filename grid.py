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
        """
        self.brush_size=self.DEFAULT_BRUSH_SIZE
        self.draw_style=draw_style
        self.x=x
        self.y=y
        self.grid= self.make_grid(draw_style,x,y)

    def __getitem__(self, key): #this for [x][y]
        return self.grid[key]

    def make_grid(self,draw_style,x,y):
        #make an empty list with len x*y, then put y amount of empty list inside.
        #then inside each one of those empty list, then put empty stacks inside each.
        #use referential array
        vert_dim=x
        hor_dim=y
        grid = ArrayR(hor_dim*vert_dim)
        if draw_style=='SET':
            layer_store_type=SetLayerStore()
        elif draw_style=='ADD':
            layer_store_type=AdditiveLayerStore()
        elif draw_style=='SEQUENCE':
            layer_store_type=SequenceLayerStore()
        else:
            raise Exception('wrong draw style')
        for vert_in in range(vert_dim):
            row=ArrayR(hor_dim)
            grid[vert_in]=row
            for hor_in in range(hor_dim):
                row[hor_in]=layer_store_type
            hor_in=0
        return grid

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size>self.MAX_BRUSH:
            self.brush_size=self.MAX_BRUSH
        self.brush_size=self.brush_size+1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size<self.MIN_BRUSH:
            self.brush_size=self.MIN_BRUSH
        self.brush_size=self.brush_size-1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        raise NotImplementedError()

grid =Grid('SET',5,4)
print(grid)