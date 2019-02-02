# Program Description: Collect all the data from the website and parse all the ip addresses.
# Date: February 02, 2019
# Author: Michael Krakovsky
# Version: 1.0

import requests                                                                                             # Enable access of get requests
import bs4
from time import sleep

INITIAL_URL = r"https://tools.tracemyip.org/search--city/toronto-%21-ontario:-v-:&gTr=1&gNr=50"              # The link that contains all IPs in Toronto
WRITE_TO = r'C:\Users\micha\Documents\GitHub\IP_Connectivity\ip_addresses_all.txt'                      # File that contains all the ip addresses
UPPER_BOUND = 9751                                                                                          # The upper bound of the ip links


def getRawIPAddresses():
    for i in range(1, UPPER_BOUND, 50):                                                                         # Loop through all the possible links on the website. The step is 50 because that is the maximum number of IPs that are show
        stringBuilder = r'https://tools.tracemyip.org/search--city/toronto-%21-ontario:-v-:&gTr=' + str(i) + '&gNr=' + str(i + 50)           # Build the string to loop through the entire site
        res = requests.get(stringBuilder)                                                                       # Send the requests and write to the files
        f = open(WRITE_TO, "a+")
        f.write(res.text)
        f.close()
        print(str(1) + ": Another Request Good.")
        sleep(1)                                                                                                # Prevent the program from sending too many requests                                                                        

getRawIPAddresses()