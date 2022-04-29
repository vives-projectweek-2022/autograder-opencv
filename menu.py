from numpy import size
import pygame
import pygame_menu
import cv2
from final_sorter import Sorter
from results_check import ResultsChecker
from printer import printer
from machinevision import MachineVision
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
        self.__machinevision = MachineVision()
        self.__resultsChecker = ResultsChecker(self.__answerKey, self.__studentAnswers)

    def updateStudent():
        self.resetScore()
        #studentName = menu.add.text_input

    def updateAnswerKey():
        self.__machineVision.getResults()
        self.__teacherCircles = self.__machineVision.getCirlces() 
        self.__teacherBlobs = self.__machineVision.getBlobs()
        self.__answerKey = Sorter(self.__teacherCircles, self.__teacherBlobs)

    def updateStudentAnswers():
        self.__machineVision.getResults()
        self.__studentCircles = self.__machineVision.getCirlces()
        self.__studentBlobs = self.__machineVision.getBlobs()
        self.__studentAnswers = Sorter(self.__studentCircles, self.__studentBlobs)

    def gradeGuessCorrection():
        self.__grade = self.__resultsChecker.correctWithGuessCorrection()

    def gradeNormalCorrection():
        self.__grade = self.__resultsChecker.correctNormal()

    def resetScore():
        self.__grade = 0

    def printScore():
        self.__resultsChecker.printResults("ACM0", self.__studentName)

    cap = cv2.VideoCapture(0) 
    pygame.init()
    size = (600,400)

    surface = pygame.display.set_mode((780, 540), pygame.RESIZABLE)
    menu = pygame_menu.Menu('Welcome', 780, 540,theme=pygame_menu.themes.THEME_SOLARIZED)

    def video():
        while (True):
            _, frame = cap.read()
            cv2.imshow('frame', frame)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break

    menu.add.button('Camera', video)
    menu.add.button('New Student', updateStudent)
    menu.add.button('Upload answer key', updateAnswerKey)
    menu.add.button('Upload student answers', updateStudentAnswers)
    menu.add.button('Grade with guess correction', gradeGuessCorrection)
    menu.add.button('Grade with normal correction', gradeNormalCorrection)
    menu.add.button('Print Scores', printScore)
    menu.add.button('Exit', pygame_menu.events.EXIT)
    menu.mainloop(surface)