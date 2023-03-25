from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer,get_layers
from layers import invert
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from data_structures.bset import BSet
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
    def __init__(self): #just a variable, coba bikin attribute slef oclor
        self.layer_store = None
        self.invert = False

    def add(self, layer: Layer) -> bool:
        if self.layer_store==layer:
            return False
        self.layer_store=layer
        return True

    def erase(self, layer: Layer) -> bool:
        if self.layer_store == None:
            return False
        self.layer_store=None
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]: #returns the color at that time and coordiante, need to connect this to grid
        color= start #disini pakai self.color
        #print('self layer store is bool',isinstance(self.layer_store,bool))
        if self.layer_store!=None:
            color = self.layer_store.apply(color, timestamp, x, y)
        if self.invert:
            color=invert.apply(color, timestamp, x, y)
        return color

    def special(self):
        self.invert= not self.invert

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
        self.layer_store=BSet()

    def add(self, layer: Layer) -> bool: #
        if layer.index+1 not in self.layer_store:
            self.layer_store.add(layer.index+1)
            return True
        return False

    def erase(self, layer: Layer) -> bool:
        if layer.index in self.layer_store:
            self.layer_store.remove(layer.index+1)
            return True
        return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        color=start
        for item in range(1, self.layer_store.elems.bit_length() + 1):
            if item in self.layer_store:
                color = get_layers()[item-1].apply(color, timestamp,x,y)
        return color

    def special(self):
        sorted_layer=ArraySortedList(len(self.layer_store))
        if not self.layer_store.is_empty():
            for layer in get_layers():
                if layer!=None and layer.index+1 in self.layer_store:
                    layer_list_item=ListItem(layer,layer.name)
                    sorted_layer.add(layer_list_item)
            median_index=int( (len(sorted_layer)/2)-0.5)
            self.layer_store.remove(sorted_layer[median_index].value.index + 1)







