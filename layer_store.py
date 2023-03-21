from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from layers import invert
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:#look at color apply. Does x and y matter ? read test set layer and main to find out
        """
        Returns the colour this square should show, given the current layers.
        """
        #returns the color which is a tuple containing 3 values at coordinate x and y
        #start is the starting color which is at the bottom of the stack
        #timestamp,if for example it is rainbow need timestamp at time ... what is the color of that square
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """
    def __init__(self): #just a variable
        self.layer_store = None
        self.invert = False

    def add(self, layer: Layer) -> bool:
        if self.layer_store==layer:
            return False
        self.layer_store = layer
        return True

    def erase(self, layer: Layer) -> bool:
        if self.layer_store == None:
            return False
        self.layer=None
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]: #returns the color at that time and coordiante, need to connect this to grid
        color= start
        if self.layer_store != None:
            color = self.layer_store.apply(color, timestamp, x, y)
        if self.invert:
            color=invert.apply(color, timestamp, x, y)
        return color

    def special(self):
        if self.invert:
            self.invert=False
        self.invert=True

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    #use queuqe because erase
    def __init__(self):
        layer_store=CircularQueue(100*20)
        self.layer_store = layer_store
        self.color = None
        self.reverse = False

    def add(self, layer: Layer) -> bool:
        self.layer_store.append(layer)
        return True

    def erase(self, layer: Layer) -> bool:
        self.layer_store.serve()
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        color=start
        temp_queue = CircularQueue(len(self.layer_store))
        while self.layer_store.is_empty() == False:  # serving it and applying color one by one, this loop empties the self.layer_store
            layer = self.layer_store.serve()
            color = layer.apply(color, timestamp, x, y)
            temp_queue.append(layer)
        while temp_queue.is_empty() == False:  # storing all the colors back into self.layer_store
            layer = temp_queue.serve()
            self.layer_store.append(layer)
        return color

    def special(self):
        temp_stack = ArrayStack(len(self.layer_store))
        while self.layer_store.is_empty() == False:
            layer = self.layer_store.serve()
            temp_stack.push(layer)
        while temp_stack.is_empty() == False:
            layer = temp_stack.pop()
            self.layer_store.append(layer)

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """
    #for example add black then add blue, because the index of blue is higer than black the square will become blue.
    #this has 9 layers that is all the colors and effects on layers.py. the index is from top is 1 bottom is 9.
    def __init__(self):
        self.layer_store=ArraySortedList(9)
        self.median=False

    def add(self, layer: Layer) -> bool:
        layer = ListItem(layer, layer.index)
        if self.layer_store.is_full()==False:
            if layer not in self.layer_store:
                self.layer_store.add(layer)
                return True
        return False

    def erase(self, layer: Layer) -> bool:
        layer =ListItem(layer,layer.index)
        if self.layer_store.is_empty()==False:
            if layer in self.layer_store:
                self.layer_store.remove()
                return True
        return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        color=start
        if self.layer_store.is_empty()==False:
            for i in range(len(self.layer_store)):
                layer = self.layer_store[i].value
                color = layer.apply(start,timestamp,x,y)
        return color

    def special(self):
        lex_order_layer= ArraySortedList(len(self.layer_store))
        for i in range(len(self.layer_store)):
            greater=0
            for j in range(len(self.layer_store)):
                if self.layer_store[i].value.name>self.layer_store[j].value.name:
                    greater=greater+1
            item=ListItem(self.layer_store[i],greater)
            lex_order_layer.add(item)
        median_index=len(self.layer_store)//2
        self.layer_store.delete_at_index(median_index)





