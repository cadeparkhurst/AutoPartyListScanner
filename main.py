# Must install PySimpleGUI, tkinter, pywinusb, pyinstaller (for exe creation)

import PySimpleGUI as sg
from datetime import date
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import pandas as pd
from time import sleep

# Used for USB POS 
from threading import current_thread
import pywinusb.hid as hid

from idInfo import *

idInfo = idInformation()


# Information about the specific scanner brand (to limit which USB device is attached to the app)
scannerVID = 0x1fca
scannerPID = 0x5aa8

class ScannerNotFound(Exception):
    pass

#
# Load party list
#   returns dataframe with partyList contents
#
def loadPartyList(path):
    values = pd.read_excel(path)
    values.drop('Unnamed: 1', axis=1) # unused row between List/Blackball
    return values

#
# Check if person is on the list
# ** TODO: Implement Fuzzy checking here
# returns onList?, isBlackballed?
#
def isOnList(fName, lName, partyListValues):
    onList = False
    blackballed=False
    name = (fName.lower() + ' ' +lName.lower())
    if (name == partyListValues.List.str.lower()).any():
        onList = True
    if (name == partyListValues.Blackball.str.lower()).any():
        blackballed = True
    return onList, blackballed

#
# Open the info window for a specific person
#
def openInfoWindow(firstName, lastName, birthdate, partyListValues): 
    #Calculate age
    if not birthdate is None:
        age = today.year - birthdate.year - ((today.month,today.day)<(birthdate.month, birthdate.day))
        is21 = (age>=21)
    else:
        is21 = False
        age = 0

    print('Looking for:',firstName, lastName)
    if not birthdate is None: print('Birthday: '+birthdate.strftime('%m/%d/%Y'))

    onList, blackball = isOnList(firstName, lastName, partyListValues)
    is21Color = 'orange'
    is18Color = 'green'
    notAllowedColor = 'red'
    wristbandColor = is21Color if (age>=21) else (is18Color if (age>=18) else notAllowedColor)

    infoLayout = [[sg.Text('NOT BLACKBALLED' if not blackball else 'BLACKBALLED', size=(30,5), background_color=('green' if not blackball else 'red'), text_color='black')],
                  [sg.Text('On List!' if onList else 'Not on List', size=(30,5), background_color=('green' if onList else 'red'), text_color='black')],
                  [sg.Text('Is {}'.format(str(age)) if not birthdate is None else 'Manually Check',size=(30,5), background_color=(wristbandColor), text_color='black')]]
    ### TODO: Could possibly add a check-in button, that logs when people checked in.
   
    if not onList and not blackball:
        infoLayout.append([sg.Button('Add To List')])
   
    infoWin = sg.Window('Information on {} {}'.format(firstName, lastName), infoLayout, modal=True)

    while True:
        event, values = infoWin.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Add To List':
            outputFile.write(firstName+' '+lastName+'\n')
            print('adding to the list: ',firstName+' '+lastName)
            break
    infoWin.close()


#################################################################################
#
# Set up stuff for the scanner
#
builtMessage = []
openInfoWindowNext = False
info = {}

def buildCompleteMessage(data): # Method for on scan
    data = data[5:] # Remove USB header
    global builtMessage
    builtMessage.extend(data[:-3]) #add all but USB footer
    if data[-1] == 0:
        #Message is complete
        # print(builtMessage)
        global openInfoWindowNext
        openInfoWindowNext = True

filter = hid.HidDeviceFilter(vendor_id = scannerVID, product_id = scannerPID)
devices = filter.get_devices()
if len(devices) == 0:
    raise ScannerNotFound('Could not find scanner, possibly it is not plugged in.')
scanner = devices[0]
scanner.open()
scanner.set_raw_data_handler(buildCompleteMessage)

################################################################################

partyList = './Lists/Test.xlsx'
outputList = 'logs.txt'
outputFile = open(outputList, 'a')
today = date.today()
partyListValues = loadPartyList(partyList)


# Build the main window and run the loop.
sg.theme('DarkAmber')
baseLayout = [
    # [sg.Text('Scan an id into the box below:', key='firstLine')],
    [sg.Text('Scan ID to Continue')],
    [sg.Text('Or enter name here:'),sg.InputText(key='inputName'), sg.Button('Submit', bind_return_key=True)],
    # [sg.Text('ID Barcode:'), sg.InputText(key="Id-Values", enable_events=True), sg.Button('Submit', visible=False,  bind_return_key=True)],
    [sg.Button('Set Party List'), sg.Button('Set Output of Adds')]]

window = sg.Window('Party-List-Scanner',baseLayout,finalize=True)
Tk().withdraw()

while True:
    timeout = 5
    event, values = window.read(timeout=timeout)
    if event in [sg.WIN_CLOSED]:
        break 
    if openInfoWindowNext:
        # print(builtMessage)
        inputVal = ''.join(chr(i) for i in builtMessage)
        # print('Input:', inputVal)
        try:
            fn, ln, bd = idInfo.parseID(inputVal)
        except CardReadException:
            print('Could not scan card correctly')
            openInfoWindowNext = False
            builtMessage = []
            continue
        openInfoWindow(fn, ln, bd, partyListValues)
        openInfoWindowNext = False
        builtMessage = []
    elif event == 'Submit':
        #Split first and last name
        inputName = values['inputName']
        f = inputName.split(' ')[0]
        l = inputName.split(' ')[1]
        print('Looking for {},{}'.format(f,l))
        openInfoWindow(f, l, None, partyListValues)
        window['inputName']('')
    elif event == 'Set Party List':
        inp = askopenfilename()
        if inp != '':
            partyList = inp
            partyListValues = loadPartyList(partyList)  

    elif event == 'Set Output of Adds':
        inp = askopenfilename()
        if inp != '':
            outputFile.close()
            outputList = inp
            outputFile = open(outputList,'a')

scanner.close()
outputFile.close()
window.close()