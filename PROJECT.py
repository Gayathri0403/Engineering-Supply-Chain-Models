import subprocess
import sys

# Step 1: Ensure PuLP is installed
try:
    import pulp
except ImportError:
    print("PuLP not found. Installing PuLP...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pulp"])
    import pulp

# Step 2: Define the SupplyChainOptimizer class
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, PULP_CBC_CMD

class SupplyChainOptimizer:
    def __init__(self, costs, distances, facilities, demand_points):
        """
        Initializes the SupplyChainOptimizer.

        Parameters:
        - costs: dict of dicts, e.g., costs[facility][demand_point]
        - distances: dict of dicts, e.g., distances[facility][demand_point]
        - facilities: list of facility names
        - demand_points: list of demand point names
        """
        self.costs = costs
        self.distances = distances
        self.facilities = facilities
        self.demand_points = demand_points

    def solve(self, weight_cost=0.5, weight_distance=0.5):
        """
        Solves the optimization problem using a weighted objective function.

        Parameters:
        - weight_cost: weight for cost in the objective (0 to 1)
        - weight_distance: weight for distance in the objective (0 to 1)

        Returns:
        - solution: dictionary of assigned facility-demand pairs
        """
        # Create a minimization problem
        model = LpProblem("MultiObjectiveFacilityLocation", LpMinimize)

        # Decision variables: x[(facility, demand_point)] ∈ {0, 1}
        x = {
            (f, d): LpVariable(f"x_{f}_{d}", cat="Binary")
            for f in self.facilities
            for d in self.demand_points
        }

        # Objective: weighted sum of cost and distance
        model += lpSum([
            weight_cost * self.costs[f][d] * x[(f, d)] +
            weight_distance * self.distances[f][d] * x[(f, d)]
            for f in self.facilities
            for d in self.demand_points
        ])

        # Constraint: each demand point is served by exactly one facility
        for d in self.demand_points:
            model += lpSum([x[(f, d)] for f in self.facilities]) == 1, f"Assign_{d}"

        # Solve the model
        model.solve(PULP_CBC_CMD(msg=False))

        # Extract solution
        solution = {
            (f, d): x[(f, d)].varValue
            for f in self.facilities
            for d in self.demand_points
            if x[(f, d)].varValue == 1
        }

        return solution

# Step 3: Sample usage
if __name__ == "__main__":
    # Sample data
    facilities = ['F1', 'F2']
    demand_points = ['D1', 'D2', 'D3']
    costs = {
        'F1': {'D1': 10, 'D2': 20, 'D3': 15},
        'F2': {'D1': 12, 'D2': 18, 'D3': 25}
    }
    distances = {
        'F1': {'D1': 5, 'D2': 10, 'D3': 6},
        'F2': {'D1': 6, 'D2': 7, 'D3': 9}
    }

    # Initialize optimizer
    optimizer = SupplyChainOptimizer(costs, distances, facilities, demand_points)

    # Solve with specified weights
    solution = optimizer.solve(weight_cost=0.6, weight_distance=0.4)

    # Display the solution
    print("Optimal Assignments:")
    for (facility, demand_point), value in solution.items():
        print(f"Facility {facility} serves Demand Point {demand_point}")
