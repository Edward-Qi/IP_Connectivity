import re                           # Import the regex module.
import pickle

err_occur = []                         # The list where we will store results.
new_list = []
pattern = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b") # Compile regular expression to match any phone number.
try:                              # Try to:
    with open ('ip_page.txt', 'rt', encoding='windows-1252') as in_file:          # open file for reading text.
        for linenum, line in enumerate(in_file):        # Keep track of line numbers.
              if pattern.search(line) != None:          # If pattern search finds a match,
                err_occur.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line number as tuple.
                start = '/lookup/'
                end = "'>"
                try:
                    new_list.append(line.split(start))[1].split(end)[0])
                except:
                    print("Error")
except FileNotFoundError:                   # If input file not found,
    print("Input file not found.")               # print an error message. 
