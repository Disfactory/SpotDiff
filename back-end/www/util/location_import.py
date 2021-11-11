import requests
#from models.model_operations import location_operations
#from models.model import db

"""
  The script uses disfactory API to fill the location table. 
  Only factory_id is imported now.
"""


#120.035141 < lng < 122.007164
#21.8969 < lat < 25.298401

# Explore the sliced area of Taiwan by lat/lng. Each is about 29km*29km.

"""
center_lat = 21.8969
DIFF = 0.01
CENTER_LNG_INIT = 120.035141
CENTER_LAT_INIT = 21.8969

center_lat = CENTER_LAT_INIT
center_lng = CENTER_LNG_INIT

while center_lng <= 122.007164:
    while center_lat <= 25.298401:
        str_url = "https://api.disfactory.tw/api/factories?lng={}&lat={}&range=30".format(center_lng, center_lat)

        #print(str_url)
        params = {'is_coming_soon': False, 'is_paid': True, 'limit': 200, 'skip': 0}
        r=requests.get(url=str_url, json=params)

        if(r.status_code == 200):
          response_list = r.json()        
          print("# : ", len(response_list))

        center_lat = center_lat + DIFF

    center_lng = center_lng + DIFF
    center_lat = CENTER_LAT_INIT

"""
#url = "https://api.disfactory.tw/api/factories?lng=121.0&lat=21.9&range=30" 
url = "https://api.disfactory.tw/api/factories"
#url = "https://api.disfactory.tw/api/factories?lng=121.0&lat=21.9&range=30" #19 items

params = {"lng" : "121.0", "lat" : "21.9", "range" : "100"}
r=requests.get(url=url, params=params)
print("request status:", r.status_code)
print(r.text)

response_list = r.json()

print("The number of the items in the dictionary is ", len(response_list))

"""
idx = 0
while idx < len(response_list):
    print(response_list[idx]["id"], " ", response_list[idx]["lat"], " ", response_list[idx]["lng"])
    idx = idx + 1
#print("Total number:", response_list[0])
"""


"""

# Create the location table
#db.create_all()


"""

