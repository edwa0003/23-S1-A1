from __future__ import annotations
from grid import Grid
from data_structures.queue_adt import CircularQueue
from action import PaintAction

class ReplayTracker:
    def __init__(self):
        """
        initializing objects to be used
        Args: None
        Raises: None
        Returns: nothing. But initializing objects.
        Complexity:
        - Always O(CircularQueue.__init__) because always initialize the same objects
        """
        self.replay_queue = CircularQueue(10000)

    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        """
        pass

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.
        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.

        Args: action which is a PaintAction object. is_undo which is boolean determining whether it's undo or not, the default value is false.
        Raises: None
        Returns: nothing. But adds action to self.replay_queue.
        Complexity:
        - Always O(CircularQueue.is_full+CircularQueue.append) because checking then append
        - qeue is full means can't append so invalid input
        """
        if not self.replay_queue.is_full(): #checking if the queue is full
            self.replay_queue.append((action,is_undo))

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        Args: grid. which is the grid you want to play next action on.
        Raises: None
        Returns: bool. True if there are no actions anymore. False if there are still actions.
        Complexity:
        - Worst: O(CircularQueue.is_empty+CircularQueue.serve+comp+CircularQueue.undo_apply) or
         O(CircularQueue.is_empty+CircularQueue.serve+comp+CircularQueue.redo_apply)
         - Best: O(1) straight away return True because there are no actions anymore
        """
        if not self.replay_queue.is_empty(): #checking if queue is empty, if empty then end and return true.
            last_action=self.replay_queue.serve()
            if last_action[1]==True: #deciding whether it's an undo or redo
                last_action[0].undo_apply(grid)
            else:
                last_action[0].redo_apply(grid)
            return False
        return True

if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

