import urllib.request
import json

# BASE URL
url = "https://api.nasa.gov/planetary/apod?api_key=Yw2oULHGrrGXP7nhbAIDonIEYuq6l5Ewns8ugb6d"

# Parse JSON Object
# It will turn this into a dictionary
def parsePictureURL(contents):
    # dictionary/Hashmap, use loads because you have a string!
    parse_json = json.loads(contents)
    # Get url and print it
    print(parse_json['url'])

def main():
    # My Birthday
    myBirthdate = "&date=2017-12-28"

    # Complete GET request and decode it...
    contents = urllib.request.urlopen(url + myBirthdate).read().decode('utf-8')

    # Pass it to function to be processed
    parsePictureURL(contents)
main()
# Parse it to get the image URL
