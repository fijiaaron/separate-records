# separate-records

This contains both a python script that can be run from the command line:

    python separate_records.py -f DX-XF-FF.txt

and a Windows executable version that can be run from the command line:
    
    separate_records.exe -f DX-XF-FF.txt

### command line options options

    python separate_records.py -h

    usage: separate_records.py [-h] [-f FILENAME] [-o OUTPUT] [-d DELIMITER] [-m MATCHER]

    options:
    -h, --help            show this help message and exit
    -f FILENAME, --filename FILENAME
                            input file, default: DX-XF-FF.txt
    -o OUTPUT, --output OUTPUT
                            output directory, default: .
    -d DELIMITER, --delimiter DELIMITER
                            token to delimit records, default: //STX12
    -m MATCHER, --matcher MATCHER
                            token to seek a match in records, default: 1280001

### example with all options

    separate_records.exe -f c:\input_directory\DX-XF-FF.txt -o c:\output_directory -d //STX12 -m 1280001

### set default values in separate_records.ini

    [SETTINGS]
    delimiter = //STX12
    matcher = 1280001
    matcher_signifies = Thailand
    input_filename = DX-XF-FF.txt
    output_directory = .
    file_ext = .080
