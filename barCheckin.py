import PySimpleGUI as sg
from datetime import date, datetime
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import pandas as pd
from time import sleep

from idInfo import *


sg.theme('DarkAmber')
baseLayout = [
    # [sg.Text('Scan an id into the box below:', key='firstLine')],
    [sg.Text('Welcome to Bar Checkin.')],
    [sg.Button('Check in  Juice')]
    [sg.Button('Check out Juice')]]

window = sg.Window('Party-List-Scanner',baseLayout,finalize=True)

while true:
    timeout = 5
    event, values = window.read(timeout=timeout)
    if event in [sg.WIN_CLOSED]:
        break 
    if event == 'Check in  Juice':
        # Open window to check in alc
        openCheckInWindow()
    if event == 'Check out Juice':
        # Open window to check out alc
        openCheckOutWindow()


def openCheckInWindow(self):
    inLayout = [
        [sg.Text('Check In Some Juice')],
        [sg.Text('ID Barcode:'), sg.Multiline(key="Id-Values", auto_size_text=True), sg.Button('Submit_Code', visible=True)],
        [sg.Text('Or enter name here:'),sg.InputText(key='inputName')],
        [sg.Text('Description of Item:'),sg.InputText(key='inputDesc')],
        [sg.Button('Check In')]]
    windowIn = sg.Window('Check-In', inLayout, finalize=True)
    while true:
        timeout = 5
        event, values = window.read(timeout=timeout)
        if event in [sg.WIN_CLOSED]:
            break
        if event == 'Check In':
            fn = ''
            ln = ''
            if values['Id-Values'] != '':
                try:
                    fn, ln, bd = idInfo.parseID(inputBarcode)
                except:
                    sg.popup_error('Error scanning, please type name or try again.')
            else:
                if values['inputName'] != '':
                    fn, ln = values['inputName'].split(' ')[0]
            
            if fn == '' or ln == '':
                sg.popup_error('No name entered or id scanned.')
            else:
                loc = checkin(fn,ln,desc)
                sg.popup('Please ')


        



def openCheckOutWindow(self):
    outLayout = [
        [sg.Text('Check Out Some Juice')],
        [sg.Text('ID Barcode:'), sg.Multiline(key="Id-Values", auto_size_text=True), sg.Button('Submit_Code', visible=True)],
        [sg.Text('Or enter name here:'),sg.InputText(key='inputName')],
        [sg.Button('Check Out')]
    ]

barMap = {
    'A':'',
    'B':'',
    'C':'',
    'D':'',
    'E':'',
    'F':'',
    'G':'',
    'H':'',    
    'I':'',
    'J':'',
    'K':'',
    'L':''
}
def checkin(fn, ln, desc):
    for key in barMap.keys():
        if barMap[key] == '':
            barMap[key] = [fn,ln,desc]
            return key
    
        