#! /usr/bin/env python

import sys
import os
import tkinter.ttk
from tkinter import filedialog, messagebox, simpledialog


def main(args):

    root = tkinter.Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Choose your file',
                                               filetypes=(('CSV files', '*.csv'), ('all files', '*.*')))

    root.drive_num = simpledialog.askinteger('How many drives are we collecting?', 'Number of drives.')

    out_file = 'out.csv'
    while root.drive_num <= 1:
        root.drive_num = simpledialog.askinteger("How many drives are we collecting?",
                                                 'Please enter an integer that is above 1')

    with open(root.filename, 'r+') as in_file:
        organize(in_file, out_file, root.drive_num)


def organize(data, out_file, num_drives):
    data_found = False

    with open(out_file, 'a') as out:
        count = 0
        column_count = 0
        split_line = []
        for line in data:
            if line.startswith('TimeStamp') and not data_found and line.__len__() > 50:
                data_found = True
                split_line = line.split(',')
                while column_count < num_drives:
                    out.write(split_line[13] + ',')
                    column_count += 1
                while column_count == num_drives:
                    out.write('\n')
                    column_count = 0
                continue
            elif data_found and line.__len__() > 50:
                print('line len: ' + str(line.__len__()))
                split_line = line.split(',')
                if count == num_drives - 1:
                    out.write(split_line[13] + '\n')
                    count = 0
                    print(line)
                else:
                    print(line)
                    count += 1
                    out.write(split_line[13] + ',')

    messagebox.showinfo("We're Done", "Organisation complete. All changes saved to out.csv! :)")


if __name__ == '__main__':
    main(sys.argv[1:])
