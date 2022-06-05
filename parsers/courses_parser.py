import requests
import re
from html.parser import HTMLParser
import requisite_parser

course_pattern = re.compile(r"(^.{0,4}) (\d{0,4}[A-Z]?) - (.*) \((\d+) units?\)")

modes = ["CO-REQUISITE", "PRE-REQUISITE", "EXCLUSION", "ATTRIBUTES", "DESCRIPTION"]
mode_name_map = {
    "CO-REQUISITE": "coReqs", 
    "PRE-REQUISITE": "preReqs",
    "EXCLUSION": "excls",
    "ATTRIBUTES": "attrs", 
    "DESCRIPTION": "description"
}
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

    def handle_data(self, data):
        # If a course title is found.
        searched = re.match(course_pattern, data)
        if (searched): # Matched start of course
            details = searched.groups() 
            course = {}
            self.cur_course = {}
            # Set data
            course["dept"] = details[0]
            course["code"] = details[1]
            course["title"] = details[2]
            course["credits"] = int(details[3])

        # If a mode was previously set
        if self.mode:
            # Reset the mode.
            self.mode = None

        # Set mode to capture data on the next data handle, see the above example data stream
        if data in modes:
            self.mode = data
    

dept = input() # Eg: COMP, MATH, ACCT
year = input() # Eg: Fall 2021 -> 2110, Spring 2022: 2130

url = f"https://w5.ab.ust.hk/wcq/gci-bin/{year}/subject/{dept}"

# text = requests.get(url)
text = open("testdata").read()

parser = CourseHTMLParser()
parser.feed(text)