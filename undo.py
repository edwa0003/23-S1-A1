from __future__ import annotations
from grid import Grid
from data_structures.stack_adt import ArrayStack
from action import PaintAction

class UndoTracker:

    def __init__(self):
        self.undo_stack=ArrayStack(10000)
        self.redo_stack=ArrayStack(10000)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        if self.undo_stack.is_full()==False:
            self.undo_stack.push(action)
            self.redo_stack.clear() #because if the user do something, it will clear the redo stack

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        if self.undo_stack.is_empty():
            return None
        last_action = self.undo_stack.pop()
        self.redo_stack.push(last_action)
        last_action.undo_apply(grid) #undo apply di paint action di file action.py
        return last_action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if self.redo_stack.is_empty():
            return None
        last_action = self.redo_stack.pop()
        self.undo_stack.push(last_action)
        last_action.redo_apply(grid)
        return last_action
