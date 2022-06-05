import re
__operators = ["OR", "AND"]

# Cleans (prior to 20xx-xx), (For students without pre-requisites etc)
__comments_pattern = re.compile(r"\([^Gg][A-Za-z][a-z].+?\)")
__grade_pattern = re.compile(r"[Gg]rade ([A-F].?) or above in ")
__course_pattern = re.compile(r"([A-Z]{4})\s?(\d{4}[A-Z]?)")
__hs_prereq_pattern = re.compile(r"\(?((?:[Aa] passing|[Ll]evel|[Gg]rade).+?(?:AL|HKDSE)[^;)]+)[;)]?")
__slash_repeat_pattern = re.compile(r"([A-Z]{4}\w? [0-9]{4}(?:\s*?\/\s*?[A-Z]{4} [0-9]{4}\w?)+)")

'''
    Test string for formalise_requisite
    :
    (For students without prerequisites) Grade A or above in COMP 2012H AND Grade B+ or above in (ELEC 1100 OR ELEC 1200 OR ELEC 2400 OR ELEC 2410 (prior 2016-17)) AND Grade A- or above in (MATH 2011 OR MATH 2023 OR MATH 2111 (prior 2016-17))
    Becomes:
    A(2012H) AND B+((ELEC1100) OR (ELEC1200) OR (ELEC2400) OR (ELEC2410)) AND A-((MATH2011) OR (MATH2023) OR (MATH2111))
'''

# Makes a pre-requisiite list well-formed.
def formalise_requisite(data):

    cleaned = data.replace("[", "(").replace("]", ")")

    # Clean high school pre-req
    cleaned = re.sub(__hs_prereq_pattern, r"(EXTERN)", data)
    # Capitalise "level" because why not :P
    cleaned = cleaned.replace("level", "Level")

    # remove semicolons
    cleaned = cleaned.replace(";", "")

    # Remove stuff like "(prior to ...)" or "(For students without...)"
    cleaned = re.sub(__comments_pattern, "", cleaned)

    # "Grade A or above in COURSE1 / COURSE2 -> A(COURSE1/COURSE2)"
    cleaned = re.sub(__slash_repeat_pattern, r"(\g<1>)", cleaned)

    # Adds brackets around singleton courses
    cleaned = re.sub(__course_pattern, r"(\g<1> \g<2>)", cleaned)

    # "Grade A or above in " becomes "A"
    cleaned = re.sub(__grade_pattern, r"\g<1>", cleaned)

    # Replace alternative operators with internal ones
    cleaned = cleaned.replace(" OR ", "/").replace(" AND ", "&")
    cleaned = cleaned.replace(" or ", "/").replace(" and ", "&")
    # Strip whitespace
    cleaned = re.sub(r"\s*/\s*", "/", cleaned)
    cleaned = re.sub(r"\s*&\s*", "&", cleaned)
    return cleaned

__grade_start_match = re.compile(r"^([A-z][+-]?)\(")

# Returns whether the first bracket encompasses the whole string.
# Eg: ((a)bc) -> true
# (ab)(c) -> false
def __is_bracket_complete(data):
    ctr = 0
    started = False
    # Scan
    i = 0
    while i < len(data) - 1:
        if data[i] == "(": 
            ctr += 1
            started = True
        elif data[i] == ")": ctr -= 1

        if ctr == 0 and started: return False
        i += 1
    return True
def make_requisite_tree(data):
    print(data)
    # Clean trailing brackets if they match
    while data[0] == "(" and __is_bracket_complete(data):
        data = data[1:-1]
    
    # If terminal node (no brackets)
    if not '(' in data:
        return {"value": data, "children": []}

    # If the input is of the form A(COMP1021) for example
    searched = re.match(__grade_start_match, data)
    if searched and data[0] and __is_bracket_complete(data):
        # Only continue if this grade is applied to the entire string.
        grade = searched.groups()[0]
        return {"value": grade, "children": [make_requisite_tree(data[len(grade):])]}
    
    # Search the string for the first | or &
    i = 0
    L = len(data)
    cntr = 0
    while i < L:
        if data[i] == "(": cntr += 1
        elif data[i] == ")": cntr -= 1
        elif cntr == 0:
            if data[i] == "&" or data[i] == "/": break
        i += 1
    # print(data, i)
    return {"value": data[i], "children": [
        make_requisite_tree(data[0:i]),
        make_requisite_tree(data[i+1:])
    ]}

if __name__ == "__main__":
    data = formalise_requisite("(Grade B+ or above in COMP 2011 / COMP 2012 / COMP 2012H) AND (grade A- or above in COMP 2711 / COMP 2711H / MATH 2343)")
    print(data)
    print(make_requisite_tree(data))