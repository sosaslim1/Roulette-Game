import random
from typing import List, Dict


class RouletteGame:
    def __init__(self):
        """Start the game logic."""
        self.balance: int = 1000
        self.selected_bet_amount: int = 10
        self.active_bets: List[Dict] = []

    def set_bet_amount(self, amount: int):
        """Set the amount for the next bet."""
        self.selected_bet_amount = amount

    def place_bet(self, number: str):
        """Place a bet on a number or category."""
        if self.balance >= self.selected_bet_amount:
            self.balance -= self.selected_bet_amount
            self.active_bets.append({"number": number, "amount": self.selected_bet_amount})
            return True, f"Bet Placed: ${self.selected_bet_amount} on {number}"
        return False, "Insufficient Balance!"

    def spin_wheel(self):
        """Spin the roulette wheel and determine the result."""
        if not self.active_bets:
            return None, "Place a Bet First!"

        result = random.choice([str(i) for i in range(1, 37)] + ["0", "00"])
        winnings = sum(bet["amount"] * 36 for bet in self.active_bets if bet["number"] == result)
        self.balance += winnings
        self.active_bets.clear()
        return result, f"Winning Number: {result}. {'You won!' if winnings > 0 else 'Better luck next time!'}"

    def reset_game(self):
        """Reset the game to its initial state."""
        self.balance = 1000
        self.active_bets = []
