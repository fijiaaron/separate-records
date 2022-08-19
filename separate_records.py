# separate_records.py
# usage:
#   python separate_records.py [-f INPUT_FILENAME -o OUTPUT_DIRECTORY -d DELIMITER -m MATCHER] 

import os
import re
from collections import defaultdict

# set default parameters
delimiter = "//STX12"
matcher = "1280001"
matcher_signifies = "Thailand"
input_filename = "DX-XF-FF.txt"
output_directory = "."
file_ext = ".080"

# get settings from config file
from configparser import ConfigParser
config = ConfigParser()
config.read("separate_records.ini") 
if config and config.has_section("SETTINGS"):
    settings = config['SETTINGS']

    delimiter = settings['delimiter'] if settings['delimiter'] else delimiter
    matcher = settings['matcher'] if settings['matcher'] else matcher
    matcher_signifies = settings['matcher_signifies'] if settings['matcher_signifies'] else matcher_signifies
    input_filename = settings['input_filename'] if settings['input_filename'] else input_filename
    output_directory = settings['output_directory'] if settings['output_directory'] else output_directory
    file_ext = settings['file_ext'] if settings['file_ext'] else file_ext

# get command line options
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', type=str, default=input_filename, help=f"input file, default: {input_filename}")
parser.add_argument('-o',  '--output', type=str, default=output_directory, help=f"output directory, default: {output_directory}")
parser.add_argument('-d', '--delimiter', type=str, default=delimiter, help=f"token to delimit records, default: {delimiter}")
parser.add_argument('-m',  '--matcher', type=str, default=matcher, help=f"token to seek a match in records, default: {matcher}")
args = parser.parse_args()


# set parameters from command line options
try: 
    input_filename = args.filename    
    output_directory = args.output
    delimiter = args.delimiter
    matcher = args.matcher
except ImportError:
    print("using default options")


# main function for processing input and writing output 
def separate_records(input_filename=input_filename, delimiter=delimiter, matcher=matcher, matcher_signifies=matcher_signifies, output_directory=output_directory):

    # get base filename without extension and create output files based on input filename
    filename = os.path.basename(input_filename)
    basename, ext = os.path.splitext(filename)
    output_match_filename = os.path.join(output_directory, basename +  "_with_" + matcher_signifies +  file_ext)
    output_nomatch_filename = os.path.join(output_directory, basename +  "_without_" + matcher_signifies + file_ext)

    print("input filename:", input_filename)
    print("output directory:", output_directory)
    print("delimiter: ", delimiter)
    print("matcher: ", matcher)

    # initialize empty lists to collect matching / non-matching sections
    matches = []
    nomatches = []

    # open input file for processing
    with open(input_filename, "r") as infile:
        content = infile.read()

        # split contents into a list of separate strings for each section
        sections = split_content_into_sections(content, delimiter)

        # divide into matching / non-matching records
        for section in sections:
            if matcher in section:
                matches.append(section)
            else:
                nomatches.append(section)

    # print simple report of processing
    print(f"sections containing `{matcher}`:", len(matches))
    print(f"sections not containing `{matcher}`:", len(nomatches))
    print(f"total sections: ", len(sections))

    # write matching records to output file
    with open(output_match_filename, "w") as outfile_matches:
        if len(matches) != 0:
            content_matches = "".join(matches)
            outfile_matches.write(content_matches)
            print("wrote matches to file: ", output_match_filename)
        else:
            print("no matches found, file not created")

    # write non-matching records to output file
    with open(output_nomatch_filename, "w") as outfile_nomatches:
        if len(nomatches) != 0:
            content_nomatches = "".join(nomatches)
            outfile_nomatches.write(content_nomatches)
            print("wrote non-matches to file: ", output_nomatch_filename)
        else:
            print(f"no non-matches found, file not created")

# helper function for splitting content into list
def split_content_into_sections(content, delimiter):
    # get a list of index positions for the start of each section
    section_starts = [m.start() for m in re.finditer(delimiter, content)]

    # get the position of the last character in the input file
    content_end = len(content)
    
    # initialize empty list to collect sections
    sections = []

    # loop through index positions to split into sections
    for i in range(len(section_starts)):
        # start each section on the delimiter
        start = section_starts[i]

        # check if there is another section to find end of the current section
        if len(section_starts) > i+1:
            finish = section_starts[i+1]
        
        # of this is the last section, use end of the content file for end of section
        else:
            finish = content_end

        # slice the content for each section
        section = content[start:finish]

        # add the section to our list
        sections.append(section)
    
    return sections


# this can be run standalong or imported with `from separate_records import separate_records`
if __name__ == "__main__":
    separate_records(input_filename=input_filename, delimiter=delimiter, matcher=matcher, matcher_signifies=matcher_signifies, output_directory=output_directory)