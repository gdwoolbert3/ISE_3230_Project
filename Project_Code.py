# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 19:09:34 2021
Project Code
@author: gordo
"""

# Import Necessary Packages
import cvxpy as cp
import pandas as pd

#%% 0. Data Import

# Import Food Data
dataPath = "C://Users/gordo/Downloads/FoodData.csv" # Path to food data file
df = pd.read_csv(dataPath)

# Import Recommendation Data
recPath = "C://Users/gordo/Downloads/Recs.csv" # Path to recommendations file
recs = pd.read_csv(recPath)

#%% 1. Create Necessary Constants

# Prompt for Desired Caloric Intake
Cal = int(input("Enter Desired Caloric Intake: "))
Objective = int(
    input(
        "Minimize CO2 Emissions (1), PO4 Emissions (2), or Water Use (3): "
        )
    )
MaxCost = int(input("Enter Budget in Dollars (if none, enter 0): "))

# Create Variable for Number of Foods
NF = len(df)

# Calculate Conversion Rate Given Caloric Intake
r = Cal / 2000.0

# Create List of Food Names
Foods = df["Food"]

# Create Lists of Objective Function Variables
EC = df["CO2"]
EF = df["PO4"]
W = df["Water-Use"]

# Create List of Constants for Constraints
CpK = df["Cal-per-Kg"]
Cost = df["Cost"]

# Create List of Nutrients/Vitamins
NV = [
      "Protein",
      "Carbs", 
      "Fats", 
      "Fiber", 
      "V-A", 
      "V-C", 
      "V-E", 
      "V-K",
      "Calc",
      "Iron",
      "Mag",
      "Zinc"
      ]

#%% 2. Set-Up Optimization Problem

# Declare Decision Variables (kg of each food)
X = cp.Variable(NF, nonneg = True)

# Objective function
if Objective == 1:
    # EC is a List of Carbon Emissions for Each Food
    obj_func = cp.sum(cp.multiply(X, EC))
elif Objective == 2:
    # EF is a List of Phosphate Emissions for Each Food
    obj_func = cp.sum(cp.multiply(X, EF))
elif Objective == 3:
    # W is a List of Water Usage for Each Food
    obj_func = cp.sum(cp.multiply(X, W))

#%% 3. Add Constraints

# Create Constraint List
constraints = []

# Add Caloric Constraint (Cal input by User)
constraints.append(cp.sum(cp.multiply(X, CpK)) >= 0.9*Cal)
constraints.append(cp.sum(cp.multiply(X, CpK)) <= 1.1*Cal)

# Add Constraints for all other Nutrients and Vitamins:
# Protein, Carbs, Fats, Fiber, V-A, V-C, V-E, V-K, Calc, Iron, Mag, and Zinc
# r is a proportion determined by desired daily caloric intake
# df contains food data and recs contains recommendations
for v in NV:
    constraints.append(cp.sum(cp.multiply(X, df[v])) >= 0.9*recs[v]*r)
    constraints.append(cp.sum(cp.multiply(X, df[v])) <= 1.1*recs[v]*r)

# Add Cost Constraint (MaxCost input by User)
if MaxCost > 0:
    constraints.append(cp.sum(cp.multiply(X, Cost)) <= MaxCost)

#%% 4. Solve Problem

# Create Problem Object
problem = cp.Problem(cp.Minimize(obj_func), constraints)

# Solve Problem
problem.solve(solver = cp.GUROBI, verbose= True)

# Display Output
print("obj_func =")
print(obj_func.value)
print("X = ")
for i in range(NF):
    if X[i].value > 0:
        print(str(1000*X[i].value) + " grams of " + str(Foods[i]))
print("Cost =")
print(cp.sum(cp.multiply(X, Cost)).value)
