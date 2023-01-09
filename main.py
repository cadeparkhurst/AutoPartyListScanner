# Must install PySimpleGUI, tkinter, pywinusb, fuzzywuzzy, python
#  pyinstaller (for exe creation)

import PySimpleGUI as sg
from datetime import date, datetime
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import pandas as pd
from time import sleep

from fuzzywuzzy import fuzz

# # Used for USB POS 
# from threading import current_thread
# import pywinusb.hid as hid

from idInfo import *

idInfo = idInformation()

# Information about the specific scanner brand (to limit which USB device is attached to the app)
# scannerVID = 0x1fca
# scannerPID = 0x5aa8

# class ScannerNotFound(Exception):
#     pass


partyList = './Lists/Halloween Party List.xlsx'
addLog = './Logs/adds.txt'
checkInLog = './Logs/checkinList.txt'
addFile = open(addLog, 'a+')
addFile.write('----------------{}----------------\n'.format(datetime.now()))
checkInFile = open(checkInLog, 'a+')
checkInFile.write('----------------{}----------------\n'.format(datetime.now()))

today = date.today()


#
# Load party list
#   returns dataframe with partyList contents
#
LIST_NAMES = 'List'
BLACKBALL = "Blackball"

def loadPartyList(path):
    values = pd.read_excel(path)
    print(values.keys)
    values[LIST_NAMES] = values[LIST_NAMES].str.lower()
    # values.drop('Unnamed: 1', axis=1) # unused row between List/Blackball
    return values


partyListValues = loadPartyList(partyList)


#
# Check if person is on the list
# ** TODO: Implement Fuzzy checking here
# returns onList?, isBlackballed?
#
def isOnList(fName, lName, partyListValues):
    onList = False
    blackballed=False
    name = (fName.lower() + ' ' +lName.lower())
    ## Brute Search
    if (name == partyListValues[LIST_NAMES].str.lower()).any():
        onList = True
    if (name == partyListValues[BLACKBALL].str.lower()).any():
        blackballed = True

    if not (onList or blackballed):
        ## Fuzzy Searchh
        print("Make fuzzy search work later")
        # print(partyListValues[LIST_NAMES].map(lambda x:fuzz.ratio(x,name)))
        # if (partyListValues[LIST_NAMES].map(lambda x:fuzz.ratio(x,name)>80)).any():
        #     onList = True
        # if (name == partyListValues[BLACKBALL].str.lower()).any():
        #     blackballed = True


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
        age = -1

    print('Looking for:',firstName, lastName)
    if not birthdate is None: print('Birthday: '+birthdate.strftime('%m/%d/%Y'))

    onList, blackball = isOnList(firstName, lastName, partyListValues)
    is21Color = 'orange'
    is18Color = 'green'
    notAllowedColor = 'red'
    wristbandColor = is21Color if (age>=21) else (is18Color if (age>=18) else notAllowedColor)

    infoLayout = [[sg.Text('Info for {} {}, they are {} years old.'.format(firstName, lastName, age))],
                  [sg.Text('NOT BLACKBALLED' if not blackball else 'BLACKBALLED', size=(30,5), background_color=('green' if not blackball else 'red'), text_color='black')],
                  [sg.Text('On List!' if onList else 'Not on List', size=(30,5), background_color=('green' if onList else 'red'), text_color='black')],
                  [sg.Text('Is {}'.format(str(age)) if not birthdate is None else 'Manually Check',size=(30,5), background_color=(wristbandColor), text_color='black')]]
    ### TODO: Could possibly add a check-in button, that logs when people checked in.
   
    if not onList and not blackball:
        infoLayout.append([sg.Button('Add To List')])
   
    infoWin = sg.Window('Information on {} {}'.format(firstName, lastName), infoLayout, modal=True)

    while True:
        event, values = infoWin.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            checkInFile.write('{} {}, was {}on the list, is {}over 21\n'.format(firstName, lastName, 'not ' if not onList else '', 'not ' if not is21 else ''))
            break
        if event == 'Add To List':
            print('adding to the list: ',firstName+' '+lastName)
            addFile.write('{} {} \n'.format(firstName, lastName))
            break
    infoWin.close()


#################################################################################
#
# Set up stuff for the scanner
#
# builtMessage = []
# openInfoWindowNext = False
# info = {}

# def buildCompleteMessage(data): # Method for on scan
#     data = data[5:] # Remove USB header
#     global builtMessage
#     builtMessage.extend(data[:-3]) #add all but USB footer
#     if data[-1] == 0:
#         #Message is complete
#         # print(builtMessage)
#         global openInfoWindowNext
#         openInfoWindowNext = True

# filter = hid.HidDeviceFilter(vendor_id = scannerVID, product_id = scannerPID)
# devices = filter.get_devices()
# if len(devices) == 0:
#     raise ScannerNotFound('Could not find scanner, possibly it is not plugged in.')
# scanner = devices[0]
# scanner.open()
# scanner.set_raw_data_handler(buildCompleteMessage)

################################################################################



# Build the main window and run the loop.
sg.theme('DarkAmber')
baseLayout = [
    # [sg.Text('Scan an id into the box below:', key='firstLine')],
    [sg.Text('Welcome to Id Scanner, using the following list: "{}"'.format(partyList), key='--Title--')],
    [sg.Text('Scan ID to Continue')],
    # [sg.Text('ID Barcode:'), sg.InputText(key="Id-Values", enable_events=False), sg.Button('Submit_Code', visible=True,  bind_return_key=False)],
    [sg.Text('ID Barcode:'), sg.Multiline(key="Id-Values", auto_size_text=True), sg.Button('Submit_Code', visible=True)],
    [sg.Text('Or enter name here:'),sg.InputText(key='inputName'), sg.Button('Submit')],
    # [sg.Button('Set Party List'), sg.Button('Set Output of Adds')]]
    [sg.Button('Set Party List')]]

window = sg.Window('Party-List-Scanner',baseLayout,finalize=True)
## Scanner may send Ctrl + J instead of an enter, but we need it to act like an enter (same control code)
# Add an interrupt event that inserts an enter
# May run into timing issues? but seems to work for now.
window.bind("<Control-j>","ENTER")
window.bind("<Control-J>","ENTER")

# Old Scanner Presses Down stead of Enter
window.bind("<Down>","ENTER")


window.bind("<Return>","Pressed_Enter")

Tk().withdraw()

enterCount=0
runOpenInfo=False

while True:
    timeout = 5
    event, values = window.read(timeout=timeout)
    if event in [sg.WIN_CLOSED]:
        break 
    # if openInfoWindowNext:
    #     # print(builtMessage)
    #     inputVal = ''.join(chr(i) for i in builtMessage)
    #     # print('Input:', inputVal)
    #     try:
    #         fn, ln, bd = idInfo.parseID(inputVal)
    #     except CardReadException:
    #         print('Could not scan card correctly')
    #         openInfoWindowNext = False
    #         builtMessage = []
    #         continue
    #     openInfoWindow(fn, ln, bd, partyListValues)
    #     openInfoWindowNext = False
    #     builtMessage = []
    elif event == 'ENTER':
        window['Id-Values'](values['Id-Values'] + '\n')
    elif event == 'Pressed_Enter' and window.FindElementWithFocus() == window['Id-Values']: ## Only count returns when typing in the id scanner area
        enterCount+=1
        # print(enterCount)
        if enterCount==4:
            runOpenInfo=True
            inputBarcode = values['Id-Values']
            # window.write_event_value('Submit_Code','')
            window['Id-Values']('')
            enterCount=0
    elif event == 'Submit_Code':
        inputBarcode = values['Id-Values']
        runOpenInfo=True
        window['Id-Values']('')
    elif event == 'Submit':
        #Split first and last name
        inputName = values['inputName']
        f = inputName.split(' ')[0]
        l = inputName.split(' ')[1]
        # print('Looking for {},{}'.format(f,l))
        openInfoWindow(f, l, None, partyListValues)
        window['inputName']('')
    elif event == 'Set Party List':
        inp = askopenfilename()
        if inp != '':
            partyList = inp
            partyListValues = loadPartyList(partyList)  
            window['--Title--']('Welcome to Id Scanner, using the following list: "{}"'.format(partyList))


    if runOpenInfo:
        try:
            fn, ln, bd = idInfo.parseID(inputBarcode)
            openInfoWindow(fn,ln,bd,partyListValues)
        except CardReadException:
            print('Could not scan card properly')
            print('Please manually check ID')
        runOpenInfo=False

# scanner.close()
addFile.close()
checkInFile.close()
window.close()