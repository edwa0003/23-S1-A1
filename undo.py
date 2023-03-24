from __future__ import annotations
from grid import Grid
from data_structures.stack_adt import ArrayStack
from action import PaintAction

class UndoTracker:

    def __init__(self):
        self.tracker=ArrayStack(10000)
        self.undo_tracker=ArrayStack(10000)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        if self.tracker.is_full()==False:
            self.tracker.push(action)
            self.undo_tracker.clear()

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        if self.tracker.is_empty():
            return None
        last_action = self.tracker.pop()
        self.undo_tracker.push(last_action)
        last_action.undo_apply(grid) #undo apply di paint action di file action.py
        return last_action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if self.undo_tracker.is_empty():
            return None
        last_action = self.undo_tracker.pop()
        self.tracker.push(last_action)
        last_action.redo_apply(grid)
        return last_action
