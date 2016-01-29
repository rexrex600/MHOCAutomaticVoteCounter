__author__ = 'Wade'
import praw
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('VoteCounter2-4813f2f9f7f3.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
r = praw.Reddit("Vote Counting Bot")
gc = gspread.authorize(credentials)
sh = gc.open('Copy of MHoC Master Sheet')
wks = sh.worksheet("7th Govt Voting Record")
r.login('agentnola','')
#print("Input thread id")
#thread = raw_input()

#print("Input bill number")
#billnum = raw_input()

id = '42zo6y'
bill = "B226"



def VoteCount(thread,billnum):
    column = wks.find(billnum).col

    already_done = []
    submission = r.get_submission(submission_id='42zo6y')
    comments = praw.helpers.flatten_tree(submission.comments)

    for comment in comments:
        if comment.id not in already_done:
            print comment.body
            print comment.author
            if "Aye" in comment.body:
                already_done.append(comment.id)
                row = wks.find(comment.author).row
                wks.update_cell(row,column,"Aye")

            if "Nay" in comment.body:
                already_done.append(comment.id)
                row = wks.find(comment.author).row
                wks.update_cell(row,column,"Nay")








VoteCount(id,bill)
