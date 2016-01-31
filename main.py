__author__ = 'agentnola'
import praw
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

#Loads the JSON Key, which is provided seperately
json_key = json.load(open('VoteCounter2-af942bc69325.json'))
scope = ['https://spreadsheets.google.com/feeds']
# Initilises all the credentials, and GoogleSheet stuff 
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
r = praw.Reddit("Vote Counting Bot")
gc = gspread.authorize(credentials)
sh = gc.open('MHoL Master Sheet')
print("Press 1 For Main Votes 2 For Amendment Votes")
vote = int(input())
if vote == 1:
	wks = sh.worksheet("VII - Bill and Motion Votes")
if vote == 2:
	wks = sh.worksheet("VII - Amendment Votes")
#User Input for Reddit/ Reddit information
user = str(input("Reddit Username:"))
print("Reddit Password:")
password = str(input())
r.login(user,password)
print("Post Voting Thread Link")
tread = str(input())
print("Post billnumber(without the B infront of it) if it is a LB remove the L temporarily from the top of spreadsheet column")
print("Press 1 For Lords Bill 2 For Commons Bill 3 For a Lords' Motion")
type = int(input())
if type == 1:
	bill = 'LB'+input()
if type == 2:
	bill = 'B'+input()
if type == 3:
	bill = 'LM'+input()

def VoteCount(thread,billnum):
    column = int(wks.find(billnum).col)

    already_done = []
    submission = r.get_submission(thread)
    comments = praw.helpers.flatten_tree(submission.comments)

    for comment in comments:
        if comment.id not in already_done:
            print(comment.body)
            print(comment.author)
        
                
            if "content" in str(comment.body).lower() and "not" not in str(comment.body).lower():
                row = wks.find(str(comment.author).lower()).row
                val = wks.cell(row,column).value
                if "N/A" not in val:
                    wks.update_cell(row,column,"Con")
                    already_done.append(comment.id)
            if "content" in str(comment.body).lower() and "not" in str(comment.body).lower():
                row = wks.find(str(comment.author).lower()).row
                val = wks.cell(row,column).value
                if "N/A" not in val:
                    wks.update_cell(row,column,"Not")
                    already_done.append(comment.id)
                
                
               
           
            



def deformat():
    cell_list = wks.range("C3:C141")
    for cell in cell_list:
        value = str(cell.value).lower()



        wks.update_cell(cell.row,cell.col,value)







##deformat()
VoteCount(tread,bill)
