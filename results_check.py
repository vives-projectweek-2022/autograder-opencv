from printer import printer

class ResultsChecker:
    def __init__(self, answerKey, studentAnswers):
        self.__answerKey = answerKey
        self.__numberOfQuestions = len(self.__answerKey)
        self.__studentAnswers = studentAnswers
        self.__totalScore = 0

    def correctNormal(self):
        for i in range(0, self.__numberOfQuestions):
            if self.__answerKey[i] == self.__studentAnswers[i]:
               	self.__totalScore += 1
        return self.__totalScore
    
    def correctWithGuessCorrection(self):
        point_reduction = (1/(self.__numberOfQuestions - 1))
        for i in range(0, self.__numberOfQuestions):
            if self.__answerKey[i] == self.__studentAnswers[i]:
               	self.__totalScore += 1
            else:
                self.__totalScore -= point_reduction

        return self.__totalScore

    def printResults(self, printerPort, studentName):
        my_printer = printer.Printer(printerPort)
        my_printer.print_text("The score for " + studentName + " is:")
        my_printer.print_text(str(self.__totalScore) + "/" + str(self.__numberOfQuestions))     
        print("Printing") 

    def resetScore(self):
        self.__totalScore = 0


            
