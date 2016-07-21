#! /usr/bin/env python

import re
import sys
import os
import argparse
import tkinter.ttk
from tkinter import filedialog, messagebox
from html.parser import HTMLParser
from datetime import datetime


def main(agrv):
    parser = argparse.ArgumentParser(description='Read an input file and save the performance data as a csv.')
    parser.add_argument('-i', '--file_name', help='Name of the input file, must be in the current working directory.',
                        dest='infile_name', required=False)
    parser.add_argument('-o', '--output_file_name', help='Name of the output file.', dest='outfile_name',
                        required=False)
    parser.add_argument('-v', '--verbose', help='Run script with increased output.', action='store_true',
                        dest='verbose', required=False)

    args = parser.parse_args()

    if not args.infile_name:
        root = tkinter.Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Choose your file',
                                                   filetypes=(('HTML files', '*.html'), ('all files', '*.*')))
        # if we don't get a filename just bail
        if root.filename:
            args.infile_name = root.filename
        else:
            exit(0)

    # assumes we are inputting html files, else create a file with time stamp as name
    if not args.outfile_name:
        match = re.search('(.*)\.html', args.infile_name)
        if match:
            args.outfile_name = match.group(1) + '.csv'
        else:
            args.outfile_name = 'timeTemp-' + str(datetime.now()) + '.csv'

    with open(str(args.infile_name), 'r') as my_file:
        parser = MyHTMLParser()
        parser.set_output_file(args.outfile_name)
        parser.feed(my_file.read())

    # confirmation dialog because Kristina wanted one
    messagebox.showinfo('File Saved', 'New temperature over time data file saved to:\n' + args.outfile_name)


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.found_temp = False
        self.ready_to_write = False
        self.my_temperature = None
        self.my_date = None
        self.my_time = None
        self.header = 0
        self.outfile_name = None

#    def handle_starttag(self, tag, attrs):
#        print("found a start tag:", tag)

#    def handle_endtag(self, tag):
#        print("found an end tag:", tag)

    def handle_data(self, data):
        temp_match = re.match(r"Current: (-?\d+)", str(data))
        if temp_match:
            self.my_temperature = temp_match.group(1)
            print(temp_match.group(1))

        date_match = re.match\
                (r"(\d{1,2}[./]\d{2}[./]\d{4})\s(\d{2}[.:]\d{2}[.:]\d{2})\s(Will wait for \d{1,2} seconds)", str(data))
        if date_match:
            self.my_date = date_match.group(1)
            self.my_time = date_match.group(2)
            self.ready_to_write = True
            print(date_match.group(1,2))

        if self.ready_to_write:
            local_file = open(self.outfile_name, 'a')
            if self.header == 0:
                local_file.write("Temperature,Date,Time\n")
                self.header = 1

            local_file.write(str(self.my_temperature) + "," + str(self.my_date) + "," + str(self.my_time) + "\n")
            local_file.close()
            self.ready_to_write = False

    def set_output_file(self, out_file):
        self.outfile_name = out_file


if __name__ == "__main__":
    main(sys.argv[1:])
