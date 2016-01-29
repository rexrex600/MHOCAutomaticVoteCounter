__author__ = 'agentnola'
import praw
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('VoteCounter2-af942bc69325.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
r = praw.Reddit("Vote Counting Bot")
gc = gspread.authorize(credentials)
sh = gc.open('Copy of MHoC Master Sheet')
wks = sh.worksheet("7th Govt Voting Record")

#print("Input thread id")
#thread = raw_input()

#print("Input bill number")
#billnum = raw_input()

user = str(input("Reddit Username:"))


print("Reddit Password:")
password = str(input())
r.login(user,password)

print("Post Voting Thread Link")
tread = str(input())
print("Post billnumber(without the B infront of it)")
bill = 'B'+input()



def VoteCount(thread,billnum):
    column = int(wks.find(billnum).col)

    already_done = []
    submission = r.get_submission(thread)
    comments = praw.helpers.flatten_tree(submission.comments)

    for comment in comments:
        if comment.id not in already_done:
            print(comment.body)
            print(comment.author)
            if str(comment.author).lower() is not "automoderator":
                already_done.append(comment.id)
                if "aye" in str(comment.body).lower():
                    already_done.append(comment.id)
                    row = int(wks.find(str(comment.author).lower()).row)

                    val = wks.cell(row,column)
                    if "N/A" not in val.value:
                        wks.update_cell(row,column,"Aye")

                if "nay" in str(comment.body).lower():
                    already_done.append(comment.id)
                    row = wks.find(str(comment.author).lower()).row
                    val = wks.cell(row,column).value
                    if "N/A" not in val:
                        wks.update_cell(row,column,"Nay")
                if "abstain" in str(comment.body).lower():
                    already_done.append(comment.id)
                    row = wks.find(str(comment.author).lower()).row
                    val = wks.cell(row,column).value
                    if "N/A" not in val:
                        wks.update_cell(row,column,"Abst")


def deformat():
    cell_list = wks.range("C3:C141")
    for cell in cell_list:
        value = str(cell.value).lower()



        wks.update_cell(cell.row,cell.col,value)







##deformat()
VoteCount(tread,bill)
