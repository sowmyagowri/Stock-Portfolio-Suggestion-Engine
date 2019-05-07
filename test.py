import datetime, pytz
import timedelta
# print (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime('%Y-%m-%d')
print datetime.datetime.now(pytz.timezone('US/Pacific'))
