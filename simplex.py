class Model:
    def __init__(self, decisionVariables, objectiveFunction, constraints):
        self.decisionVariables = decisionVariables
        self.objectiveFunction = objectiveFunction
        self.constraints = constraints

        self.slackVariables = []
        self.table = []

        self.pivotColumn = 0
        self.pivotRow = 0
        self.pivot = 0

        self.neoPivotRow = []
    

    def solve(self):
        self.addSlackVariables()
        self.createTable()
        while self.thereIsNegative():
            self.getPivot()
            self.recreateTable()
        
        return Table(self.table)
    
    def result(self):
        for line in self.table:
            print(line)

    def addSlackVariables(self):
        i = 0
        for constraint in self.constraints:
            i += 1

            if constraint.getComparisonOperator() == '<' or constraint.getComparisonOperator() == '<=':
                self.slackVariables.append(SlackVariable(f's{i}', 1))
            elif constraint.getComparisonOperator() == '>' or constraint.getComparisonOperator() == '>=':
                self.slackVariables.append(SlackVariable(f's{i}', -1))
            else:
                self.slackVariables.append(SlackVariable(f's{i}', 0))
    
    def createTable(self):
        self.addVariablesRow()
        self.addFunctionRow()
        for i in range(len(self.constraints)):
            self.addConstraintRow(self.constraints[i], self.slackVariables[i], i)
    
    def addVariablesRow(self):
        row = [' ']

        for decisionVariable in self.decisionVariables:
            row.append(decisionVariable.getDecisionVariable())
        
        for slackVariable in self.slackVariables:
            row.append(slackVariable.getLabel())
        
        row.append(' ')

        self.table.append(row)
    
    def addFunctionRow(self):
        row = ['Z']

        if self.objectiveFunction.getObjective() == 'max':
            multiplier = -1
        else:
            multiplier = 1
        
        for value in self.objectiveFunction.getFunction():
            row.append(value * multiplier)
        
        for slackVariable in self.slackVariables:
            row.append(0)
        
        row.append(0)

        self.table.append(row)
    
    def addConstraintRow(self, constraint, slackVariable, position):
        row = [slackVariable.getLabel()]

        for i in range(len(constraint.getConstraint()) - 1):
            row.append(constraint.getConstraint()[i])
        
        for i in range(len(self.constraints)):
            if i == position:
                row.append(slackVariable.getSlack())
            else:
                row.append(0)
        
        row.append(constraint.getConstraint()[-1])

        self.table.append(row)
    
    def thereIsNegative(self):
        for i in self.table[1]:
            if (type(i) == int or type(i) == float) and i < 0:
                return True
    
    def getPivot(self):
        self.getPivotColumn()
        self.getPivotRow()

        self.pivot = self.table[self.pivotRow][self.pivotColumn]
    
    def getPivotColumn(self):
        lowest = 0
        pos = 0

        for i in range(1, len(self.table[1]) - 1):
            if self.table[1][i] < lowest:
                lowest = self.table[1][i]
                pos = i
        
        self.pivotColumn = pos


    def getPivotRow(self):
        lowest = 0
        pos = 0
        flag = True

        for i in range(1, len(self.table)):
            if self.table[i][self.pivotColumn] <= 0:
                continue

            div = self.table[i][-1] / self.table[i][self.pivotColumn]

            if flag:
                lowest = div
                pos = i
                flag = False
            else:
                if div < lowest:
                    lowest = div
                    pos = i
        
        self.pivotRow = pos
    
    def recreateTable(self):
        self.transformPivotRow()
        self.transformPivotColumn()
    
    def transformPivotRow(self):
        self.table[self.pivotRow][0] = self.table[0][self.pivotColumn]
        
        for i in range(1, len(self.table[0])):
            self.table[self.pivotRow][i] = self.table[self.pivotRow][i] / self.pivot
    
    def transformPivotColumn(self):
        for i in range(1, len(self.table)):
            if i == self.pivotRow:
                continue

            multiplier = (-1) * self.table[i][self.pivotColumn]

            self.neoPivotRow = self.table[self.pivotRow].copy()

            self.multiplyPivotRow(multiplier)
            
            self.addNeoPivotRow(i)
    
    def multiplyPivotRow(self, multiplier):
        for i in range(1, len(self.neoPivotRow)):
            self.neoPivotRow[i] = self.neoPivotRow[i] * multiplier
    
    def addNeoPivotRow(self, line):
        for i in range(1, len(self.table[line])):
            self.table[line][i] = self.table[line][i] + self.neoPivotRow[i]

class DecisionVariable:
    def __init__(self, decisionVariable):
        self.decisionVariable = decisionVariable
    
    def getDecisionVariable(self):
        return self.decisionVariable

class ObjectiveFunction:
    def __init__(self, objective, function):
        self.objective = objective
        self.function = function
    
    def getObjective(self):
        return self.objective
    
    def getFunction(self):
        return self.function

class Constraint:
    def __init__(self, comparisonOperator, constraint):
        self.comparisonOperator = comparisonOperator
        self.constraint = constraint
    
    def getComparisonOperator(self):
        return self.comparisonOperator
    
    def getConstraint(self):
        return self.constraint

class SlackVariable:
    def __init__(self, label, slack):
        self.label = label
        self.slack = slack
    
    def getLabel(self):
        return self.label
    
    def getSlack(self):
        return self.slack

class Table:
    def __init__(self, table):
        self.table = table
    
    def __repr__(self):
        table = ''
        for row in range(len(self.table)):
            for column in range(len(self.table[row])):
                table = table + f'{self.table[row][column]}\t'
            table = table + '\n'
        return table
    
    def exportCSV(self):
        csv = ''
        for row in range(len(self.table)):
            for column in range(len(self.table[row])):
                csv = csv + f'{self.table[row][column]},'
            csv = csv + '\n'
        
        file = open('solution.csv', 'w')
        file.write(csv)
        file.close()