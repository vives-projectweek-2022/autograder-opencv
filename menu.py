from numpy import size
import pygame
import pygame_menu
import cv2
from final_sorter import Sorter
from results_check import ResultsChecker
from printer import printer
from machinevision import MachineVision
import numpy as np

machinevision = MachineVision()

teacherBlobs = null
teacherCircles = null
studentBlobs = null
studentCircles = null

answerKey = null
studentAnswers = null
studentName = ""
grade = null

def updateStudent():
    pass
    #studentName = menu.add.text_input

def updateAnswerKey():
    machineVision.getResults()
    teacherCircles = machineVision.getCirlces() 
    teacherBlobs = machineVision.getBlobs()
    answerKey = Sorter(teacherCircles, teacherBlobs)

def updateStudentAnswers():
    machineVision.getResults()
    studentCircles = machineVision.getCirlces()
    studentBlobs = machineVision.getBlobs()
    studentAnswers = Sorter(studentCircles, studentBlobs)

def grade():



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
menu.add.button('Grade!', grade)
menu.add.button('Print Scores', )
menu.add.button('Exit', pygame_menu.events.EXIT)
menu.mainloop(surface)