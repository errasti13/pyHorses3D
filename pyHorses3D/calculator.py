#calculator.py

class Horses3DCalculator:
    def __init__(self, solution):
        self.solution = solution

    def compute_magnitude(self, name):
        magnitude = sum(self.solution.magnitudes.values())  # Just a placeholder computation
        self.solution.add_magnitude(name, magnitude)