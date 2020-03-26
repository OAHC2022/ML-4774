import csv
import os
from six.moves import urllib
import googlemaps
from dotenv import load_dotenv
load_dotenv()

DATA_URL = 'https://raw.githubusercontent.com/OAHC2022/ML-4774/master/project/municipality.csv'

def get_data(data_url=DATA_URL):
    csv_path = os.path.join(os.getcwd(),'data.csv')     
    urllib.request.urlretrieve(data_url,csv_path)

def parse_data():
    with open('data.csv',newline='') as csvfile:
        reader = csv.reader(csvfile)
        #  burn the first two lines
        reader.__next__()
        reader.__next__()

        result = []
        for row in reader:
            result.append(row[0])
        # burn the last one
        return result[:-1]


def get_coordinate(api_key, bldg_list):
    """
    Use googlemaps api to get the meta data of each building
    :param api_key: the api key for google api
    :param bldg: building name at UVa
    :return: None if the address does not exist, MetaData if exists
    """
    gm = googlemaps.Client(key=api_key)
    result = []
    counter = 0
    for bldg in bldg_list:
        geocode_result = gm.geocode('{}'.format(bldg))
        loc_lat = geocode_result[0]['geometry']['location']['lat']
        loc_lng = geocode_result[0]['geometry']['location']['lng']
        ne_lat = geocode_result[0]['geometry']['viewport']['northeast']['lat']
        ne_lng = geocode_result[0]['geometry']['viewport']['northeast']['lng']
        sw_lat = geocode_result[0]['geometry']['viewport']['southwest']['lat']
        sw_lng = geocode_result[0]['geometry']['viewport']['southwest']['lng']

        result.append([loc_lat,loc_lng,ne_lat,ne_lng,sw_lat,sw_lng])
        counter += 1
        print('finish {}/{}'.format(counter,len(bldg_list)))
    return result

def write_data(data):
    with open('location.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Latitude","Longitude","NE Latitude","NE Longitude","SW Latitude","SW Longitude"])
        writer.writerows(data)

if __name__ == '__main__':
    get_data()
    locations = parse_data()
    api_key = os.environ.get('map_api_key')
    results = get_coordinate(api_key,locations)
    write_data(results)
