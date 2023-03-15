import requests
from api_key import api_key
from volume_numbers import volume_numbers_list

county_ids = [100002, 100003, 100004, 100005, 100006, 100007, \
              100008, 100009, 100010, 100013, 100015, 100016, \
              100017, 100018, 100019, 100020, 100021, 100022, \
              100023, 100024, 100025, 100026, 100027, 100028, \
              100029,100031]

#download volumes for each county with api

for volume_number in volume_numbers_list:
    x = requests.get("https://www.duchas.ie/api/v0.6/cbes/?VolumeNumber={0}&apiKey={1}".format(volume_number, api_key))
    file = open("volumes\\{0}.json".format(volume_number), 'wb')
    file.write(x.content)
    file.close()