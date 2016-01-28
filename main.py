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

wks = gc.open_by_key('1Z6gg99ViOVNuSDzO77wh71ZRr2HKwYi9pd1s9pnuYkY').sheet1



