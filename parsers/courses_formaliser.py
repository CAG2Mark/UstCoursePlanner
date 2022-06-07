import json
from threading import main_thread
import requisite_parser
import re

with open("data_dump.json") as f:
    all_courses = json.load(f)

# Courses that need to be handled manually
special_cases = [
    "LANG 3021",
    "LANG 4030",
    "ISOM 3230",
    "SCIE 3500",
    "ACCT 2200",
    "CHEM 4640",
    "MGMT 2130"
]

# Manual changes made to fix their inconsistent formatting.
# This is for weird formats that don't come up often enough to code a special case for
# code, pre_req, co_req
manual_changes = [
    ("MARK 4210", "MARK 2120 and MARK 3220 and MARK 3420", None),
    ("SCIE 3110", "Level 4 or above in HKDSE 1x Physics OR Level 4 or above in HKDSE 1x Chemistry OR Level 4 or above in HKDSE Mathematics M1/M2", None),
    ("FINA 5840", "FINA 5120 and FINA 5210 and FINA 5290", None),
    ("ECON 3014", "ECON 2103 OR ECON 2113", None),
    ("ECON 3334", "ISOM 2500 or MATH 2411 or MATH 3423", None),
    ("ECON 4234", "ECON 3113 or ECON 3014", None),
    ("ECON 4474", "ECON 2103 OR ECON 2113 OR ECON 3113 AND (ECON 2123 OR ECON 3123)", None),
    ("FINA 7900C", "FINA 7900A", None),
    ("FINA 7900D", "FINA 7900B", None),
    ("PHYS 3053", "Grade B- or above in PHYS 1114 OR PHYS 1314", None)
]

for change in manual_changes:
    course = all_courses[change[0]]
    if change[1]: course["preReqs"] = change[1]
    if change[2]: course["coReqs"] = change[2]

__cga_prereq_pattern = re.compile(r"^CGA at ([0-9\.]+?) or above$")
__cc_pattern = re.compile(r"Common Core \(((?:SSC)?)-?(.+)\) for 4Y programs")

for code, item in all_courses.items():
    if code in special_cases: 
        item["handleReqsManually"] = True
        continue

    # Add missing fields if not there
    fill_fields = ["coReqs", "excls", "preReqs"]
    for f in fill_fields:
        if not f in item: item[f] = ""

    # Special case: Co-reqs only required if student has no pre-reqs
    item["coReqIfNoPrereq"] = "without prerequisites" in item["coReqs"]

    # Special cases: CGA
    cga_match = re.match(__cga_prereq_pattern, item["preReqs"])
    if cga_match:
        item["cgaReq"] = float(cga_match.groups()[0])
        item["preReqs"] = ""

    item["preReqs"] = requisite_parser.parse_prereq(item["preReqs"])
    item["coReqs"] = requisite_parser.parse_prereq(item["coReqs"])

    if item["excls"].strip():
        item["excls"] = requisite_parser.parse_excl(item["excls"])
    else:
        item["excls"] = []
    
    # Handle CC status
    item["ccType"] = ""
    item["isSsc"] = False

    if not "attrs" in item: continue

    for p in item["attrs"]:
        searched = re.match(__cc_pattern, p)
        if not searched: continue

        details = searched.groups()
        item["ccType"] = details[1]
        item["isSsc"] = not not details[0]

    

with open("allCourses.json", "w") as f:
    f.write(json.dumps(all_courses, indent=4))