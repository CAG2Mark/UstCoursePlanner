import re
__operators = ["OR", "AND"]

# Cleans (prior to 20xx-xx), (For students without pre-requisites etc)
__comments_pattern = re.compile(r"\s?\([A-Za-z][a-z].+?\)\s?")
__grade_pattern = re.compile(r"Grade ([A-F].?) or above in ")
__course_pattern = re.compile(r"([A-Z]{4} \d{4}[A-Z]?)")

'''
    Test string for formalise_requisite
    :
    (For students without prerequisites) Grade A or above in COMP 2012H AND Grade B+ or above in (ELEC 1100 OR ELEC 1200 OR ELEC 2400 OR ELEC 2410 (prior 2016-17)) AND Grade A- or above in (MATH 2011 OR MATH 2023 OR MATH 2111 (prior 2016-17))
    Becomes:
    A(2012H) AND B+((ELEC1100) OR (ELEC1200) OR (ELEC2400) OR (ELEC2410)) AND A-((MATH2011) OR (MATH2023) OR (MATH2111))
'''

# Makes a pre-requisiite list well-formed.
def formalise_requisite(data):
    # Remove stuff like "(prior to ...)" or "(For students without...)"
    cleaned = re.sub(__comments_pattern, "", data)

    # Adds brackets around singleton courses
    cleaned = re.sub(__course_pattern, r"(\g<0>)", cleaned)
    
    # "Grade A or above in " becomes "A"
    cleaned = re.sub(__grade_pattern, r"\g<1>", cleaned)
    return cleaned

def parse_requisite(data):
    return 

print(formalise_requisite("(For students without prerequisites) Grade A or above in COMP 2012H AND Grade B+ or above in (ELEC 1100 OR ELEC 1200 OR ELEC 2400 OR ELEC 2410 (prior 2016-17)) AND Grade A- or above in (MATH 2011 OR MATH 2023 OR MATH 2111 (prior 2016-17))"))