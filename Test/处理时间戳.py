import datetime
timeStamp = 1615207516
dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
otherStyleTime = dateArray.strftime("%H")
print(type(otherStyleTime))