from backend.tweet import TweetSchedule
from bs4 import BeautifulSoup


tweet = TweetSchedule(username='@SUyghurmuslims', password='!qwe03192057092zxc#')
tweet_time = tweet.start_scheduling()
print(tweet_time)
