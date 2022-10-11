# Must install PySimpleGUI, tkinter, pywinusb, pyinstaller (for exe creation)

import PySimpleGUI as sg
from datetime import date
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import pandas as pd
from time import sleep

from threading import current_thread

import pywinusb.hid as hid


# Information about the specific scanner brand (to limit which USB device is attached to the app)
scannerVID = 0x1fca
scannerPID = 0x5aa8

class CardReadException(Exception):
    pass

class ScannerNotFound(Exception):
    pass


idPrefixes = {
    # "DAA":"Full Name",    "DAB":"Family Name",    "DAC":"Given Name",    "DAD":"Middle Name",    "DAE":"Name Suffix",    "DAF":"Name Prefix",    "DAG":"Mailing Street Address1",    "DAH":"Mailing Street Address2",    "DAI":"Mailing City",    "DAJ":"Mailing Jurisdiction Code",    "DAK":"Mailing Postal Code",    "DAL":"Residence Street Address1",    "DAM":"Residence Street Address2",    "DAN":"Residence City",    "DAO":"Residence Jurisdiction Code",    "DAP":"Residence Postal Code",    "DAQ":"License or ID Number",    "DAR":"License Classification Code",    "DAS":"License Restriction Code",    "DAT":"License Endorsements Code",    "DAU":"Height in FT_IN",    "DAV":"Height in CM",    "DAW":"Weight in LBS",    "DAX":"Weight in KG",    "DAY":"Eye Color",    "DAZ":"Hair Color",    "DBA":"License Expiration Date",    "DBB":"Date of Birth",    "DBC":"Sex",    "DBD":"License or ID Document Issue Date",    "DBE":"Issue Timestamp",    "DBF":"Number of Duplicates",    "DBG":"Medical Indicator Codes",    "DBH":"Organ Donor",    "DBI":"Non-Resident Indicator",    "DBJ":"Unique Customer Identifier",    "DBK":"Social Security Number",    "DBL":"Date Of Birth",    "DBM":"Social Security Number",    "DBN":"Full Name",    "DBO":"Family Name",    "DBP":"Given Name",    "DBQ":"Middle Name or Initial",    "DBR":"Suffix",    "DBS":"Prefix",    "DCA":"Virginia Specific Class",    "DCB":"Virginia Specific Restrictions",    "DCD":"Virginia Specific Endorsements",    "DCE":"Physical Description Weight Range",    "DCF":"Document Discriminator",    "DCG":"Country territory of issuance",    "DCH":"Federal Commercial Vehicle Codes",    "DCI":"Place of birth",    "DCJ":"Audit information",    "DCK":"Inventory Control Number",    "DCL":"Race Ethnicity",    "DCM":"Standard vehicle classification",    "DCN":"Standard endorsement code",    "DCO":"Standard restriction code",    "DCP":"Jurisdiction specific vehicle classification description",    "DCQ":"Jurisdiction-specific",    "DCR":"Jurisdiction specific restriction code description",    "DCS":"Last Name",    "DCT":"Given Name",    "DCU":"Suffix",   "DDB":"Card Revision Date",    "DDC":"HazMat Endorsement Expiry Date",  "DDE":"Family Name Truncation",    "DDF":"First Names Truncation",    "DDG":"Middle Names Truncation",    "DDH":"Under 18 Until",    "DDI":"Under 19 Until",    "DDJ":"Under 21 Until",    "DDK":"Organ Donor Indicator",    "DDL":"Veteran Indicator",    "PAA":"Permit Classification Code",    "PAB":"Permit Expiration Date",    "PAC":"Permit Identifier",    "PAD":"Permit IssueDate",    "PAE":"Permit Restriction Code",    "PAF":"Permit Endorsement Code",    "ZVA":"Court Restriction Code"}
    "DAA":"Full Name",    "DAB":"Family Name",    "DAC":"Given Name",    "DAD":"Middle Name",    "DAE":"Name Suffix",    "DAF":"Name Prefix",    "DAG":"Mailing Street Address1",    "DAH":"Mailing Street Address2",    "DAI":"Mailing City",    "DAJ":"Mailing Jurisdiction Code",    "DAK":"Mailing Postal Code",    "DAL":"Residence Street Address1",    "DAM":"Residence Street Address2",    "DAN":"Residence City",    "DAO":"Residence Jurisdiction Code",    "DAP":"Residence Postal Code",    "DAQ":"License or ID Number",    "DAR":"License Classification Code",    "DAS":"License Restriction Code",    "DAT":"License Endorsements Code",    "DAU":"Height in FT_IN",    "DAV":"Height in CM",    "DAW":"Weight in LBS",    "DAX":"Weight in KG",    "DAY":"Eye Color",    "DAZ":"Hair Color",    "DBA":"License Expiration Date",    "DBB":"Date of Birth",    "DBC":"Sex",    "DBD":"License or ID Document Issue Date",    "DBE":"Issue Timestamp",    "DBF":"Number of Duplicates",    "DBG":"Medical Indicator Codes",    "DBH":"Organ Donor",    "DBI":"Non-Resident Indicator",    "DBJ":"Unique Customer Identifier",    "DBK":"Social Security Number",    "DBL":"Date Of Birth",    "DBM":"Social Security Number",    "DBN":"Full Name",    "DBO":"Family Name",    "DBP":"Given Name",    "DBQ":"Middle Name or Initial",    "DBR":"Suffix",    "DBS":"Prefix",    "DCA":"Virginia Specific Class",    "DCB":"Virginia Specific Restrictions",    "DCD":"Virginia Specific Endorsements",    "DCE":"Physical Description Weight Range",    "DCF":"Document Discriminator",    "DCG":"Country territory of issuance",    "DCH":"Federal Commercial Vehicle Codes",    "DCI":"Place of birth",    "DCJ":"Audit information",    "DCK":"Inventory Control Number",    "DCL":"Race Ethnicity",    "DCM":"Standard vehicle classification",    "DCN":"Standard endorsement code",    "DCO":"Standard restriction code",    "DCP":"Jurisdiction specific vehicle classification description",    "DCQ":"Jurisdiction-specific",    "DCR":"Jurisdiction specific restriction code description",    "DCS":"Last Name",    "DCT":"Given Name",    "DCU":"Suffix",    "DDA":"Compliance Type",    "DDB":"Card Revision Date",    "DDC":"HazMat Endorsement Expiry Date",    "DDD":"Limited Duration Document Indicator",    "DDE":"Family Name Truncation",    "DDF":"First Names Truncation",    "DDG":"Middle Names Truncation",    "DDH":"Under 18 Until",    "DDI":"Under 19 Until",    "DDJ":"Under 21 Until",    "DDK":"Organ Donor Indicator",    "DDL":"Veteran Indicator",    "PAA":"Permit Classification Code",    "PAB":"Permit Expiration Date",    "PAC":"Permit Identifier",    "PAD":"Permit IssueDate",    "PAE":"Permit Restriction Code",    "PAF":"Permit Endorsement Code",    "ZVA":"Court Restriction Code"}


#
# Load party list
#   returns dataframe with partyList contents
#
def loadPartyList(path):
    values = pd.read_excel(path)
    values.drop('Unnamed: 1', axis=1) # unused row between List/Blackball
    return values

#
# Parse id by using the prefixMap
#
def parseID(value: str, prefixMap=idPrefixes):
    perInfo = {}
    alreadySeen = set()
    lines = value.split('\n')
    for line in lines:
        if line[0:3] in prefixMap.keys():
            perInfo[prefixMap[line[0:3]]]=line[3:]
    return perInfo

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
def openInfoWindow(userInfo, partyListValues): 
    if 'Date of Birth' in userInfo.keys():   
        birthday = userInfo['Date of Birth']
    else:
        raise CardReadException('Could not find birthday in information.')
    
    birthdate = date(int(birthday[4:9]), int(birthday[0:2]), int(birthday[2:4]))
    age = today.year - birthdate.year - ((today.month,today.day)<(birthdate.month, birthdate.day))
    is21 = (age>=21)

    fName = ''
    lName = ''
    if 'Last Name' in userInfo.keys():
        lName = userInfo['Last Name'].split(',')[0].lower() # take the first if it is a list
    else:
        raise CardReadException('Could not find last name in information.')
    if 'Given Name' in userInfo.keys():
        fName = userInfo['Given Name'].split(',')[0].lower() # take the first if it is a list
    else:
        raise CardReadException('Could not find first name in information.')

    print('Looking for:',fName,lName)
    print('Birthday: '+birthdate.strftime('%m/%d/%Y'))

    onList, blackball = isOnList(fName, lName, partyListValues)
    is21Color = 'orange'
    is18Color = 'green'
    notAllowedColor = 'red'
    wristbandColor = is21Color if (age>=21) else (is18Color if (age>=18) else notAllowedColor)

    infoLayout = [[sg.Text('NOT BLACKBALLED' if not blackball else 'BLACKBALLED', size=(30,5), background_color=('green' if not blackball else 'red'), text_color='black')],
                  [sg.Text('On List!' if onList else 'Not on List', size=(30,5), background_color=('green' if onList else 'red'), text_color='black')],
                  [sg.Text('Is {}'.format(str(age)),size=(30,5), background_color=(wristbandColor), text_color='black')]]
    ### TODO: Could possibly add a check-in button, that logs when people checked in.
   
    if not onList and not blackball:
        infoLayout.append([sg.Button('Add To List')])
   
    infoWin = sg.Window('Information on {} {}'.format(fName, lName), infoLayout, modal=True)

    while True:
        event, values = infoWin.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Add To List':
            outputFile.write(fName+' '+lName+'\n')
            print('adding to the list: ',fName+' '+lName)
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
        inputVal = ''.join(chr(i) for i in builtMessage)
        # print(inputVal)
        global info
        info = parseID(inputVal, idPrefixes)
        global openInfoWindowNext
        openInfoWindowNext = True

filter = hid.HidDeviceFilter(vendor_id = scannerVID, product_id = scannerPID)
devices = filter.get_devices()
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
    [sg.Text('Scan an id into the box below:', key='firstLine')],
    [sg.Text('Scan ID to Continue')],
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
        openInfoWindow(info, partyListValues)
        openInfoWindowNext = False
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