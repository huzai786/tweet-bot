from backend.tweet import TweetSchedule, _extract_time


tweet = TweetSchedule(username='@SUyghurmuslims', password='!qwe03192057092zxc#')
tweet_time = tweet.last_tweet_time()
x = _extract_time(tweet_time)
