import tkinter as tk
from game import RouletteGame


class RouletteGUI:
    def __init__(self):
        """Start the GUI for the Roulette Game."""
        self.game = RouletteGame()
        self.root = tk.Tk()
        self.root.title("Roulette Game")
        self.setup_ui()

    def setup_ui(self):
        """Setup the GUI components."""
        # Balance Label
        self.balance_label = tk.Label(self.root, text=f"Balance: ${self.game.balance}", font=("Arial", 14))
        self.balance_label.grid(row=0, column=0, columnspan=8, pady=10)

        # Result Label
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.grid(row=1, column=0, columnspan=8, pady=5)

        # Roulette Table
        self.canvas = tk.Canvas(self.root, width=900, height=600, bg="white")
        self.canvas.grid(row=2, column=0, columnspan=8)
        self.create_roulette_table()

        # Bet Amount Selection
        tk.Label(self.root, text="Bet Amount:", font=("Arial", 14)).grid(row=3, column=0, columnspan=8, pady=10)
        for i, amount in enumerate([10, 50, 100, 500]):
            tk.Button(
                self.root,
                text=f"${amount}",
                width=10,
                font=("Arial", 12),
                command=lambda x=amount: self.set_bet_amount(x)
            ).grid(row=4, column=i, padx=5, pady=5)

        # Spin Button
        self.spin_button = tk.Button(self.root, text="SPIN", font=("Arial", 16), bg="green", fg="white",
                                     command=self.spin_wheel)
        self.spin_button.grid(row=5, column=0, columnspan=4, pady=20)

        # Reset Button
        self.reset_button = tk.Button(self.root, text="RESET", font=("Arial", 16), bg="red", fg="white",
                                      command=self.reset_game)
        self.reset_button.grid(row=5, column=4, columnspan=4, pady=20)

    def create_roulette_table(self):
        """Roulette table layout."""
        numbers = [
            ["00", "0"],
            ["3", "6", "9", "12", "15", "18", "21", "24", "27", "30", "33", "36"],
            ["2", "5", "8", "11", "14", "17", "20", "23", "26", "29", "32", "35"],
            ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"],
            ["1 TO 18", "EVEN", "RED", "BLACK", "ODD", "19 TO 36"],
            ["1 TO 12", "13 TO 24", "25 TO 36"]
        ]

        tile_width = 80
        tile_height = 50
        x_offset = 20
        y_offset = 20

        for row_idx, row in enumerate(numbers):
            for col_idx, num in enumerate(row):
                x_start = x_offset + col_idx * tile_width
                y_start = y_offset + row_idx * tile_height
                x_end = x_start + tile_width
                y_end = y_start + tile_height

                color, text_color = self.get_tile_colors(num)
                self.canvas.create_rectangle(x_start, y_start, x_end, y_end, fill=color, outline="black")
                text_id = self.canvas.create_text(
                    (x_start + x_end) / 2, (y_start + y_end) / 2, text=num, fill=text_color, font=("Arial", 12)
                )
                self.canvas.tag_bind(text_id, "<Button-1>", lambda event, n=num: self.place_bet(n))

    def get_tile_colors(self, num: str):
        """Get tile background and text color."""
        if num in ["RED", "BLACK", "EVEN", "ODD", "1 TO 18", "19 TO 36", "1 TO 12", "13 TO 24", "25 TO 36"]:
            return "white", "black"
        elif num == "RED":
            return "red", "white"
        elif num == "BLACK":
            return "black", "white"
        elif num == "0" or num == "00":
            return "green", "white"
        else:
            return ("red", "white") if int(num) % 2 != 0 else ("black", "white")
        
    def set_bet_amount(self, amount: int):
        """Set the bet amount."""
        self.game.set_bet_amount(amount)
        self.update_result(f"Bet Amount Set: ${amount}", "blue")

    def place_bet(self, number: str):
        """Place a bet on the selected number."""
        success, message = self.game.place_bet(number)
        if success:
            self.update_balance()
        self.update_result(message, "blue" if success else "red")

    def spin_wheel(self):
        """Spin the wheel and show the result."""
        result, message = self.game.spin_wheel()
        if result:
            self.highlight_result(result)
        self.update_result(message, "green" if "won" in message else "red")
        self.update_balance()

    def highlight_result(self, number: str):
        """Highlight the winning number."""
        for item_id in self.canvas.find_all():
            if self.canvas.itemcget(item_id, "text") == number:
                coords = self.canvas.coords(item_id)
                x, y = coords[0], coords[1]
                self.canvas.create_oval(
                    x - 20, y - 20, x + 20, y + 20, fill="yellow", outline="black", tags="highlight"
                )

    def reset_game(self):
        """Reset the game to its initial state."""
        self.game.reset_game()
        self.update_balance()
        self.update_result("", "black")
        self.canvas.delete("highlight")

    def update_balance(self):
        """Update the balance display."""
        self.balance_label.config(text=f"Balance: ${self.game.balance}")

    def update_result(self, message: str, color: str):
        """Update the result message."""
        self.result_label.config(text=message, fg=color)

    def run(self):
        """Run the game."""
        self.root.mainloop()
