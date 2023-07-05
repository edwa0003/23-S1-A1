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
    def __init__(self): #just an item with attributes
        """
        Initializing attributes
        Args: None
        Raises: None
        Returns: None
        Complexity:
        - Always 0(1) because initializing variables
        """
        self.layer_store = None #initializing. O(1)
        self.invert = False #initializing. O(1)

    def add(self, layer: Layer) -> bool:
        """
        Set the single layer.
        Args: layer which is a Layer object
        Raises: None
        Returns: bool. if the added layer is different from current layer returns true, if it's the same returns false
        Complexity:
        - Always 0(comp). only checking, no loop or recursion
        """
        if self.layer_store==layer: #checking if there any changes. O(comp).
            return False
        self.layer_store=layer #assigning the layer store to new layer. O(1)
        return True

    def erase(self, layer: Layer) -> bool:
        """
        Remove the single layer. Ignore what is currently selected.
        Args: layer which is a Layer object
        Raises: None
        Returns: bool. if self.layer_store is empty then nothing can be erased so returns False. if self.layer_store has something
        in it which means something can be erased, returns True.
        Complexity:
        - Always 0(comp). only checking no loop or recursion.
        """
        if self.layer_store == None: #checking if the layer is empty. O(1).
            return False
        self.layer_store=None #assigning variable. O(1).
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        getting current color of the layer store.
        Args:
        -start: starting color
        -timestamp: time
        -x: x coordinate
        -y: y coordinate
        Raises: None
        Returns: color which is a tuple containg 3 integers.
        Complexity:
        - Worst: 0(comp+apply+comp+apply)=O(comp+apply). Which means special is turned on.
        - Best: O(comp+apply). Which means special is turned off.
        """
        color= start
        if self.layer_store!=None:
            color = self.layer_store.apply(color, timestamp, x, y)
        if self.invert: #Invert the colour output.
            color=invert.apply(color, timestamp, x, y)
        return color

    def special(self):
        """
        Turning on or off invert.
        Args: None
        Raises: None
        Returns: None. But, makes the opposite of the current state of self.invert.
        Complexity:
        - Always 0(1). Only assigning variable.
        """
        self.invert= not self.invert

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    def __init__(self):
        """
        Initializing objects and attributes to be used
        Args: None
        Raises: None
        Returns: None
        Complexity:
        - Always 0(CircularQueue.__init__) because only initializing variables and initializing queue with fixed capacity
        """
        layer_store=CircularQueue(100*20)
        self.layer_store = layer_store
        self.color = None
        self.reverse = False

    def add(self, layer: Layer) -> bool:
        """
        Add a new layer to be added last.
        Args: layer which is a Layer object
        Raises: from CircularQueue will raise is full if the queue is full
        Returns: bool. True if the added layer is added succesfully. if fails then raise exception queue is full.
        Complexity:
        - Always O(CircularQueue.append) only adding to queue.
        """
        self.layer_store.append(layer)
        return True

    def erase(self, layer: Layer) -> bool:
        """
        Remove the first layer that was added. Ignore what is currently selected.
        Args: layer which is a Layer object
        Raises: from CircularQueue will raise queue is empty if queue is empty
        Returns: True if layer erased succesfully. False if layer store is empty
        - Always O(CircularQueue.serve) only serving queue.
        """
        self.layer_store.serve()
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        getting current color of the layer store.
        Args:
        -start: starting color
        -timestamp: time
        -x: x coordinate
        -y: y coordinate
        Raises: None
        Returns: color which is a tuple containg 3 integers.
        Complexity:
        - N is len(self.layer_store)
        - Worst: O(CircularQueue.__init__+N*CircularQueue.is_empty*comp*CircularQueue.serve*apply*CircularQueue.append + N*CircularQueue.is_empty*comp*CircularQueue.serve*apply*CircularQueue.append)=
        O(CircularQueue.__init__+N*CircularQueue.is_empty*comp*CircularQueue.serve*apply*CircularQueue.append). this happens when there are a lot of elements in self.layer_store
        - Best: O(CircularQueue.__init__+1*CircularQueue.is_empty*comp*CircularQueue.serve*apply*CircularQueue.append + 1*CircularQueue.is_empty*comp*CircularQueue.serve*apply*CircularQueue.append)=
        O(1*CircularQueue.is_empty*comp*CircularQueue.serve*apply*CircularQueue.append). this happens when there is only 1 element in self.layer_store
        """
        color=start
        temp_queue = CircularQueue(len(self.layer_store)) #creating temporary queue
        while self.layer_store.is_empty() == False:  # serving it and applying color one by one, this loop empties the self.layer_store
            layer = self.layer_store.serve() #complexity of this loop is O(N*CircularQueue.serve). N is how many layers are in self.layer_store.
            color = layer.apply(color, timestamp, x, y)
            temp_queue.append(layer) #adding color to temp_queue
        while temp_queue.is_empty() == False: #complexity of this loop is O(N*CircularQueue.serve). N is how many layers are in temp_queue which is the same amount as how many layers are in self.layer_store.
            layer = temp_queue.serve()
            self.layer_store.append(layer) # storing all the colors back into self.layer_store
        return color

    def special(self):
        """
        Reverse the order of current layers (first becomes last, etc.)
        Args: None
        Raises: None
        Returns: nothing. But reverses the order of the layers
        Complexity:
        - N being how many layers are stored in self.layer_store.
        - Worst: O(ArrayStack.__init__+N*CircularQueue.is_empty*comp*CircularQueue.serve*ArrayStack.push+N*ArrayStack.is_empty*comp*ArrayStack.pop*CircularQueue.append)
        this happens when there are many elements in layer store.
        - Best: O(ArrayStack.__init__+CircularQueue.is_empty*comp*CircularQueue.serve*ArrayStack.push+ArrayStack.is_empty*comp*ArrayStack.pop*CircularQueue.append).
        Meaning only 1 layer in self.layer_store.
        """
        temp_stack = ArrayStack(len(self.layer_store)) #creating a temporary stack. reverse queue using stack.
        while self.layer_store.is_empty() == False: #serving until queue is empty
            layer = self.layer_store.serve() #complexity of this loop is O(N*CircularQueue.serve). N is how many layers are in self.layer_store.
            temp_stack.push(layer)
        while temp_stack.is_empty() == False: #complexity of this loop is O(N*CircularQueue.serve). N is how many layers are in temp_stack which is the same amount as how many layers are in self.layer_store.
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
    def __init__(self):
        """
        Initializing object to be used
        Args: None
        Raises: None
        Returns: None
        Complexity:
        - Always 0(1) because initializing set with fixed size
        """
        self.layer_store=BSet()

    def add(self, layer: Layer) -> bool:
        """
        Ensure this layer type is applied.
        Args: layer which is a Layer object
        Raises: none
        Returns: bool. if the added layer is added succesfully. if fails then raise exception queue is full.
        Complexity:
        - Always O(BSet.__contains__+comp+BSet.add).
        """
        if layer.index+1 not in self.layer_store:
            self.layer_store.add(layer.index+1)
            return True
        return False

    def erase(self, layer: Layer) -> bool:
        """
        Ensure this layer type is applied.
        Args: layer which is a Layer object
        Raises: none
        Returns: bool. True if the added layer is erased succesfully. False if layer not in layer store.
        Complexity:
        - Always O( BSet.__contains__+BSet.remove ).
        """
        if layer.index in self.layer_store:
            self.layer_store.remove(layer.index+1)
            return True
        return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Ensure this layer type is applied.
        Args: layer which is a Layer object
        Raises: none
        Returns: color which is a tuple containg 3 integers.
        Complexity:
        -N is how many layer in layer store.
        - Worst: O( N*__contains__*apply ). This happens when there are a lot of elements in self.layer_store.
        - Best: O(__contains__*apply). This happens when there is only 1 element in self.layer_store.
        """
        color=start
        for item in range(1, self.layer_store.elems.bit_length() + 1):
            if item in self.layer_store:
                color = get_layers()[item-1].apply(color, timestamp,x,y)
        return color

    def special(self):
        """
        Ensure this layer type is applied.
        Args: layer which is a Layer object
        Raises: none
        Returns: bool. if the added layer is added succesfully. if fails then raise exception queue is full.
        Complexity:
        - N is how many layer in layer store.
        - Worst: O(ArraySortedList.__init__+BSet.is_empty+comp*sorted_layer.add+BSet.remove). This happens when there are a lot of element in self.layer_store.
        - Best: The same because the amount of layer in get_layers is the same
        """
        sorted_layer=ArraySortedList(len(self.layer_store))
        if not self.layer_store.is_empty():
            for layer in get_layers():
                if layer!=None and layer.index+1 in self.layer_store:
                    layer_list_item=ListItem(layer,layer.name) #making list item with value layer and key layer.name. O(1).
                    sorted_layer.add(layer_list_item) #adding to sorted list so it is automatically sorted. O(sorted_layer.add(layer_list_item))
            median_index=int( (len(sorted_layer)/2)-0.5)
            self.layer_store.remove(sorted_layer[median_index].value.index + 1)







