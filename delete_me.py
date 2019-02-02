import pickle 
import time

PICKLE_IP_INFO = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\Pickled_Files\IP_Address_Information.pickle"

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

