from datetime import datetime
import pytz
import requests,os

bearer_token = os.environ.get("BEARER_TOKEN")

#import requests

response = requests.get("https://api.twitter.com/2/tweets", headers={"Authorization": "Bearer YOUR_BEARER_TOKEN"})
if "Date" in response.headers:
    twitter_time_str = response.headers["Date"]
    print(f"Twitter Server Time (UTC): {twitter_time_str}")
# Convert UTC time to your local time zone
from datetime import datetime, timezone
import pytz

# Get Twitter server time (example from API response header)
twitter_time = datetime.strptime(twitter_time_str, "%a, %d %b %Y %H:%M:%S %Z")
twitter_time = twitter_time.replace(tzinfo=timezone.utc)

# Get your system's current time (in UTC)
local_time = datetime.now(timezone.utc)

# Compare times
time_difference = abs((local_time - twitter_time).total_seconds())
print(f"System Time (UTC): {local_time}")
print(f"Twitter Server Time (UTC): {twitter_time}")
print(f"Time Difference (seconds): {time_difference}")