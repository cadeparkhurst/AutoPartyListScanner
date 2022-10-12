from datetime import date

class CardReadException(Exception):
    pass

class idInformation():

    # idPrefixes = {
    #     # "DAA":"Full Name",    "DAB":"Family Name",    "DAC":"Given Name",    "DAD":"Middle Name",    "DAE":"Name Suffix",    "DAF":"Name Prefix",    "DAG":"Mailing Street Address1",    "DAH":"Mailing Street Address2",    "DAI":"Mailing City",    "DAJ":"Mailing Jurisdiction Code",    "DAK":"Mailing Postal Code",    "DAL":"Residence Street Address1",    "DAM":"Residence Street Address2",    "DAN":"Residence City",    "DAO":"Residence Jurisdiction Code",    "DAP":"Residence Postal Code",    "DAQ":"License or ID Number",    "DAR":"License Classification Code",    "DAS":"License Restriction Code",    "DAT":"License Endorsements Code",    "DAU":"Height in FT_IN",    "DAV":"Height in CM",    "DAW":"Weight in LBS",    "DAX":"Weight in KG",    "DAY":"Eye Color",    "DAZ":"Hair Color",    "DBA":"License Expiration Date",    "DBB":"Date of Birth",    "DBC":"Sex",    "DBD":"License or ID Document Issue Date",    "DBE":"Issue Timestamp",    "DBF":"Number of Duplicates",    "DBG":"Medical Indicator Codes",    "DBH":"Organ Donor",    "DBI":"Non-Resident Indicator",    "DBJ":"Unique Customer Identifier",    "DBK":"Social Security Number",    "DBL":"Date Of Birth",    "DBM":"Social Security Number",    "DBN":"Full Name",    "DBO":"Family Name",    "DBP":"Given Name",    "DBQ":"Middle Name or Initial",    "DBR":"Suffix",    "DBS":"Prefix",    "DCA":"Virginia Specific Class",    "DCB":"Virginia Specific Restrictions",    "DCD":"Virginia Specific Endorsements",    "DCE":"Physical Description Weight Range",    "DCF":"Document Discriminator",    "DCG":"Country territory of issuance",    "DCH":"Federal Commercial Vehicle Codes",    "DCI":"Place of birth",    "DCJ":"Audit information",    "DCK":"Inventory Control Number",    "DCL":"Race Ethnicity",    "DCM":"Standard vehicle classification",    "DCN":"Standard endorsement code",    "DCO":"Standard restriction code",    "DCP":"Jurisdiction specific vehicle classification description",    "DCQ":"Jurisdiction-specific",    "DCR":"Jurisdiction specific restriction code description",    "DCS":"Last Name",    "DCT":"Given Name",    "DCU":"Suffix",   "DDB":"Card Revision Date",    "DDC":"HazMat Endorsement Expiry Date",  "DDE":"Family Name Truncation",    "DDF":"First Names Truncation",    "DDG":"Middle Names Truncation",    "DDH":"Under 18 Until",    "DDI":"Under 19 Until",    "DDJ":"Under 21 Until",    "DDK":"Organ Donor Indicator",    "DDL":"Veteran Indicator",    "PAA":"Permit Classification Code",    "PAB":"Permit Expiration Date",    "PAC":"Permit Identifier",    "PAD":"Permit IssueDate",    "PAE":"Permit Restriction Code",    "PAF":"Permit Endorsement Code",    "ZVA":"Court Restriction Code"}
    #     "DAA":"Full Name",    "DAB":"Family Name",    "DAC":"Given Name",    "DAD":"Middle Name",    "DAE":"Name Suffix",    "DAF":"Name Prefix",    "DAG":"Mailing Street Address1",    "DAH":"Mailing Street Address2",    "DAI":"Mailing City",    "DAJ":"Mailing Jurisdiction Code",    "DAK":"Mailing Postal Code",    "DAL":"Residence Street Address1",    "DAM":"Residence Street Address2",    "DAN":"Residence City",    "DAO":"Residence Jurisdiction Code",    "DAP":"Residence Postal Code",    "DAQ":"License or ID Number",    "DAR":"License Classification Code",    "DAS":"License Restriction Code",    "DAT":"License Endorsements Code",    "DAU":"Height in FT_IN",    "DAV":"Height in CM",    "DAW":"Weight in LBS",    "DAX":"Weight in KG",    "DAY":"Eye Color",    "DAZ":"Hair Color",    "DBA":"License Expiration Date",    "DBB":"Date of Birth",    "DBC":"Sex",    "DBD":"License or ID Document Issue Date",    "DBE":"Issue Timestamp",    "DBF":"Number of Duplicates",    "DBG":"Medical Indicator Codes",    "DBH":"Organ Donor",    "DBI":"Non-Resident Indicator",    "DBJ":"Unique Customer Identifier",    "DBK":"Social Security Number",    "DBL":"Date Of Birth",    "DBM":"Social Security Number",    "DBN":"Full Name",    "DBO":"Family Name",    "DBP":"Given Name",    "DBQ":"Middle Name or Initial",    "DBR":"Suffix",    "DBS":"Prefix",    "DCA":"Virginia Specific Class",    "DCB":"Virginia Specific Restrictions",    "DCD":"Virginia Specific Endorsements",    "DCE":"Physical Description Weight Range",    "DCF":"Document Discriminator",    "DCG":"Country territory of issuance",    "DCH":"Federal Commercial Vehicle Codes",    "DCI":"Place of birth",    "DCJ":"Audit information",    "DCK":"Inventory Control Number",    "DCL":"Race Ethnicity",    "DCM":"Standard vehicle classification",    "DCN":"Standard endorsement code",    "DCO":"Standard restriction code",    "DCP":"Jurisdiction specific vehicle classification description",    "DCQ":"Jurisdiction-specific",    "DCR":"Jurisdiction specific restriction code description",    "DCS":"Last Name",    "DCT":"Given Name",    "DCU":"Suffix",    "DDA":"Compliance Type",    "DDB":"Card Revision Date",    "DDC":"HazMat Endorsement Expiry Date",    "DDD":"Limited Duration Document Indicator",    "DDE":"Family Name Truncation",    "DDF":"First Names Truncation",    "DDG":"Middle Names Truncation",    "DDH":"Under 18 Until",    "DDI":"Under 19 Until",    "DDJ":"Under 21 Until",    "DDK":"Organ Donor Indicator",    "DDL":"Veteran Indicator",    "PAA":"Permit Classification Code",    "PAB":"Permit Expiration Date",    "PAC":"Permit Identifier",    "PAD":"Permit IssueDate",    "PAE":"Permit Restriction Code",    "PAF":"Permit Endorsement Code",    "ZVA":"Court Restriction Code"}

    # TODO: Could remove unused ones (We don't need to know everything)
    aamva2020Prefixes = {
        "DCS":"Customer Family Name", #Last name
        "DAC":"Customer First Name", #First name
        "DAD":"Customer Middle Name(s)", #Comma Separated
        "DBB":"Date of Birth"
    }

    aamva2005Prefixes = {
        "DCS":"Customer Family Name",
        "DCT":"Customer Given Names", #Includes First and Middle
        "DBB":"Date of Birth"
    }

    aamva2003Prefixes = {
        "DCS":"Family Name",
        "DCT":"Given Name", #Includes first and middle
        "DAC":"First Name",
        "DBB":"Date of Birth"
    }

    aamva2000Prefixes = {
        "DAB":"Driver Last Name", #Optional
        "DAC":"Driver First Name", #Optional
        "DBB":"Date of Birth"
    }



    verToDict = {
        "10":[aamva2020Prefixes, 'Customer First Name', 'Customer Family Name', 'Date of Birth'],
        "09":[aamva2020Prefixes, 'Customer First Name', 'Customer Family Name', 'Date of Birth'],
        "03":[aamva2005Prefixes, 'Customer Given Names', 'Customer Family Name', 'Date of Birth'],
        "02":[aamva2003Prefixes, 'Family Name', 'First Name', 'Date of Birth'],
        "01":[aamva2000Prefixes, 'Driver First Name', 'Driver Last Name', 'Date of Birth']
    }

    #
    # Parse id by using the prefixMap
    #
    def parseID(self, value: str):
        perInfo = {}
        if not value[0] == '@':
            raise CardReadException('Not valid ')
        lines = value.split('\n')
        versionSpecs = self._getKeyMapFromVersion(lines[1])
        prefixMap = versionSpecs[0]
        for line in lines:
            if line[0:3] in prefixMap.keys():
                perInfo[prefixMap[line[0:3]]]=line[3:]
        
        if not versionSpecs[1] in perInfo.keys():
            raise CardReadException("Couldn't find first name.")
        if not versionSpecs[2] in perInfo.keys():
            raise CardReadException("Couldn't find last name.")
        if not versionSpecs[3] in perInfo.keys():
            raise CardReadException("Couldn't find birthday.")

        dateString = perInfo[versionSpecs[3]]
        birthdate = date(int(dateString[4:9]), int(dateString[0:2]), int(dateString[2:4]))

        return perInfo[versionSpecs[1]].split(',')[0].split(' ')[0], perInfo[versionSpecs[2]], birthdate
    

    def _getKeyMapFromVersion(self, infoLine: str):
        amountToSkip = 13
        lengthOfVer = 2
        ver = ''.join(infoLine[amountToSkip:amountToSkip+lengthOfVer])
        # print(ver)
        l = self.verToDict.get(ver)
        if l is None:
            return [self.aamva2020Prefixes, 'Customer First Name', 'Customer Family Name', 'Date of Birth']
            # raise CardReadException('Unsupported AAMVA Version {}'.format(ver))
        else:
            return l