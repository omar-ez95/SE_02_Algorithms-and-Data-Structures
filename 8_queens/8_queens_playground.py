import tkinter as tk

class NQueensGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('N Queens Problem')

        self.label = tk.Label(self.master, text="Enter n:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.master)
        self.entry.pack(pady=10)

        self.btn_generate = tk.Button(self.master, text="Generate Board", command=self.generate_board)
        self.btn_generate.pack(pady=10)

        self.board_frame = None

    def generate_board(self):
        if self.board_frame:
            self.board_frame.destroy()

        self.n = int(self.entry.get())
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(pady=10)

        self.buttons = []
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]

        for i in range(self.n):
            row_buttons = []
            for j in range(self.n):
                color = "white" if (i + j) % 2 == 0 else "black"
                btn = tk.Button(self.board_frame, bg=color, width=4, height=2, command=lambda x=i, y=j: self.place_queen(x, y))
                btn.grid(row=i, column=j)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        if not hasattr(self, 'btn_forbidden'):
            self.btn_forbidden = tk.Button(self.master, text="Show Forbidden Squares", command=self.show_forbidden_squares)
            self.btn_forbidden.pack(pady=10)

    def place_queen(self, x, y):
        color = "white" if (x + y) % 2 == 0 else "black"
        if self.board[x][y] == 0:
            self.board[x][y] = 1
            self.buttons[x][y].config(text="Q", bg="yellow")
        else:
            self.board[x][y] = 0
            self.buttons[x][y].config(text="", bg=color)

    def show_forbidden_squares(self):
        for i in range(self.n):
            for j in range(self.n):
                color = "white" if (i + j) % 2 == 0 else "black"
                if self.board[i][j] != 1:
                    self.buttons[i][j].config(bg=color)

        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 1:
                    self.attack_squares(i, j)

    def attack_squares(self, x, y):
        for i in range(self.n):
            if i != x and self.board[i][y] != 1:
                self.buttons[i][y].config(bg="red")
            if i != y and self.board[x][i] != 1:
                self.buttons[x][i].config(bg="red")

        for i in range(1, self.n):
            if x + i < self.n and y + i < self.n and self.board[x + i][y + i] != 1:
                self.buttons[x + i][y + i].config(bg="red")
            if x + i < self.n and y - i >= 0 and self.board[x + i][y - i] != 1:
                self.buttons[x + i][y - i].config(bg="red")
            if x - i >= 0 and y + i < self.n and self.board[x - i][y + i] != 1:
                self.buttons[x - i][y + i].config(bg="red")
            if x - i >= 0 and y - i >= 0 and self.board[x - i][y - i] != 1:
                self.buttons[x - i][y - i].config(bg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()
