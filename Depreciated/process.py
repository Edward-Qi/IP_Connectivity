import re
PING_FILE = r"C:\Users\micha\Documents\GitHub\IP_Connectivity\pings.txt"

def parsePingFileForAvgs(pingFile, ipDictionary):  
    with open(pingFile, "r") as f:
        lines = f.readlines()
        # Loop through all lines, ignoring header.
        for l in lines[1::2]:
            ip = (l.split('Pinging ')[-1].split('with')[0])                 # Add last element to list (i.e. the process name)
            ip = ip.strip()                                                 # Remove the white space at the end.
            avg = (l.split()[-1].split(r"\r")[0])                           # Parse the average 
            avg = re.sub("[^0-9]", "", avg)                                 
            ipDictionary[ip].changeAvg(avg)                                 # Change the value of the average 
    
