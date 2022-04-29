import numpy as np

circleData = np.array([[170,116,8],
                [22,232,6],
                [168,184,6],
                [168,218,6],
                [120,252,8],
                [168,202,8],
                [170,66,8],
                [170,100,8],
                [122,182,8],
                [72,234,6],
                [124,30,8],
                [172,32,8],
                [76,80,8],
                [120,234,6],
                [76,98,8],
                [24,164,8],
                [168,254,8],
                [124,64,8],
                [222,100,8],
                [76,46,8],
                [74,148,8],
                [224,48,8],
                [124,82,8],
                [224,66,8],
                [122,166,8],
                [74,200,6],
                [120,288,6],
                [26,28,6],
                [122,116,6],
                [222,116,6],
                [74,132,8],
                [168,168,6],
                [22,216,6],
                [20,304,6],
                [18,342,6],
                [26,62,6],
                [222,134,8],
                [222,150,6],
                [170,362,6],
                [76,64,8],
                [122,98,8],
                [24,112,8],
                [22,198,8],
                [74,216,8],
                [72,268,6],
                [76,114,8],
                [170,48,8],
                [122,200,6],
                [20,268,6],
                [170,82,8],
                [168,150,8],
                [24,130,6],
                [24,180,6],
                [72,250,6],
                [120,270,6],
                [222,290,6],
                [72,342,6],
                [224,32,6],
                [24,146,6],
                [168,236,8],
                [168,272,6],
                [72,286,6],
                [222,184,8],
                [22,250,6],
                [20,286,6],
                [122,342,6],
                [18,360,6],
                [120,362,6],
                [170,134,8],
                [72,304,6],
                [72,324,8],
                [170,344,6],
                [222,220,6],
                [168,288,6],
                [72,360,6],
                [26,46,8],
                [222,82,6],
                [222,168,6],
                [222,202,6],
                [222,272,6],
                [18,322,6],
                [122,148,6],
                [74,182,6],
                [120,218,6],
                [222,308,6],
                [76,30,6],
                [122,132,6],
                [222,236,8],
                [124,48,8],
                [26,80,7],
                [170,326,6],
                [168,308,6],
                [224,362,8],
                [74,166,8],
                [224,344,6],
                [26,96,6],
                [222,254,6],
                [120,324,6],
                [224,326,6],
                [120,306,8]])

blobData = np.array([[31, 83],
                    [176, 154],
                    [81, 118], 
                    [129, 102], 
                    [78, 341], 
                    [226, 360], 
                    [126, 306], 
                    [227, 239], 
                    [227, 205], 
                    [81, 169], 
                    [173, 290], 
                    [27, 323], 
                    [126, 272], 
                    [79, 254], 
                    [30, 185], 
                    [180, 33], 
                    [232, 67], 
                    [131, 49], 
                    [174, 222], 
                    [176, 137]])

simpleCircles = np.array([[1,1],[2,1],[3,1],[4,1],[5,1],
                        [1,2],[2,2],[3,2],[4,2],[5,2],
                        [1,3],[2,3],[3,3],[4,3],[5,3],
                        [1,4],[2,4],[3,4],[4,4],[5,4],
                        [1,5],[2,5],[3,5],[4,5],[5,5]
                        ])

simpleBlobs = np.array([[1,1],[2,2],[3,3],[4,4],[5,5]])

class Sorter:
    #stap 1: matrix met cirkels: x,y,z coordinaten
    def __init__(self, circles, blobs):
        self.__circles = circles
        self.__blobs = blobs
        

#stap2:de data sorteren op y(oplopend)

    def sortY(self):
        sortedY = self.__circles[self.__circles[:,1].argsort()]

        # this returns a matrix with the Y values sorted
        return sortedY

# stap 3: Maak een nieuwe array, met subarrays per 5 om die daarna op X te kunnen sorteren
    def chunkPerN(self, sortedY, numberOfChunks):    
        n = numberOfChunks
        chunkedPerFive = [sortedY[i:i + n] for i in range(0, len(sortedY), n)]

        # this returns a matrix with chunks (specified in)
        return chunkedPerFive

# stap 4: sorteer op X
    def sortX(self, chunks):
        
        sortedX = []
        for i in range(0,len(chunks)):
            sorter = lambda x: (x[0])
            sortedchunkX = sorted(chunks[i], key=sorter)
            sortedX.append(sortedchunkX)

        #this returns a matrix with sorted X values
        return sortedX

 # stap 6: X, Y waarden van de blobs vergelijken met die van de matrix uit stap 4
    def createAnswerMatrix(self, sortedCircles, sortedBlobs, difference):
        arraySize = len(sortedCircles) * len(sortedCircles[0])
        answerMatrix = np.zeros(arraySize)
        shapedAnswerMatrix = np.reshape(answerMatrix, (len(sortedCircles), len(sortedCircles[0])))
        for row in range(0, len(sortedBlobs)):
            blobX = sortedBlobs[row][0]
            blobY = sortedBlobs[row][1]
            for col in range(0, len(sortedCircles[0])):
                circleX = sortedCircles[row][col][0]
                circleY = sortedCircles[row][col][1]
                if ((abs(blobX-circleX) < difference).all() and (abs(blobY-circleY) < difference).all()):
                    shapedAnswerMatrix[row][col] = 1

        # This returns the answermatrix with a '1' in the position of a blob
        return shapedAnswerMatrix
        

    def sortBlobs(self):
        sortedX = self.__blobs[self.__blobs[:,0].argsort()]
        sortedFull = sortedX[sortedX[:,1].argsort()]

        # this returns the blob matrix sorted
        return sortedFull
 
    def sortAllCirkels(self, numberOfChunks):
        sortedY = self.sortY()
        chunks = self.chunkPerN(sortedY, numberOfChunks)
        sortedXY = self.sortX(chunks)

        # this returns the circle matrix fully sorted
        return sortedXY
    
    def printAnswerLetters(self, answers):
        answerstring = "Answers:\n"
        for row in range(0, len(answers)):
            for column in range(0, len(answers[0])):
                if answers[row,column] == 1:
                    position = column
                    if column == 0:
                        answerstring = answerstring + str(row) + "A\n"
                    elif column == 1:
                        answerstring = answerstring + str(row) + "B\n"
                    elif column == 2:
                        answerstring = answerstring + str(row) + "C\n"
                    elif column == 3:
                        answerstring = answerstring + str(row) + "D\n"
                    elif column == 4:
                        answerstring = answerstring + str(row) + "E\n"
                    else:
                        answerstring += "Nothing detected"
        # this creates a string with the answers
        return answerstring  

    def createAnswerArray(self, answers):
        answerArray = np.zeros(20)
        for row in range(0, len(answers)):
            for column in range(0, len(answers[0])):
                if answers[row,column] == 1:
                    answerArray[row] = column + 1
        return answerArray

    def getSortedAnswerArray(self, numberOfOptions, pixelDifference=10):
        sortedCircles = self.sortAllCirkels(numberOfOptions)
        sortedBlobs = self.sortBlobs()
        answers = self.createAnswerMatrix(sortedCircles, sortedBlobs, pixelDifference)
        letterAnswers = self.printAnswerLetters(answers)
        return self.createAnswerArray(answers)
        
# sorter = Sorter(circleData, blobData)
# print(sorter.getSortedAnswerArray(5, 10))



