

from datetime import datetime
from dateutil import tz

# from_zone = tz.tzutc()
# to_zone = tz.tzlocal()

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Asia/Beijing')



utc = datetime.utcnow().replace(tzinfo=from_zone)
print(utc.astimezone(to_zone))
print(datetime.now())


utc = datetime.now().replace(tzinfo=to_zone)
print(utc.astimezone(from_zone))
print(datetime.utcnow())
