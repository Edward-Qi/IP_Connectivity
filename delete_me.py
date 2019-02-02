import pickle 

with open(r"C:\Users\micha\Documents\GitHub\IP_Connectivity\ipAddresses.pickle", "rb") as input_file:
    e = pickle.load(input_file)

print(e.index("99.224.24.61"))