import numpy

class Card:

    def __init__(self, grid, rowSums, columnSums):
        self.grid = grid
        self.rowSums = rowSums
        self.columnSums = columnSums

    def draw(self, showTotals = True):
        print("+" + "---+"*3)
        for i, row in enumerate(self.grid):
            if showTotals:
                print(("| {}   {}   {} | {}").format(*[x if x != 0 else " " for x in row], self.rowSums[i]))
            else:
                print(("| {}   {}   {} |").format(*[x if x != 0 else " " for x in row]))
            
            if i % 3 == 2:
                print("+" + "---+"*3)
                if showTotals:
                    print(("{}{}{}").format(*[str(columnSum).rjust(4, ' ') for columnSum in self.columnSums]))                
            else:
                print("+" + "   +"*3)
        
    def rotate(self, matrix, forward = True):
        if forward:
            return numpy.rot90(matrix, 3)
        else:
            return numpy.rot90(matrix, -3)
        
    def getRowCount(self):
        return len(self.grid)

    def getColumnCount(self):
        rotatedGrid = self.rotate(self.grid)
        return len(rotatedGrid)

    def getRow(self, index):
        return self.grid[index]

    def getColumn(self, index):
        column = []
        for row in self.grid:
            column.append(row[index])
        return column

    def printRow(self, index):
        print(("row {}: {}   {}   {}").format(index, *[rowItem for rowItem in self.getRow(index)]))

    def printColumn(self, index):
        print(("col {}: {}   {}   {}").format(index, *[colItem for colItem in self.getColumn(index)]))

    def calculateCompleteness(self):
        completenessMap = {}

        # *[x if x != 0 else " " for x in row]
        for x, row in enumerate(self.grid):
            completenessMap["r"+str(x)] = numpy.count_nonzero(row)

        rotatedGrid = self.rotate(self.grid)
        for y, column in enumerate(rotatedGrid):
            completenessMap["c"+str(y)] = numpy.count_nonzero(column)

        print(completenessMap)

    def findMostComplete(self):
        highestCompleteness = 0
        highestCompletenessIndex = -1

        i = 0
        for x, row in enumerate(self.grid):
            completeness = numpy.count_nonzero(row)
            if completeness > highestCompleteness and completeness < len(row):
                (highestCompleteness, highestCompletenessIndex) = (completeness, i)
            i+=1

        rotatedGrid = self.rotate(self.grid)
        for y, column in enumerate(rotatedGrid):
            completeness = numpy.count_nonzero(column)
            if completeness > highestCompleteness and completeness < len(column):
                (highestCompleteness, highestCompletenessIndex) = (completeness, i)
            i+=1

        return highestCompletenessIndex

    def fillMostComplete(self, mostCompleteIndex):
        i = 0
        for x, row in enumerate(self.grid):
            # print(("row: {}").format(row))
            if i == mostCompleteIndex:
                missingValue = self.rowSums[i] - numpy.sum(row)
                if missingValue > 0:
                    # print(("missingValue: {}").format(missingValue))
                    indexOfZero = list(row).index(0)
                    row[indexOfZero] = missingValue
            i+=1

        rotatedGrid = self.rotate(self.grid)
        for y, column in enumerate(rotatedGrid):
            # print(("column: {}").format(list(column)))
            if i == mostCompleteIndex:
                missingValue = self.columnSums[i - len(self.rowSums)] - numpy.sum(column)
                if missingValue > 0:
                    # print(("missingValue: {}").format(missingValue))
                    indexOfZero = list(column).index(0)
                    column[indexOfZero] = missingValue
            i+=1

        self.grid = self.rotate(rotatedGrid, False)


if __name__ == '__main__':

    # grid = [
    #     [4, 0, 0],
    #     [0, 5, 0],
    #     [3, 1, 0],
    # ]
    # rowSums = [15, 20, 10]
    # columnSums = [14, 8, 23]
    grid = [
        [0, 5, 0],
        [9, 0, 0],
        [0, 6, 1],
    ]
    rowSums = [11, 20, 14]
    columnSums = [18, 14, 13]

    game_card = Card(grid, rowSums, columnSums)
    print("\n\n\n***** BEFORE *****")
    game_card.draw()

    mostCompleteIndex = game_card.findMostComplete()
    while mostCompleteIndex >= 0:
        print(("mostCompleteIndex: {}").format(mostCompleteIndex))
        game_card.fillMostComplete(mostCompleteIndex)
        mostCompleteIndex = game_card.findMostComplete()
        pass

    print("\n***** AFTER *****")
    game_card.draw()

    # game_card.printRow(0)
    # game_card.printRow(1)
    # game_card.printRow(2)

    # game_card.printColumn(0)
    # game_card.printColumn(1)
    # game_card.printColumn(2)

    # print(("rc: {}").format(game_card.getRowCount()))
    # print(("cc: {}").format(game_card.getColumnCount()))

    # game_card.calculateCompleteness()

    # game_card.draw(False)
    # game_card.grid = game_card.rotate(game_card.grid, False)
    # game_card.draw(False)
