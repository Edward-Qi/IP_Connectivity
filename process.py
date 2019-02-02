processes = []

with open(r"C:\Users\User\Downloads\IP_Connectivity-master\IP_Connectivity-master\pings.txt", "r") as f:
    lines = f.readlines()
    # Loop through all lines, ignoring header.
    # Add last element to list (i.e. the process name)
    for l in lines[1::2]:
        processes.append(print(((l.split('Pinging ')[-1].split('with')[0]),(l.split()[-1].split(r"\r")[0]))))


