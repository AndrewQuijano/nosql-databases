import urllib.request

# Get the content
url = "https://api.nasa.gov/planetary/apod?api_key=Yw2oULHGrrGXP7nhbAIDonIEYuq6l5Ewns8ugb6d"
date = "&start_date=2017-12-28"
contents = urllib.request.urlopen(url+date).read()

# Parse it to get the image URL
