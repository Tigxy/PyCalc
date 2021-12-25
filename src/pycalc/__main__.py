from .calculator import solve
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("formula", type=str, help="the formula to evaluate")

args = parser.parse_args()
try:
    print("Result is", solve(args.formula))
except ValueError as err:
    print("Failed to evaluate formula:", err)
