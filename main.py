#!
__author__ = __author__ = [  'agentnola', 'chrispytoast123', 'jb567', 'electric-blue', 'rexrex600' ]
import gspread
import json
import praw
import re
from oauth2client.client import SignedJwtAssertionCredentials
import concurrent.futures
import getpass
import time

##  INITIALISATION OF PROGRAM AND ERROR CHECKING FUNCTIONS

#   Error checking functions

def checkURL():
    print('Copy Voting Thread Link Below')
    URL = str(input())
    return URL

def login():
    user = str(input('Reddit Username:'))
    try:
        r.login(user,getpass.getpass('Reddit Password:'))
    except praw.errors.InvalidUserPass:
        print ("Incorrect Password")
        login()

#   Variables

sheetName = '10th Govt Voting Record'
already_done = []
done_voters = []
dupes = []
docName = 'Slave Sheet'
docKey = 'DriveAPI-8b5effde4bd4.json'

#   Loads the JSON Key, which is provided seperately
json_key = json.load(open(docKey))
scope = ['https://spreadsheets.google.com/feeds']
#   Initilises all the credentials, and GoogleSheet stuff
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
r = praw.Reddit('MHOC-plebian house, vote counter v1')
gc = gspread.authorize(credentials)
sh = gc.open(docName)
wks = sh.worksheet(sheetName)
#   User Input for Reddit/ Reddit information
login()
rThread = checkURL()

strt = time.time()



##  FUNCTION DEFINITIONS

def findLastMP(wksColumn):
    wksCellList = wks.col_values(wksColumn)
    for wksCell in wksCellList:
        if wksCell == "Speaker":
            return wks.find(wksCell).row

def getMPs():
    col = getCol()
    wksMPs = wks.col_values(3)[2:findLastMP(4)-1]
    wksMPIsSitting = wks.col_values(col)[2:findLastMP(4)-1]
    for i in wksMPs:
        if wksMPIsSitting[wksMPs.index(i)] == 'N/A':
            del wksMPIsSitting[wksMPs.index(i)]
            wksMPs.remove(i)
    return wksMPs

def getVotes(url):
    #getting the list of comments
    rThread = r.get_submission(url)
    rThread.replace_more_comments(limit=None, threshold=0)
    rComments = praw.helpers.flatten_tree(rThread.comments)
    #returning the list of comments
    return rComments

def getCol():
    cells = wks.range('F3:BZ3')
    for cell in cells:
        if cell.value == '':
            col = cell.col
            break
    return col

def getUpdateCells(MPs):
    col = getCol()
    updateList = wks.range(str(wks.get_addr_int(3, col)) + ":" + wks.get_addr_int(findLastMP(4)-1, col))
    wksMPIsSitting = wks.col_values(col)[2:findLastMP(4)-1]
    for i in updateList:
        if wksMPIsSitting[updateList.index(i)] == 'N/A':
            del wksMPIsSitting[updateList.index(i)]
            updateList.remove(i)
    return updateList

def titleCol():
    #setting up the spreadsheet for the count
    col = getCol()
    title = str(rThread.title())
    billNum = title.split("/")[-2]
    billNum = billNum.split("_")[0]
    print("You are counting " + billNum)
    wks.update_cell(2, col, "=HYPERLINK(\"" + rThread + "\", \"" + billNum + "\")")

##  END OF DECLARATION OF UTILITY FUNCTIONS - MAIN PROGRAM BELOW
#   Prepping spreadsheet
titleCol()

#   Compiling working lists
votes = getVotes(rThread)
gMPs = getMPs()
updateList = getUpdateCells(gMPs)

def countVote(gMP):
    voteCount = 0
    for i in votes:
        if str(i.author).lower() == gMP.lower():
            voteCount += 1
    if voteCount > 1:
        
        return gMP, 'DNV', True
    elif voteCount < 1:
        return gMP, 'DNV', False
    else:
        for i in votes:
            if str(i.author).lower() == gMP.lower():
                if 'aye' in str(i.body).lower():
                    return gMP, 'Aye', False
                elif 'nay' in str(i.body).lower():
                    return gMP, 'Nay', False
                elif 'abstain' in str(i.body).lower():
                    return gMP, 'Abs', False

print("The votes were as follows: ")

with concurrent.futures.ThreadPoolExecutor() as executor:
    for out in executor.map(countVote, gMPs):
        MP, vote, isDupe = out
        if isDupe == False:
            print(MP + " : " + vote)
        else:
            print(MP + " voted more than once and recieved a DNV")
        updateList[gMPs.index(MP)].value = vote

wks.update_cells(updateList)

end = time.time()

print("The count took " + end-strt + " seconds")
