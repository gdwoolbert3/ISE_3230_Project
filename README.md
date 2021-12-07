# ISE_3230_Project
A repository for the code and data related to the final project for ISE 3230

This Repository contains 3 files other than this one:

FoodData.csv:
This file contains the 44 foods that were used in the linear optimization program as well as their nutritional information and cost information.

Recs.csv:
This file contains the FDA recommended daily amounts of various nutrients/vitamins (assuming a 2000 calorie diet).

Project_Code:
This is a .py file where the actual problem code is written out. To run this code, you will need 2 python libraries installed. The first is cvxpy. This library handles the creation and solving of linear programs. In this file, it is used to create the objective functions and constraints and to find the optimal solution. The second library needed is pandas. The file uses this library to read in and work with the data from the two .csv files (FoodData.csv and Recs.csv, both described above).
Finally, this file also requires that the user have the GUROBI solver installed as it is the actual solver that is used to find the optimal solution (NOTE: there is a way to do this using only cvxpy and not requiring GUROBI but that would require editing the code in the file and will not be discussed here).
