import PySimpleGUI as sg
from datetime import date

idPrefixes = {
    "DAA":"Full Name",    "DAB":"Family Name",    "DAC":"Given Name",    "DAD":"Middle Name",    "DAE":"Name Suffix",    "DAF":"Name Prefix",    "DAG":"Mailing Street Address1",    "DAH":"Mailing Street Address2",    "DAI":"Mailing City",    "DAJ":"Mailing Jurisdiction Code",    "DAK":"Mailing Postal Code",    "DAL":"Residence Street Address1",    "DAM":"Residence Street Address2",    "DAN":"Residence City",    "DAO":"Residence Jurisdiction Code",    "DAP":"Residence Postal Code",    "DAQ":"License or ID Number",    "DAR":"License Classification Code",    "DAS":"License Restriction Code",    "DAT":"License Endorsements Code",    "DAU":"Height in FT_IN",    "DAV":"Height in CM",    "DAW":"Weight in LBS",    "DAX":"Weight in KG",    "DAY":"Eye Color",    "DAZ":"Hair Color",    "DBA":"License Expiration Date",    "DBB":"Date of Birth",    "DBC":"Sex",    "DBD":"License or ID Document Issue Date",    "DBE":"Issue Timestamp",    "DBF":"Number of Duplicates",    "DBG":"Medical Indicator Codes",    "DBH":"Organ Donor",    "DBI":"Non-Resident Indicator",    "DBJ":"Unique Customer Identifier",    "DBK":"Social Security Number",    "DBL":"Date Of Birth",    "DBM":"Social Security Number",    "DBN":"Full Name",    "DBO":"Family Name",    "DBP":"Given Name",    "DBQ":"Middle Name or Initial",    "DBR":"Suffix",    "DBS":"Prefix",    "DCA":"Virginia Specific Class",    "DCB":"Virginia Specific Restrictions",    "DCD":"Virginia Specific Endorsements",    "DCE":"Physical Description Weight Range",    "DCF":"Document Discriminator",    "DCG":"Country territory of issuance",    "DCH":"Federal Commercial Vehicle Codes",    "DCI":"Place of birth",    "DCJ":"Audit information",    "DCK":"Inventory Control Number",    "DCL":"Race Ethnicity",    "DCM":"Standard vehicle classification",    "DCN":"Standard endorsement code",    "DCO":"Standard restriction code",    "DCP":"Jurisdiction specific vehicle classification description",    "DCQ":"Jurisdiction-specific",    "DCR":"Jurisdiction specific restriction code description",    "DCS":"Last Name",    "DCT":"First Name",    "DCU":"Suffix",    "DDA":"Compliance Type",    "DDB":"Card Revision Date",    "DDC":"HazMat Endorsement Expiry Date",    "DDD":"Limited Duration Document Indicator",    "DDE":"Family Name Truncation",    "DDF":"First Names Truncation",    "DDG":"Middle Names Truncation",    "DDH":"Under 18 Until",    "DDI":"Under 19 Until",    "DDJ":"Under 21 Until",    "DDK":"Organ Donor Indicator",    "DDL":"Veteran Indicator",    "PAA":"Permit Classification Code",    "PAB":"Permit Expiration Date",    "PAC":"Permit Identifier",    "PAD":"Permit IssueDate",    "PAE":"Permit Restriction Code",    "PAF":"Permit Endorsement Code",    "ZVA":"Court Restriction Code"}

partyList = ''
outputList = ''
today = date.today()


def parseID(value: str, prefixMap):
    perInfo = {}
    lines = value.split('\n')
    # k = 0
    for line in lines:
        if line[0:3] in prefixMap.keys():
            perInfo[prefixMap[line[0:3]]]=line[3:]
        # print('{} - {}'.format(k,line))
        # k+=1
    print(perInfo)
    return perInfo

def openInfoWindow(userInfo, partyList): 
    if 'Date of Birth' in userInfo.keys():   
        birthday = userInfo['Date of Birth']
    else:
        birthday = '01012022' # TEST DATE
    birthdate = date(int(birthday[4:9]), int(birthday[0:2]), int(birthday[2:4]))
    age = today.year - birthdate.year - ((today.month,today.day)<(birthdate.month, birthdate.day))
    is21 = (age>=21)

    infoLayout = [[sg.Text('NOT BLACKBALLED')],[sg.Text('Is On the List')],[sg.Text('Is over 21? {}'.format(is21),size=(30,5), background_color=('#06FF05' if (age>=21) else '#FF5733')  )]]
    # infoWin = sg.Window('Information on {}'.format(userInfo['First Name']), infoLayout, modal=True)
    infoWin = sg.Window('Information on {}'.format('bla'), infoLayout, modal=True)

    while True:
        event, values = infoWin.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    
    infoWin.close

sg.theme('DarkAmber')

baseLayout = [
    [sg.Text('Scan an id into the box below:', key='firstLine')],
    [sg.Text('ID Barcode:'), sg.InputText(key="Id-Values", enable_events=True), sg.Button('Submit', visible=False,  bind_return_key=True)],
    [sg.Button('Set Party List'), sg.Button('Set Output of Adds')]
]

window = sg.Window('Party-List-Scanner',baseLayout,finalize=True)

while True:
    event, values = window.read()
    if event in [sg.WIN_CLOSED]:
        break 
    elif event == 'Submit':
        inputValue = values['Id-Values']
        # Search for data on value
        parsedInput = parseID(inputValue, idPrefixes)
        openInfoWindow(parsedInput, partyList)

        window['Id-Values'].update('')


window.close()