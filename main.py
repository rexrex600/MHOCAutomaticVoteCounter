__author__ = [  'agentnola', 'chrispytoast123', 'jb567' ]
import gspread
import json
import praw
import re
from oauth2client.client import SignedJwtAssertionCredentials

#Variables

sheetName = '8th Govt Voting Record'
already_done = []
done_voters = []
dupes = []

#Loads the JSON Key, which is provided seperately
json_key = json.load(open('VoteCounter2-af942bc69325.json'))
scope = ['https://spreadsheets.google.com/feeds']
# Initilises all the credentials, and GoogleSheet stuff
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
r = praw.Reddit('MHOC-plebian house, vote counter v1')
gc = gspread.authorize(credentials)
sh = gc.open('MHoC Slave Sheet')
wks = sh.worksheet(sheetName)
#User Input for Reddit/ Reddit information
user = str(input('Reddit Username:'))
password = str(input('Reddit Password:'))
r.login(user,password)
print('Post Voting Thread Link')
thread = str(input())

#getColumn
column = 0
cells = wks.range('F3:BZ3')
for cell in cells:
    if cell.value == '':
        column = cell.col
        break
print(column)
#DNVing
bottomRow = int(wks.find('Speaker').row) - 1
print(bottomRow)
cell_list = wks.range(wks.get_addr_int(3, column) +  ':' +
        wks.get_addr_int(bottomRow, column))
for cell in cell_list:
    if not cell.value == 'N/A':
      cell.value='DNV'
wks.update_cells(cell_list)


submission = r.get_submission(thread)

#Name The Bill
title = str(submission.title)
billNum = str(re.search('^(\S+)', title).group())
print(billNum)
wks.update_cell(2, column, billNum)


if not re.search('^L', title) is None:
    wks.update_cell(1, column, 'L')
# else:
    #TODO find a way of doing parties wks.update_cell(1, column, 'C')

submission.replace_more_comments(limit=None, threshold=0)
comments = praw.helpers.flatten_tree(submission.comments)

for comment in comments:
    if comment.id not in already_done:
        print(str(comment.author) + ': ' + str(comment.body))
        try:
            row = int(wks.find(str(comment.author).lower()).row)
            cellValue = ''
            if 'aye' in str(comment.body).lower():
                already_done.append(comment.id)
                cellValue = 'aye'

            if 'nay' in str(comment.body).lower():
                already_done.append(comment.id)
                cellValue = 'nay'

            if 'abstain' in str(comment.body).lower():
                already_done.append(comment.id)
                cellValue = 'abs'
            if not 'N/A' == wks.cell(row, column).value:
                if not comment.author in done_voters:
                    wks.update_cell(row,column,'Aye')
                    done_voters.append(comment.author)
                else:
                    print('Dupe found: ' + comment.author)
                    dupes.append(comment.author)
        except gspread.exceptions.CellNotFound:
            print('Automod Comment')
        
print('Dupes: ' + str(dupes))
print('Done!')



