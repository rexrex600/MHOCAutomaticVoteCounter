__author__ = 'Wade'
import praw
import gspread
r = praw.Reddit("Vote Counting Bot")
gc = gspread.authorize()
def parseVote():
