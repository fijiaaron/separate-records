# separate_records.py
# usage:
#   python separate_records.py [-f INPUT_FILENAME -o OUTPUT_DIRECTORY -d DELIMITER -m MATCHER] 

import os
from datetime import datetime
from re import split

timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

delimiter = "//STX12"
matcher = "1280001"
matcher_signifies = "Thailand"
input_filename = "DX-XF-FF.txt"
output_directory = "."
file_ext = ".080"

try: 
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, default=input_filename, help=f"input file, default: {input_filename}")
    parser.add_argument('-o',  '--output', type=str, default=output_directory, help=f"output directory, default: {output_directory}")
    parser.add_argument('-d', '--delimiter', type=str, default=delimiter, help=f"token to delimit records, default: {delimiter}")
    parser.add_argument('-m',  '--matcher', type=str, default=matcher, help=f"token to seek a match in records, default: {matcher}")
    args = parser.parse_args()

    input_filename = args.filename    
    output_directory = args.output
    delimiter = args.delimiter
    matcher = args.matcher
except ImportError:
    print("using default options")

filename = os.path.basename(input_filename)
basename, ext = os.path.splitext(filename)

output_match_filename = os.path.join(output_directory, basename +  "_with_" + matcher_signifies +  file_ext)
output_nomatch_filename = os.path.join(output_directory, basename +  "_without_" + matcher_signifies + file_ext)

print("input filename:", input_filename)
print("output directory:", output_directory)
print("delimiter: ", delimiter)
print("matcher: ", matcher)

matches = []
nomatches = []

with open(input_filename, "r") as infile:
    content = infile.read()
    sections = split(r'.(?=' + delimiter + ')', content)

    for section in sections:
        if matcher in section:
            matches.append(section)
        else:
            nomatches.append(section)

print(f"sections containing `{matcher}`:", len(matches))
print(f"sections not containing `{matcher}:`", len(nomatches))
print(f"total sections", len(sections))

with open(output_match_filename, "w") as outfile_matches:
    outfile_matches.writelines(matches)
    print("wrote matches to file: ", output_match_filename)

with open(output_nomatch_filename, "w") as outfile_nomatches:
    outfile_nomatches.writelines(nomatches)
    print("wrote non-matches to file: ", output_nomatch_filename)
