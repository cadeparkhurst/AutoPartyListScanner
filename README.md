# AutoPartyListScanner
Scans barcodes on ID's to check if they are on the party list and verify their age

## Background Information
Driver information is encoded using PDF417. This is a well known 2d barcode standard.

## Example Use Case
1. Open's app and points it to the "list" for the current party.
2. Select scan/input area
3. Scan card, which pastes encoded information (as if scanner was a keyboard) into the input area.
4. Return if they are (on list/not on list/blackballed), and if they are over 18, over 21.
5. If not on the list, have option to add them to the list (main use case for girls)
6. Mark down if they were admitted to the party

Other cases?
1. Search for guests by brother who added them to the list

Potential Problems
1. Not all states enforce all information is on card.
    - Should have back up way to manually search, through app or directly on list
2. Integrate directly with google sheets?
    - Google Sheets for Developers > sheets API