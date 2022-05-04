from numpy import size
import pygame
import pygame_menu
import cv2
from final_sorter import Sorter
from results_check import ResultsChecker
from printer import printer
from machinevision import MachineVision as mv
import numpy as np

class Menu:
    def __init__(self):
        self.__teacherBlobs = []
        self.__teacherCircles = []
        self.__studentBlobs = []
        self.__studentCircles = []

        self.__answerKey = []
        self.__studentAnswers = []
        self.__studentName = "Testing student"
        self.__grade = 0
        self.__machineVision = mv()
        self.__resultsChecker = ResultsChecker(5)

    def updateStudent(self):
        self.resetScore()
        self.__resultsChecker.resetMatrixStudent()
        self.__studentName = input("Please enter the student's name: ")
        print("Student registered: " + self.__studentName )

    def updateAnswerKey(self):
        self.__resultsChecker.resetMatrixAnswer()
        self.resetScore()
        self.__machineVision.getResults()
        self.__teacherCircles = self.__machineVision.getCirlces() 
        self.__teacherBlobs = self.__machineVision.getBlobs()
        #sorting
        sorting = Sorter(self.__teacherCircles, self.__teacherBlobs)
        self.__answerKey = sorting.getSortedAnswerArray(5, 10)
        print(str(self.__answerKey))
        self.__resultsChecker.setAnswerKey(self.__answerKey)
        print(str(self.__resultsChecker.getAnswerKey()))
        cv2.destroyAllWindows()
        print("correct answer received")

    def updateStudentAnswers(self):
        self.__resultsChecker.resetMatrixStudent()
        print("reset matrix")
        print(str(self.__resultsChecker.getStudentAnswers()))
        self.resetScore()
        self.__machineVision.getResults()
        self.__studentCircles = self.__machineVision.getCirlces()
        self.__studentBlobs = self.__machineVision.getBlobs()
        #sorting
        sorting = Sorter(self.__studentCircles, self.__studentBlobs)
        self.__studentAnswers = sorting.getSortedAnswerArray(5, 10)
        print()
        print(str(self.__studentAnswers))
        self.__resultsChecker.setStudentAnswers(self.__studentAnswers)
        print(str(self.__resultsChecker.getStudentAnswers()))
        cv2.destroyAllWindows()
        print("student answer received")

    def gradeGuessCorrection(self):
        self.__grade = self.__resultsChecker.correctWithGuessCorrection()
        print("guess correction: " + str(self.__grade))

    def gradeNormalCorrection(self):
        self.__grade = self.__resultsChecker.correctNormal()
        print("normal grading: " + str(self.__grade))

    def resetScore(self):
        self.__grade = 0

    def printScore(self):
        self.__resultsChecker.printResults("ACM0", self.__studentName)


pygame.init()
size = (600,400)
bg_color = (4,118,217)
title_bg_color = (4,66,191)
text_color = (242,195,167)


autograder_theme = pygame_menu.themes.Theme(background_color=bg_color, title_background_color=title_bg_color, widget_font_color=text_color, title_font=pygame_menu.font.FONT_PT_SERIF, widget_font=pygame_menu.font.FONT_HELVETICA, selection_color=text_color)

surface = pygame.display.set_mode((780, 540), pygame.RESIZABLE)
menu = pygame_menu.Menu('Autograder Menu Selection', 780, 540,theme=autograder_theme)

mainMenu = Menu()
menu.add.button('New Student', mainMenu.updateStudent)
menu.add.button('Upload answer key', mainMenu.updateAnswerKey)
menu.add.button('Upload student answers', mainMenu.updateStudentAnswers)
menu.add.button('Grade with guess correction', mainMenu.gradeGuessCorrection)
menu.add.button('Grade with normal correction', mainMenu.gradeNormalCorrection)
menu.add.button('Print Scores', mainMenu.printScore)
menu.add.button('Exit', pygame_menu.events.EXIT)
menu.mainloop(surface)