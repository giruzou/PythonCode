from itertools import product
import numpy as np
import z3
from z3solver import Z3Solver
from kivy.app import App
from kivy.uix.button import Label, Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout


class MainGrid(GridLayout):

    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        self.shift_down = False


class SubGrid(FocusBehavior, GridLayout):

    def __init__(self, **kwargs):
        super(SubGrid, self).__init__(**kwargs)
        self.shift_down = False

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """Based on FocusBehavior that provides automatic keyboard
        access, key presses will be used to select children.
        """
        if 'shift' in keycode[1]:
            self.shift_down = True

    def keyboard_on_key_up(self, window, keycode):
        """Based on FocusBehavior that provides automatic keyboard
        access, key release will be used to select children.
        """
        if 'shift' in keycode[1]:
            self.shift_down = False

    def add_widget(self, widget):
        """ Override the adding of widgets so we can bind and catch their
        *on_touch_down* events. """
        widget.bind(on_touch_down=self.button_touch_down)
        return super(SubGrid, self).add_widget(widget)

    def button_touch_down(self, button, touch):
        """ Use collision detection to select buttons when the touch occurs
        within their area. """
        if button.collide_point(*touch.pos):
            self.update_button_text(button)

    def update_button_text(self, button):
        if self.shift_down:
            button.countdown()
        else:
            button.countup()


class Cell(Button):
    DIC = {0: "*", 1: "1", 2: "2", 3: "3", 4: "4",
           5: "5", 6: "6", 7: "7", 8: "8", 9: "9"}

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.counter = 0
        self.text = Cell.DIC[0]

    def countup(self):
        self.counter = (self.counter+1) % 10
        self.text = Cell.DIC[self.counter]

    def countdown(self):
        self.counter = (self.counter-1) % 10
        self.text = Cell.DIC[self.counter]


class SudokuApp(App):

    def on_start(self):
        main_grid = self.root.ids.main_grid
        for (k, l) in product(range(3), repeat=2):
            sub_grid = SubGrid(id="block_{}_{}".format(str(k), str(l)))
            for (i, j) in product(range(3), repeat=2):
                sub_grid.add_widget(
                    Cell(id="cell_{}_{}".format(str(3*k+i), str(3*l+j))))
            main_grid.add_widget(sub_grid)

    def _parse_idx(self, widget):
        i, j = widget.id.split("_")[1:]
        return int(i), int(j)

    def solve(self):
        grid = lambda i, j: z3.Int("grid[%d,%d]" % (i, j))
        print("Start to solve")
        sub_grids = self.root.ids.main_grid.children
        problem = [[0]*9 for _ in range(9)]
        for sub_grid in sub_grids:
            block = sub_grid.children
            for cell in block:
                i, j = self._parse_idx(cell)
                if cell.text.isnumeric():
                    problem[i][j] = int(cell.text)
                else:
                    problem[i][j] = 0
        solver = Z3Solver(problem)
        result = solver.solve()
        if result == z3.sat:
            model = solver.model()
            for sub_grid in sub_grids:
                block = sub_grid.children
                for cell in block:
                    i, j = self._parse_idx(cell)
                    cell.text = str(model[grid(i, j)])
        else:
            print(result)

    def reset(self):
        print("Reset")
        sub_grids = self.root.ids.main_grid.children
        for sub_grid in sub_grids:
            block = sub_grid.children
            for cell in block:
                cell.text = '*'


def main():
    SudokuApp().run()


if __name__ == '__main__':
    main()
