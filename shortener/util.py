import tzlocal
import pytz

def getLocalCreateAt(createAt):
    local_timezone = tzlocal.get_localzone()
    return createAt.replace(tzinfo=pytz.utc).astimezone(local_timezone)
