import simplex

decisionVariables = [
    simplex.DecisionVariable('x1'),
    simplex.DecisionVariable('x2')
]

objectiveFunction = simplex.ObjectiveFunction(
    'min',
    [-5, -3]
)

constraints = [
    simplex.Constraint(
        '=',
        [2, 1, 100]
    ),
    simplex.Constraint(
        '<=',
        [1, 3, 150]
    ),
]

model = simplex.Model(decisionVariables, objectiveFunction, constraints)

solution = model.solve()

solution.exportCSV()