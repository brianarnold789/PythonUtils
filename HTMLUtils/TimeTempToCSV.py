#! /usr/bin/env python

from html.parser import HTMLParser
import re


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.found_temp = False
        self.ready_to_write = False
        self.my_temperature = None
        self.my_date = None
        self.my_time = None

#    def handle_starttag(self, tag, attrs):
#        print("found a start tag:", tag)

#    def handle_endtag(self, tag):
#        print("found an end tag:", tag)

    def handle_data(self, data):
        temp_match = re.match(r"Current: (\d+)", str(data))
        if temp_match:
            self.my_temperature = temp_match.group(1)
            # print(temp_match.group(1))

        date_match = re.match\
                (r"(\d{1,2}[./]\d{2}[./]\d{4})\s(\d{2}[.:]\d{2}[.:]\d{2})\s(Will wait for \d{1,2} seconds)", str(data))
        if date_match:
            self.my_date = date_match.group(1)
            self.my_time = date_match.group(2)
            self.ready_to_write = True
            # print(date_match.group(1,2))

        if self.ready_to_write:
            local_file = open('new.txt', 'a')
            local_file.write(self.my_temperature + "," + self.my_date + "," + self.my_time + "\n")
            local_file.close()
            self.ready_to_write = False


with open('../TestFiles/sample.html', 'r') as my_file:
    parser = MyHTMLParser()
    parser.feed(my_file.read())
