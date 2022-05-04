from final_sorter import Sorter
from results_check import ResultsChecker
from printer import printer
from machinevision import MachineVision
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

# from blobtest import blob
# circles and blobs = via function from blobs
machineVision = MachineVision()
machineVision.getResults()
allcirlces = machineVision.getCirlces()# return matrix with circles 
allblobs = machineVision.getBlobs()# return matrix blobs


# Create new sorter object and give circle and blob data
answerKey = Sorter(circleData, blobData)

# Let the sorter create an answers array
teacherCopy = answerKey.getSortedAnswerArray(5, 12)

studentAnswers = Sorter(allcirlces, allblobs)

studentCopy = studentAnswers.getSortedAnswerArray(5, 12)

resultsChecker = ResultsChecker(teacherCopy, studentCopy)
score = resultsChecker.correctNormal()
print(score)
resultsChecker.printResults("ACM0", "Autograder")


