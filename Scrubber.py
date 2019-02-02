import re                           # Import the regex module.

err_occur = []                         # The list where we will store results.
pattern = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b") # Compile regular expression to match any phone number.                         # Try to:
    with open ('ip_page.txt', 'r') as in_file:          # open file for reading text.
        for linenum, line in enumerate(in_file):        # Keep track of line numbers.
            if pattern.search(line) != None:          # If pattern search finds a match,
                try:
                    err_occur.append((linenum, line.rstrip('\n'))) # strip linebreaks, store line and line number as tuple.
                    print("Line ", linenum, ": ", line, sep='')  # print results as "Line [linenum]: [line]".
                except:
                    print("Error")               # print an error message.
                    exit()
                  # If input file not found,
    print("Input file not found.")               # print an error message. 
