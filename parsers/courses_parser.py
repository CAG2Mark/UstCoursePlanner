import re
from html.parser import HTMLParser
import requisite_parser
import os
import json

course_pattern = re.compile(r"(^.{0,4}) (\d{0,4}[A-Z]?) - (.*) \((\d+) units?\)")

data_path = "scraped/data"
files = os.listdir(data_path)

ignore_modes = ["VECTOR", "PREVIOUS CODE"]

modes = ["CO-REQUISITE", "PRE-REQUISITE", "EXCLUSION", "ATTRIBUTES", "DESCRIPTION"]
mode_name_map = {
    "CO-REQUISITE": "coReqs", 
    "PRE-REQUISITE": "preReqs",
    "EXCLUSION": "excls",
    "ATTRIBUTES": "attrs", 
    "DESCRIPTION": "description"
}

all_courses = {}

# Stores data provided by 151044
prev_data = {}

'''
    Example data stream:

    ATTRIBUTES
    Common Core (QR) for 4Y programs
    PRE-REQUISITE
    A passing grade in AL Pure Mathematics/AL Applied Mathematics; OR level 3 or above in HKDSE Mathematics Extended Module M1/M2
    CO-REQUISITE
    (For students without prerequisites) MATH 1012 OR MATH 1013 OR MATH 1014 OR MATH 1020 OR MATH 1023 OR MATH 1024
    EXCLUSION
    COMP 2711H, MATH 2343
    DESCRIPTION
    Basic concepts ...
'''
class CourseHTMLParser(HTMLParser):
    def __init__(self):
        self.course_dict = {}
        super().__init__()
        self.mode = None
        self.cur_course = {}

    def handle_data(self, data):
        # If a course title is found.
        searched = re.match(course_pattern, data)
        if (searched): # Matched start of course
            details = searched.groups() 
            course = self.cur_course
            # Set data
            course["dept"] = details[0]
            course["code"] = details[1]
            course["title"] = details[2]
            course["credits"] = int(details[3])

            code = details[0] + " " + details[1]

            if not code in all_courses:
                all_courses[code] = course

            self.cur_course = {}

        # if it is an ignored mode
        if self.mode and self.mode in ignore_modes:
            self.mode = None

        # If a mode was previously set
        if self.mode:
            prop = mode_name_map[self.mode]

            # As there may be multiple attributes 
            if self.mode == "ATTRIBUTES" and not data.strip() in modes:
                if not prop in self.cur_course: self.cur_course[prop] = []
                self.cur_course[prop].append(data)
            elif not data.strip() in modes:
                self.cur_course[prop] = data
                self.mode = None

        # Set mode to capture data on the next data handle, see the above example data stream
        if data in modes or data in ignore_modes:
            self.mode = data

p = CourseHTMLParser()

for f in files:
    with open(f"scraped/data/{f}") as o:
        p.feed(o.read())

with open("data_dump.json", "w") as f:
    f.write(json.dumps(all_courses))