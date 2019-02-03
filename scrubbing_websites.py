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
import statistics
import matplotlib
import matplotlib.pyplot as plt

INITIAL_URL = r"https://tools.tracemyip.org/search--city/toronto-%21-ontario:-v-:&gTr=1&gNr=50"                                    # The link that contains all IPs in Toronto
WRITE_TO_IPS = r'C:\Users\micha\Documents\GitHub\IP_Connectivity\ip_addresses_all.txt'                                             # File that contains all the ip addresses
PING_FILE = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\pings.txt"                                                           # Write the pings to this file
IP_LIST = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\ipAddresses.pickle"                                                    # The list of ip addresses from the scrapped text file.
UPPER_BOUND = 9751                                                                                                                 # The upper bound of the ip links
IPADDRESS_DICT_FILE_NO_AVG = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\Pickled_Files\ip_Objects_No_Avg.pickle"             # The location of the pickle file that stores the information regarding IP addresses.
IPADDRESS_DICT_FILE_WITH_AVG = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\Pickled_Files\ip_Objects_With_Avg.pickle"         # The location of the pickle file that contains information on IP Addresses with the averages
IPADDRESS_DICT_FILE_WITH_ZSCORES = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\Pickled_Files\ip_Objects_With_Avg_AND_ZScore.pickle"       # Pickle file with all perks and with ips with a zscore of 0
IMAGE_TWO_D_PLOT_NON_DOWN = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\Pickled_Files\image_TwoD_Plot_Non_Down.png"                            # The plot of the 2-D plot that includes the greater area
IMAGE_TWO_D_PLOT_DOWN = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\Pickled_Files\image_TwoD_Plot_Down.png"                                    # The plot of the 2-D that only involves the downtown core.
CSV_IP_INFO = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\Pickled_Files\ipAddress_Information.csv"                           # Stores the ip address information in a csv format

class IPAddress:

    # Class: Determines how an IPAddress and its relevant information is stored

    # Function Name: __init__
    # Function Description: Initiate the IP Address. 
    # Parameters: longitude (The longitude where the IP address is located), latitude (The longitude where the IP address is located), 
    # average (The average time it takes to send n ping requests (The time is recorded in ms)), zipCode (The zip code of the ip address)
    # Returns: None
    # Throws: None

    def __init__(self, longitude, latitude, average, zipCode):
        self.longitude = longitude
        self.latitude = latitude
        self.average = average
        self.zipCode = zipCode
        self.zScore = 0
    
    # Mutate the average value
    def changeAvg(self, newVal):
        self.average = newVal

    # Mutate the z-score
    def changeZScore(self, score):
        self.zScore = score

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

    # Accessor method for the zipCode
    def getZScore(self):
        return self.zScore

def getRawIPAddresses(fileToWrite, loopTo):

    # Function Name: getRawIPAddresses
    # Function Description: The function gets all the raw data from the site including ip addresses. 
    # Parameters: fileToWrite (The path to the text file with the raw data), loopTo (The upper bound of the website to loop through)
    # Returns: None
    # Throws: None

    for i in range(1, UPPER_BOUND, 50):                                                                                                      # Loop through all the possible links on the website. The step is 50 because that is the maximum number of IPs that are show
        stringBuilder = r'https://tools.tracemyip.org/search--city/toronto-%21-ontario:-v-:&gTr=' + str(i) + '&gNr=' + str(i + 50)           # Build the string to loop through the entire site
        res = requests.get(stringBuilder)                                                                                                    # Send the requests and write to the files
        f = open(fileToWrite, "a+")
        f.write(res.text)
        f.close()
        print(str(i) + ": Another Request Good.")
        time.sleep(1)                                                                                                # Prevent the program from sending too many requests                                                                        

def parseIPAddresses(rawIPFile, dumpInto):

    # Function Name: parseIPAddresses
    # Function Description: The function parses the IP addresses from the raw data file 
    # Parameters: rawIPFile (The data that was scrubbed from the internet), dumpInto (The pickle file that will retrieve the dumped list)
    # Returns: errorCount (The number of lines that could not be parsed)
    # Throws: Throw an error when the line cannot be read.

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

def pingIPs(numPings, allIPs, pingFile):

    # Function Name: pingIPs
    # Function Description: The function pings all provided ip addresses for packets and records the necessary information.
    # Parameters: numPings (The number of pings to send to each IP), allIPs (The list that contains all the IP addresses to ping), 
    # pingFile (The file to write the ping information)
    # Returns: errorCount (The number of errors that were incurred during the collection process)
    # Throws: An error if there is an issue with a request. The errors are caught to prevent program termination.

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
    print("All done. The error count was: " + str(errorCount))
    return errorCount

def getLongandLat(allIPs, dumpInto):

    # Function Name: getLongandLat
    # Function Description: With the list of valid ips, get all the necessary information to map speed onto a graph
    # Parameters: allIPs (List of all valid ips), dumpInto (The pickle file with the dictionary of IP objects)
    # Returns: ipMap (A map to IPAddress objects that store necessary information)
    # Throws: An error if there is an issue with a request. The errors are caught to prevent program termination.

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
        time.sleep(0.5)       ##### INCREASE IF STOPS                                                                          # Create a slight delay in the program to prevent a crash
        if ((time.time() - currentTime) > 30):
            print("Thirty Seconds passed, Still processing. On IP: " + str(val) + " Located at index: " + str(i))
            currentTime = time.time()   
    with open(dumpInto, 'wb+') as f:            # Dump the contents into the following pickle file
        pickle.dump(ipMap, f)
    return ipMap

def parsePingFileForAvgs(pingFile, getIPObjectsNoAvg, dumpInto):  

    # Function Name: parsePingFileForAvgs
    # Function Description: Parse the ping file and get the average speeds
    # Parameters: pingFile (The file with all the ping requests), getIPObjectsNoAvg (The ip dictionary file name that contains all IP Address objects), 
    # dumpInto (The pickle to dump the file with the averages)
    # Returns: None
    # Throws: None

    with open(getIPObjectsNoAvg, "rb") as ips:           # Pickle list file
        ipDict = pickle.load(ips)
    num = 0
    with open(pingFile, "r") as f:
        lines = f.readlines()
        for l in lines[1::2]:                                               # Loop through all lines, ignoring header.
            ip = (l.split('Pinging ')[-1].split('with')[0])                 # Add last element to list (i.e. the process name)
            ip = ip.strip()                                                 # Remove the white space at the end.
            avg = (l.split()[-1].split(r"\r")[0])                           # Parse the average 
            avg = re.sub("[^0-9]", "", avg)     
            try:                            
                ipDict[ip].changeAvg(avg)                                 # Change the value of the average
            except:
                num += 1
    with open(dumpInto, 'wb+') as f:            # Dump the contents into the following pickle file
        pickle.dump(ipDict, f)
    print(num)                                  # Print number of errors, print length of dictionary
    print(len(ipDict))

def getAverageAndStdDev(ipDictionary):

    # Function Name: getAverageAndStdDev
    # Function Description: Calculate the avergae and the standard deviation of all the values in the list.
    # Parameters: ipDictionary (The dictionary file name of IP objects) 
    # Returns: A tuple containing the average and the standard deviation.
    # Throws: None

    with open(ipDictionary, "rb") as ips:           # Pickle list file
        ipDict = pickle.load(ips)
    calList = []
    numVals = 0
    for i, val in ipDict.items():                             # Loop through the entire list and append to list
        try:
            theAverage = float(val.getAverage())                    # Ensure it is the float form
            if (theAverage != 0.0):
                calList.append(theAverage)
                numVals += 1                                        # Tract the number of valid data points  
        except ValueError:   
            pass                                                    # Nothing will happen                                          
    avg = statistics.mean(calList)                                  # Calculate the average and the standard deviation
    std = statistics.stdev(calList)
    print("The number of used in the averages and standard deviation in getAverageAndStdDev: " + str(numVals))
    return (avg, std)

def upDateZScore(ipDictionary, theCityAvg, theCitySTD, dumpInto):

    # Function Name: upDateZScore
    # Function Description: Update all the z-scores in the dictionary.
    # Parameters: ipDictionary (The dictionary file name of IP objects) theCityAvg (The average of ping responses from the city), 
    # theCitySTD (The cities standard deviation), dumpInto (The file with all the information)
    # Returns: None
    # Throws: None

    with open(ipDictionary, "rb") as ips:           # Pickle the file
        ipDict = pickle.load(ips)
    numVals = 0                                     # Diagnostic information
    leanDict = {}
    for i, val in ipDict.items():                   # Loop through the entire dictionary, only use values with a positive average
        try:                                        # and place it in the newer dictionary
            thePingAverage = float(val.getAverage()) 
            if (thePingAverage != 0.0):
                newZ = (thePingAverage - theCityAvg) / theCitySTD
                numVals += 1
                leanDict[i] = IPAddress(val.getLongitude(), val.getLatitude(), val.getAverage(), val.getZipCode()) 
                leanDict[i].changeZScore(newZ) 
        except ValueError: 
            pass
    with open(dumpInto, 'wb+') as f:            # Dump the contents into the following pickle file
        pickle.dump(leanDict, f)
    print("The number of used in the averages and standard deviation in upDateZScore: " + str(numVals))

def createCSV(ipDictionary, writeInto_):
    with open(ipDictionary, "rb") as ips:           # Pickle the file
        ipDict = pickle.load(ips)
    with open(writeInto_ , 'a+') as f:
        f.write("Average, Latitude, Longitude, Z-Score")
    for indx, vals in ipDict.items():
        with open(writeInto_ , 'a+') as f:
            stringBuilder = str(vals.getAverage()) + "," + str(vals.getLatitude()) + "," + str(vals.getLongitude()) + "," + str(vals.getZScore()) + '\n'
            f.write(stringBuilder)

def graphTwoD(ipDictionary, cnFigure, nonCNFigure):

    # Function Name: graphTwoD
    # Function Description: Plot a 2D representation of the data.
    # Parameters: ipDictionary (The dictionary name of IP objects), cnFigure (The destination of the figure in the downtown core),
    # nonCNFigure (The destination of the non-downtown core)
    # Returns: None
    # Throws: None

   # if (((long > -79.49) and (long < -79.35)) and ((lat > 43.63) 
    #   and (lat < 43.72)) and (zScore < 3)):
     #   return True

    numUsed = 0
    with open(ipDictionary, "rb") as ips:           # Pickle the file
        ipDict = pickle.load(ips)
    longitudeAxis = []                                  # The three different types of axises
    latitudeAxis = []
    colourZScore = []
    avgTime = []
    boolInd = []
    for ind, vals in ipDict.items():                    # Iterate throught the entire dictionary and get the axis points
        if ((vals.getLongitude() > -79.57) and (vals.getLongitude() < -79.33) and (vals.getLatitude() > 43.62) 
            and (vals.getLatitude() < 43.85) and (vals.getZScore() < 3)):         # Determine the scope of the image
            longitudeAxis.append(vals.getLongitude())
            latitudeAxis.append(vals.getLatitude())
            colourZScore.append(vals.getZScore())
            avgTime.append(float(vals.getAverage()))
            numUsed += 1
    #plt.plot(longitudeAxis, latitudeAxis, c=colourZScore)                   # Plot the appropriate values based on standardised
    norm = [float(i)/sum(avgTime) for i in avgTime]
    plt.scatter(longitudeAxis, latitudeAxis, c=norm, cmap=plt.cm.Paired, linewidths=5)
    #f, ax = plt.subplots(1)
    #ax.set_ylim(bottom=43.63, top=43.72)
    #f.savefig(cnFigure, dpi=110)
    plt.title('Internet Speed Relative To Torontonians')
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.axvline(x=-79.49, color='r', linestyle='-')
    plt.axvline(x=-79.35, color='r', linestyle='-')
    plt.axhline(y=43.63, color='r', linestyle='-')
    plt.axhline(y=43.72, color='r', linestyle='-')                                             # Plot lines to show imaginary boxes    
    plt.colorbar()
    fig = plt.gcf()
    fig.set_size_inches(25, 13)
    #f.savefig(cnFigure, dpi=110)
    fig.savefig(cnFigure, dpi=110)
    fig.savefig(nonCNFigure, dpi=110)
    plt.clf()                                                                           # Clear the plots
    print("The number of values used: " + str(numUsed))

######getRawIPAddresses(WRITE_TO, UPPER_BOUND)                # 1. FIRST TASK: Writes the raw data from the site to a text file.
######parseIPAddresses(WRITE_TO_IPS, IP_LIST)                 # 2. SECOND TASK: Writes the ip addresses into a list 
######errorCount = pingIPs(15, e, PING_FILE)                  # 3. THIRD TASK: Ping the specified desired IP Addresses
######getLongandLat(ipDict, IPADDRESS_DICT_FILE_NO_AVG)       # 4. FOURTH TASK: Find the longitude and latitude of each 
parsePingFileForAvgs(PING_FILE, IPADDRESS_DICT_FILE_NO_AVG, IPADDRESS_DICT_FILE_WITH_AVG)         # 5. FIFTH TASK: Put the averages from the text file
(avg, std) = getAverageAndStdDev(IPADDRESS_DICT_FILE_WITH_AVG)          # 6. SIXTH TASK: Find the average and the standard deviation
upDateZScore(IPADDRESS_DICT_FILE_WITH_AVG, avg, std, IPADDRESS_DICT_FILE_WITH_ZSCORES)  # 7. SEVENTH TASK: Put the z-scores into the dictionary and pickle
graphTwoD(IPADDRESS_DICT_FILE_WITH_ZSCORES, IMAGE_TWO_D_PLOT_DOWN, IMAGE_TWO_D_PLOT_NON_DOWN)        # 8. EIGTH TASK: Put the data into a graph. (Create for both)
createCSV(IPADDRESS_DICT_FILE_WITH_ZSCORES, CSV_IP_INFO)