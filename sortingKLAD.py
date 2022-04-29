import numpy as np

data = np.array([[170,116,8],
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


class Sorter:
    #stap 1: matrix met cirkels: x,y,z coordinaten
    def __init__(self, data):
        self.__data = data
        

#stap2:dedatasorterenopy(oplopend)

    def sortY(self):
        #print("original:")
        #print(self.__data)
        #print("-----------------")
        #print("sorted on Y")
        sortedY = self.__data[self.__data[:,1].argsort()]
        #print(sortedY) 
        return sortedY

# stap 3: Maak een nieuwe array, met subarrays per 5 om die daarna op X te kunnen sorteren
    def chunkPerFive(self, sortedY):
        #print("start")
        n=5
        chunkedPerFive=[sortedY[i:i + n] for i in range(0, len(sortedY), n)]
        print("sorted into 5 arrays")
        #print(chunkedPerFive)
        return chunkedPerFive

# stap 4: sorteer op X
    # def sortX(self):
        # print("sorting X")
        # chunked = self.chunkPerFive()
        # sortedX = 
        # print(sortedX)
        
 # stap 6: X, Y waarden van de blobs vergelijken met die van de matrix uit stap 4
    def createAnswerMatrix(self, circles, blobs, row, col):
        amount = (row*col)
        answersMatrix = np.empty(amount)
        answersMatrix.fill(0)
        shapedMatrix = np.reshape(answersMatrix, (row,col))
        for r in range(0, len(circels)):
            for c in range(0, col)
        for r in range(0, 20):
            for c in range(0, 5):
                # check if 
                    if abs(blobs[c][0] - cirkels[c][0]) < 5 and abs(blobs[r][1] - cirkels[r][1]) < 5:
                        shapedMatrix[r][c] = 1

    # print(shapedMatrix)



    def sortAll(self):
        print(self.sortY())
        self.chunkPerFive()
        #self.sortX()
        #self.createAnswerMatrix()

sorter = Sorter(data)
sorter.sortAll()

