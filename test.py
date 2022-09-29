from backend.tweet import TweetSchedule
username, password = '@SUyghurmuslims', '!qwe03192057092zxc#'
tweet = TweetSchedule(username, password)

time = tweet.start_scheduling()
print('time', time)
