from printer import printer

class ResultsChecker:
    def __init__(self,options):
        self.__totalScore = 0
        self.__answerKey = 0
        self.__numberOfQuestions = 0
        self.__numberOfOptions = options
        self.__studentAnswers = 0

    def setAnswerKey(self, answerKey):
        self.__answerKey = answerKey
        self.__numberOfQuestions = len(self.__answerKey)
    def getAnswerKey(self):
        return self.__answerKey

    def setStudentAnswers(self,studentAnswers):
        self.__studentAnswers = studentAnswers
    def getStudentAnswers(self):
        return self.__studentAnswers

    def correctNormal(self):
        self.__totalScore = 0
        for i in range(0, self.__numberOfQuestions):
            if self.__answerKey[i] == self.__studentAnswers[i]:
               	self.__totalScore += 1
        return self.__totalScore
    
    def correctWithGuessCorrection(self):
        self.__totalScore = 0
        point_reduction = (1/(self.__numberOfOptions - 1))
        for i in range(0, self.__numberOfQuestions):
            if self.__answerKey[i] == self.__studentAnswers[i]:
               	self.__totalScore += 1
            elif self.__studentAnswers[i] == 0:
                self.__answerKey += 0
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

    def resetMatrixStudent(self):
        self.__studentAnswers = 0
        
    def resetMatrixAnswer(self):
        self.__answerKey = 0
        self.__numberOfQuestions = 0



            
