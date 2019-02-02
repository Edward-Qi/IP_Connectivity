import pickle 
import time
import requests

PICKLE_IP_INFO = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\Pickled_Files\IP_Address_Information.pickle"

class IPAddress:

    # Function Name: __init__
    # Function Description: Initiate the IP Address. 
    # Parameters: longitude (The longitude where the IP address is located), latitude (The longitude where the IP address is located), 
    # average (The average time it takes to send 15 ping requests), zipCode (The zip code of the ip address)
    # Returns: None
    # Throws: None

    def __init__(self, longitude, latitude, average, zipCode):
        self.longitude = longitude
        self.latitude = latitude
        self.average = average
        self.zipCode = zipCode

    # Accessor method for the longitude
    def getLongitude(self):
        return self.longitude

    # Accessor method for the latitude
    def getLatitude(self):
        return self.latitude

    # Accessor method for the average of packets sent
    def getAverage(self):
        return self.average

    # Accessor method for the zipCode
    def getZipCode(self):
        return self.zipCode

def getLongandLat(allIPs, dumpInto):
    ipMap = {}   
    currentTime = time.time()                                                                                   # Store the ip address information in a hash table
    for i, val in enumerate(allIPs):
        stringBuilder = r"http://ip-api.com/json/" + str(val)                                         # Build a string to send request for json
        insertObject = None                                                                         # Set the default value to none
        res = requests.get(stringBuilder)
        data = res.json()                                                                       # Retrieve the JSON format text and build the object with the necessary information
        if (data['status'] == 'success'):
            insertObject = IPAddress(data['lon'], data['lat'], 0, data['zip'])                  # Add proper content
            ipMap[val] = insertObject
        else:
            print(str(val) + ": There was an error in getting this IPs information.")
        time.sleep(1)                                                                             # Create a slight delay in the program to prevent a crash
        if ((time.time() - currentTime) > 30):
            print("Thirty Seconds has passed, I am still pinging! Currently on IP: " + str(val) + " Located at index: " + str(i))
            currentTime = time.time()   
        with open(dumpInto, 'wb+') as f:            # Dump the contents into the following pickle file
            pickle.dump(ipMap, f)
    return ipMap

with open(r"C:\Users\micha\Documents\GitHub\IP_Connectivity\ipAddresses.pickle", "rb") as input_file:
    l = pickle.load(input_file)

getLongandLat(l, PICKLE_IP_INFO)

