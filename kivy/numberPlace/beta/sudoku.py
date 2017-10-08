from itertools import product
import threading
import z3
from z3solver import Z3Solver
from kivy.app import App
from kivy.uix.button import Label, Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


class MainGrid(GridLayout):
    pass


class SubGrid(GridLayout):
    pass


class Cell(FocusBehavior, Button):
    DIC = {0: "*", 1: "1", 2: "2", 3: "3", 4: "4",
           5: "5", 6: "6", 7: "7", 8: "8", 9: "9"}

    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.counter = 0
        self.text = Cell.DIC[0]
        self.bind(on_touch_down=self.button_touch_down)
        self.skip = False
        self.shift_down=False

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

    def button_touch_down(self, button, touch):
        """ Use collision detection to select buttons when the touch occurs
        within their area. """
        if self.skip == False:
            if button.collide_point(*touch.pos):
                self.update_cell_value(button)
        else:
            return

    def update_cell_value(self, button):
        if self.shift_down:
            self.countdown()
        else:
            self.countup()

    def countup(self):
        self.counter = (self.counter+1) % 10
        self.text = Cell.DIC[self.counter]

    def countdown(self):
        self.counter = (self.counter-1) % 10
        self.text = Cell.DIC[self.counter]


class SudokuApp(App):

    def __init__(self, **kwargs):
        super(SudokuApp, self).__init__(**kwargs)
        self.progress_counter = 0

    def on_start(self):
        self.cells = dict()
        main_grid = self.root.ids.main_grid
        for (k, l) in product(range(3), repeat=2):
            sub_grid = SubGrid(id="block_{}_{}".format(k, l))
            for (i, j) in product(range(3), repeat=2):
                cell = Cell(id="cell_{}_{}".format(3*k+i, 3*l+j))
                self.cells[(3*k+i, 3*l+j)] = cell
                sub_grid.add_widget(cell)
            main_grid.add_widget(sub_grid)

    def progress(self, nap):
        prog = ['|', '/', '-', '\\']
        self.root.ids.message.text = "Start To Solve..." + \
            prog[self.progress_counter % len(prog)]
        self.progress_counter += 1

    def solve(self):
        self.solve_thread = threading.Thread(target=self._solve)
        self.solve_thread.start()
        Clock.schedule_interval(self.progress, 0.1)

    def _solve(self):
        self.root.ids.reset.disabled = True
        self.root.ids.solve.disabled = True
        for cell in self.cells.values():
            cell.skip = True
        problem = [[0]*9 for _ in range(9)]
        for (i, j) in product(range(9), repeat=2):
            cell = self.cells[(i, j)]
            if cell.text.isnumeric():
                problem[i][j] = int(cell.text)

        solver = Z3Solver(problem)
        result = solver.solve()

        if result == z3.sat:
            model = solver.model()
            grid = lambda i, j: z3.Int("grid[%d,%d]" % (i, j))
            for (i, j) in product(range(Z3Solver.GRID_SIZE), repeat=2):
                self.cells[(i, j)].text = str(model[grid(i, j)])
                self.root.ids.message.text = "Got Answer"
        else:
            self.root.ids.message.text = "Fail To Solve"
        self.root.ids.reset.disabled = False
        self.root.ids.solve.disabled = False
        Clock.unschedule(self.progress)
        for cell in self.cells.values():
            cell.skip=False
        self.progress_counter = 0

    def reset(self):
        self.root.ids.message.text = "Reset"
        sub_grids = self.root.ids.main_grid.children
        for cell in self.cells.values():
            cell.text = '*'
            cell.counter = 0


def main():
    SudokuApp().run()


if __name__ == '__main__':
    main()
