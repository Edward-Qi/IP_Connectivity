# Program Description: Collect all the data from the website and parse all the ip addresses.
# Date: February 02, 2019
# Author: Michael Krakovsky
# Version: 1.0

import requests                                                                                             # Enable access of get requests
import bs4
import time
import subprocess
import pickle

INITIAL_URL = r"https://tools.tracemyip.org/search--city/toronto-%21-ontario:-v-:&gTr=1&gNr=50"             # The link that contains all IPs in Toronto
WRITE_TO_IPS = r'C:\Users\micha\Documents\GitHub\IP_Connectivity\ip_addresses_all.txt'                      # File that contains all the ip addresses
WRITE_TO_PINGS = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\pings.txt"                               # Write the pings to this file
UPPER_BOUND = 9751                                                                                          # The upper bound of the ip links

# Function Name: getRawIPAddresses
# Function Description: The function gets all the raw data from the site including ip addresses. 
# Parameters: fileToWrite (The path to the text file with the raw data), loopTo (The upper bound of the website to loop through)
# Returns: None
# Throws: None

def getRawIPAddresses(fileToWrite, loopTo):
    for i in range(1, UPPER_BOUND, 50):                                                                         # Loop through all the possible links on the website. The step is 50 because that is the maximum number of IPs that are show
        stringBuilder = r'https://tools.tracemyip.org/search--city/toronto-%21-ontario:-v-:&gTr=' + str(i) + '&gNr=' + str(i + 50)           # Build the string to loop through the entire site
        res = requests.get(stringBuilder)                                                                       # Send the requests and write to the files
        f = open(fileToWrite, "a+")
        f.write(res.text)
        f.close()
        print(str(i) + ": Another Request Good.")
        time.sleep(1)                                                                                                # Prevent the program from sending too many requests                                                                        

# Function Name: pingIPs
# Function Description: The function pings all provided ip addresses for packets and records the necessary information.
# Parameters: numPings (The number of pings to send to each IP), allIPs (The list that contains all the IP addresses to ping), 
# pingFile (The file to write the ping information)
# Returns: None
# Throws: None

def pingIPs(numPings, allIPs, pingFile):
    errorCount = 0
    currentTime = time.time()
    for i in allIPs:
        try:
            commandString = "ping -n " + str(numPings) + " -w 3000 " + str(i)                   # Loop through all IPs, and ping each one numPings times.
            commandOut = subprocess.check_output(commandString)                                 # -w specifies the timeout value, -n specifies the number of times to ping
            f = open(pingFile, "a+")
            f.write(str(commandOut))                                                                 # Record the output and write to the file.
            f.write('\n' + 50 * "-" + '\n')
            f.close()
        except:
            errorCount += 1
            print("There was an error at IP: " + str(i))
        if ((time.time() - currentTime) > 300):
            print("Five minutes has passed, I am still pinging! Currently on IP: " + str(i))
            currentTime = time.time()                                                               # Indicate that the program is still pinging and reset timer
    return errorCount


with open(r"C:\Users\micha\Documents\GitHub\IP_Connectivity\ipAddresses.pickle", "rb") as input_file:
    e = pickle.load(input_file)

errorCount = pingIPs(15, e, r"C:\Users\micha\Documents\GitHub\IP_Connectivity\pings.txt")
print("All done. The error count was: " + str(errorCount))
######getRawIPAddresses(WRITE_TO, UPPER_BOUND)                # Only needs to be run ONCE! Writes the raw data from the site to a text file.