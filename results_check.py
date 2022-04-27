from printer import printer

class ResultsChecker:
    def __init__(self, correction):
        self.__correctArray[] = correction
        self.__numberOfQuestions = len(self.__correctArray)
        self.__totalScore = 0

    def correctNormal(self, answers):
        for i in range(self.__numberOfQuestions):
            if self.__correctArray[i] == answers[i]:
                self.__totalScore += 1
        
        return self.__totalScore
    
    def correctWithGuessCorrection(self, answers):
        point_reduction = (1/(self.__numberOfQuestions - 1))
        for i in range(self.__numberOfQuestions):
            if self.__correctArray[i] == answers[i]:
                self.__totalScore += 1
            elif answers[i] == 0:
                self.__totalScore += 0
            elif self.__correctArray[i] != answers[i]:
                self.__totalScore -= point_reduction
        return self.__totalScore

    def printResults(self, printerPort, studentName):
        resultString = "{}".format(self.__totalScore) + "/" + "{}".format(self.__numberOfQuestions)
        my_printer = printer.Printer(printerPort)
        my_printer.print_text("The score for {} is:").format(studentName)
        my_printer.print_text(resultString)     
        return console.log("Printing: {}").format("The score for {} is:").format(studentName)   
            
