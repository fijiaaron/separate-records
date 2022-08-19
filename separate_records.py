# separate_records.py
# usage:
#   python separate_records.py [-f INPUT_FILENAME -o OUTPUT_DIRECTORY -d DELIMITER -m MATCHER] 

import os
import re

delimiter = "//STX12"
matcher = "1280001"
matcher_signifies = "Thailand"
input_filename = "DX-XF-FF.txt"
output_directory = "."
file_ext = ".080"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', type=str, default=input_filename, help=f"input file, default: {input_filename}")
parser.add_argument('-o',  '--output', type=str, default=output_directory, help=f"output directory, default: {output_directory}")
parser.add_argument('-d', '--delimiter', type=str, default=delimiter, help=f"token to delimit records, default: {delimiter}")
parser.add_argument('-m',  '--matcher', type=str, default=matcher, help=f"token to seek a match in records, default: {matcher}")
args = parser.parse_args()

try: 
    input_filename = args.filename    
    output_directory = args.output
    delimiter = args.delimiter
    matcher = args.matcher
except ImportError:
    print("using default options")

def separate_records(input_filename=input_filename, delimiter=delimiter, matcher=matcher, matcher_signifies=matcher_signifies, output_directory=output_directory):

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
        sections = split_content_into_sections(content, delimiter)

        for section in sections:
            if matcher in section:
                matches.append(section)
            else:
                nomatches.append(section)

    print(f"sections containing `{matcher}`:", len(matches))
    print(f"sections not containing `{matcher}:`", len(nomatches))
    print(f"total sections: ", len(sections))

    # write matching records to output file
    with open(output_match_filename, "w") as outfile_matches:
        if len(matches) != 0:
            content_matches = "".join(matches)
            outfile_matches.write(content_matches)
            print("wrote matches to file: ", output_match_filename)
        else:
            print("no matches found, file not created: ", output_match_filename)

    # write non-matching records to output file
    with open(output_nomatch_filename, "w") as outfile_nomatches:
        if len(nomatches) != 0:
            content_nomatches = "".join(nomatches)
            outfile_nomatches.write(content_nomatches)
            print("wrote non-matches to file: ", output_nomatch_filename)
        else:
            print(f"no non-matches found, file not created:", output_nomatch_filename)


def split_content_into_sections(content, delimiter):
    section_starts = [m.start() for m in re.finditer(delimiter, content)]
    content_end = len(content)
    
    sections = []
    for i in range(len(section_starts)):
        start = section_starts[i]
        if len(section_starts) > i+1:
            finish = section_starts[i+1]
        else:
            finish = content_end
        section = content[start:finish]
        sections.append(section)
    
    return sections

if __name__ == "__main__":
    separate_records(input_filename=input_filename, delimiter=delimiter, matcher=matcher, matcher_signifies=matcher_signifies, output_directory=output_directory)