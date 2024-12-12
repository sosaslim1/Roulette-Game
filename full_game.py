import random
from typing import List, Dict


class RouletteGame:
    def __init__(self):
        """Initialize the game logic."""
        self.balance: int = 1000
        self.selected_bet_amount: int = 10
        self.active_bets: List[Dict] = []
        self.colors = {  # Mapping of colors for numbers
            "00": "green", "0": "green",
            **{str(i): "red" for i in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]},
            **{str(i): "black" for i in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]}
        }

    def set_bet_amount(self, amount: int):
        """Set the amount for the next bet."""
        self.selected_bet_amount = amount

    def place_bet(self, bet: str):
        """Place a bet on a number, color, or range."""
        if self.balance >= self.selected_bet_amount:
            self.balance -= self.selected_bet_amount
            self.active_bets.append({"type": bet, "amount": self.selected_bet_amount})
            return True, f"Bet Placed: ${self.selected_bet_amount} on {bet}"
        return False, "Insufficient Balance!"

    def spin_wheel(self):
        """Spin the roulette wheel and determine the result."""
        if not self.active_bets:  # Check if there are any active bets
            return None, "Place a Bet First!"

        # Randomly choose the winning number
        result = random.choice([str(i) for i in range(1, 37)] + ["0", "00"])
        result_color = self.colors.get(result, "green")  # Get the color of the winning number

        # Initialize winnings
        winnings = 0
        for bet in self.active_bets:  # Loop through all active bets
            bet_type = bet["type"]
            
            # Check if the bet matches the exact number
            if bet_type == result:
                winnings += bet["amount"] * 36

            # Check for color bets (RED/BLACK)
            elif bet_type.lower() == result_color:  # Bet matches the color
                winnings += bet["amount"] * 2  # Payout is 1:1 (double the bet)

            # Check for ODD/EVEN bets
            elif bet_type == "ODD" and self.is_odd(result):  # Bet matches ODD
                winnings += bet["amount"] * 2  # Payout is 1:1
            elif bet_type == "EVEN" and self.is_even(result):  # Bet matches EVEN
                winnings += bet["amount"] * 2  # Payout is 1:1

        # Clear all bets after the spin
        self.active_bets.clear()

        # Update the balance and return the results
        if winnings > 0:
            self.balance += winnings
            return result, f"Winning Number: {result} ({result_color}). You won ${winnings}!"
        return result, f"Winning Number: {result} ({result_color}). Better luck next time!"

    def is_odd(self, number: str) -> bool:
        """Check if the given number is odd."""
        try:
            return int(number) % 2 != 0
        except ValueError:  # For "0" or "00"
            return False

    def is_even(self, number: str) -> bool:
        """Check if the given number is even."""
        try:
            return int(number) % 2 == 0
        except ValueError:  # For "0" or "00"
            return False

    def reset_game(self):
        """Reset the game to its initial state."""
        self.balance = 1000
        self.active_bets = []
