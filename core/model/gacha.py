import random
from global_consts import GUARANTEED_SPINS_AMOUNT

class GachaSystem:
    def __init__(self):
        pass
    
    def get_probability(self, roll):
        if roll < GUARANTEED_SPINS_AMOUNT * 2 // 3:
            return 0.005 + 0.0005 * roll
        elif roll < GUARANTEED_SPINS_AMOUNT - GUARANTEED_SPINS_AMOUNT // 6:
            return 0.015 + 0.05 * (roll - 20)
        elif roll < GUARANTEED_SPINS_AMOUNT:
            return 0.265 + 0.147 * (roll - 25)
        else:
            return 1
    
    def roll(self, rolled):
        probability = self.get_probability(rolled)
        if random.random() < probability:
            return True
        else:
            return False
