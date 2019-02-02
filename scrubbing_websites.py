# Program Description: Collect all the data from the website and parse all the ip addresses.
# Date: February 02, 2019
# Author: Michael Krakovsky
# Version: 1.0

import requests                                                                                             # Enable access of get requests
import bs4
import time
import subprocess
import pickle
import re                           # Import the regex module.

INITIAL_URL = r"https://tools.tracemyip.org/search--city/toronto-%21-ontario:-v-:&gTr=1&gNr=50"             # The link that contains all IPs in Toronto
WRITE_TO_IPS = r'C:\Users\micha\Documents\GitHub\IP_Connectivity\ip_addresses_all.txt'                      # File that contains all the ip addresses
WRITE_TO_PINGS = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\pings.txt"                               # Write the pings to this file
UPPER_BOUND = 9751                                                                                          # The upper bound of the ip links

# Class: Determines how an IPAddress and its relevant information is stored

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


# Function Name: getRawIPAddresses
# Function Description: The function gets all the raw data from the site including ip addresses. 
# Parameters: fileToWrite (The path to the text file with the raw data), loopTo (The upper bound of the website to loop through)
# Returns: None
# Throws: None

def getRawIPAddresses(fileToWrite, loopTo):
    for i in range(1, UPPER_BOUND, 50):                                                                                                      # Loop through all the possible links on the website. The step is 50 because that is the maximum number of IPs that are show
        stringBuilder = r'https://tools.tracemyip.org/search--city/toronto-%21-ontario:-v-:&gTr=' + str(i) + '&gNr=' + str(i + 50)           # Build the string to loop through the entire site
        res = requests.get(stringBuilder)                                                                                                    # Send the requests and write to the files
        f = open(fileToWrite, "a+")
        f.write(res.text)
        f.close()
        print(str(i) + ": Another Request Good.")
        time.sleep(1)                                                                                                # Prevent the program from sending too many requests                                                                        

# Function Name: parseIPAddresses
# Function Description: The function parses the IP addresses from the raw data file 
# Parameters: rawIPFile (The data that was scrubbed from the internet), dumpInto (The pickle file that will retrieve the dumped list)
# Returns: errorCount (The number of lines that could not be parsed)
# Throws: Throw an error when the line cannot be read.

def parseIPAddresses(rawIPFile, dumpInto):
    ipAddresses = []                                                                # Where the final ip address will be stored.
    err_occur = []                                                                  # The list where we will store results.
    errorCount = 0
    pattern = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")                 # Compile regular expression to match any ip address.
    try:                              # Try to:
        with open (rawIPFile, 'rt', encoding='windows-1252') as in_file:          # open file for reading text.
            for linenum, line in enumerate(in_file):        # Keep track of line numbers.
                if pattern.search(line) != None:          # If pattern search finds a match,
                    err_occur.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line number as tuple.
                    start = '/lookup/'
                    end = "'>"
                    try:
                        ipAddresses.append((line.split(start))[1].split(end)[0])            # Append the IP address
                    except:
                        print("Error: The line that cannot be parsed." + line +'\n' + '\n')
                        errorCount +=1                                                          # Indicate a failed parsed line, inc error count
    except FileNotFoundError:                   # If input file not found,
        print("Input file not found.")               # print an error message. 
    with open(dumpInto, 'wb+') as f:            # Dump the contents into the following pickle file
        pickle.dump(ipAddresses, f)

# Function Name: pingIPs
# Function Description: The function pings all provided ip addresses for packets and records the necessary information.
# Parameters: numPings (The number of pings to send to each IP), allIPs (The list that contains all the IP addresses to ping), 
# pingFile (The file to write the ping information)
# Returns: errorCount (The number of errors that were incurred during the collection process)
# Throws: An error if there is an issue with a request. The errors are caught to prevent program termination.

def pingIPs(numPings, allIPs, pingFile):
    errorCount = 0                                                                              # Track the number of throw aways
    currentTime = time.time()
    for idx, val in enumerate(allIPs):
        try:
            commandString = "ping -n " + str(numPings) + " -w 3000 " + str(val)                   # Loop through all IPs, and ping each one numPings times.
            commandOut = subprocess.check_output(commandString)                                 # -w specifies the timeout value, -n specifies the number of times to ping
            f = open(pingFile, "a+")
            f.write(str(commandOut))                                                            # Record the output and write to the file.
            f.write('\n' + 50 * "-" + '\n')
            f.close()
        except:
            errorCount += 1                                                                     # Keep the algorithm purring, record failed query
            print("There was an error at IP: " + str(val) + " Located at index: " + str(idx))
        if ((time.time() - currentTime) > 300):
            print("Five minutes has passed, I am still pinging! Currently on IP: " + str(val) + " Located at index: " + str(idx))
            currentTime = time.time()                                                               # Indicate that the program is still pinging and reset timer
    return errorCount

# Function Name: getLongandLat
# Function Description: With the list of valid ips, get all the necessary information to map speed onto a graph
# Parameters: allIPs (List of all valid ips), dumpInto (The pickle file with the dictionary of IP objects)
# Returns: ipMap (A map to IPAddress objects that store necessary information)
# Throws: An error if there is an issue with a request. The errors are caught to prevent program termination.

def getLongandLat(allIPs, dumpInto):
    ipMap = {}   
    currentTime = time.time()                                                                   # Store the ip address information in a hash table
    for i, val in enumerate(allIPs):
        stringBuilder = r"http://ip-api.com/json/" + str(val)                                   # Build a string to send request for json
        insertObject = None                                                                     # Set the default value to none
        res = requests.get(stringBuilder)
        data = res.json()                                                                       # Retrieve the JSON format text and build the object with the necessary information
        if (data['status'] == 'success'):
            insertObject = IPAddress(data['lon'], data['lat'], 0, data['zip'])                  # Add proper content
            ipMap[val] = insertObject                                                           # Add the IP to the dictionary
        else:
            print(str(val) + ": There was an error in getting this IPs information.")
        time.sleep(0.5)                                                                             # Create a slight delay in the program to prevent a crash
        if ((time.time() - currentTime) > 30):
            print("Thirty Seconds passed, Still processing. On IP: " + str(val) + " Located at index: " + str(i))
            currentTime = time.time()   
        with open(dumpInto, 'wb+') as f:            # Dump the contents into the following pickle file
            pickle.dump(ipMap, f)
    return ipMap



with open(r"C:\Users\micha\Documents\GitHub\IP_Connectivity\ipAddresses.pickle", "rb") as input_file:               # Pickle list file
    e = pickle.load(input_file)

errorCount = pingIPs(15, e, r"C:\Users\micha\Documents\GitHub\IP_Connectivity\pings.txt")
print("All done. The error count was: " + str(errorCount))
######getRawIPAddresses(WRITE_TO, UPPER_BOUND)                # Only needs to be run ONCE! Writes the raw data from the site to a text file.