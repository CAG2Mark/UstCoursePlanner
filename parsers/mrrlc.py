#!/usr/bin/env python3

# Major requirement representation language compiler

# Note: this is very much thrown together and is not efficient or beautiful :)

from ast import Expression
import sys
import os
import logging
import re
import json
import argparse
from typing import List, Tuple
import requisite_parser
logging.basicConfig(format='%(levelname)s - %(message)s')

comment_pattern = re.compile(r"(?<!\<)#.*$")
assignment_pattern = re.compile(r"^([A-Za-z][A-Za-z\s]*?)\s*=\s*(.*)$")
flag_pattern = re.compile(r"^!(.+?)\s(.+)$")
or_pattern = re.compile(r"\sOR\s")
and_pattern = re.compile(r"\sAND\s")
course_pattern = re.compile(r"([A-Z]{4})\s?(\d{4}[A-Z]?)")
not_in_bracket_pattern = re.compile(r",(?![^\{]*\})(?![^\(]*\))")

bracket_map = {"{": "}", "(": ")", "[": "]", "<": ">"}

class MajorReqParser:
    """Class that will parse a single major requirement file in the format specified by https://github.com/CAG2Mark/UstCoursePlanner/blob/master/majorReqs/README.md.
    """

    def __init__(self) -> None:
        self.name_dict = {}
        self.major_options = {}
        self.cur_option_name = ""
        self.cur_option = {}
        self.error = False
        self.line_map = {}

        # note: bad practice usually... in this case it's small enough scale and I'm lazy :P
        self.__functions = {
            "noOfCourses": self.no_of_courses_fn,
            "fromEach": self.from_each_fn,
            "fromSpecific": self.from_specific_fn,
            "fromGroup": self.from_group_fn,
            "Electives": self.electives_fn,
            "Option": self.option_fn
        }

        self.__function_parameters = {
            "noOfCourses": (1,2),
            "fromEach": (1,2),
            "fromSpecific": (1,3),
            "fromGroup": (2,4),
            "Electives": (2,3),
            "Option": (1,2)
        }

        self.requirements = []

        def expr_callback_static(token):
            return self.__evaluate_token(token)

        self.__evaluate_token_static = expr_callback_static

    def read_file_lines(self, file_name:str) -> List[str]:
        """Reads the lines of a file given an input file name.

        Args:
            file_name (str): The name of the file.
        
        Returns:
            List[str]: The lines of the file.
        """
        if not os.path.exists(file_name):
            logging.error(f"File {file_name} does not exist!")
            return None
        
        return open(file_name).readlines()

    def __print_error_pos(self, line_no:int, pos:int, message:str) -> None:
        """Prints an error message at a specified line at a specified position.

        Args:
            line_no (int): The line number.
            pos (int): The position of the error.
            message (str): The error message.
        """

        for i in range(max(0, line_no - 2), line_no+1):
            print(f"{i+1}\t{self.lines_og[i].rstrip()}")
        
        if pos != -1:
            spaces = " "*pos
            print(f"\t{spaces}^")
        else:
            print()
        spaces_msg = " "*(pos - len(message)//2)
        print(f"\t{spaces_msg}{message}")

    def __print_error_lines(self, line_range:Tuple[int, int], message:str) -> None:
        for i in range(line_range[0], line_range[0] + line_range[1] + 1):
            print(f"{i+1}\t{self.lines_og[i].rstrip()}")
    
        print()
        print(f"\t{message}")

    def preprocess(self, lines:List[str]) -> List[str]:
        """Strips comments, right whitespace, and empty lines from a given list of lines. Also pre-processes expressions to be readable by the parser.

        Args:
            lines (List[str]): The lines to strip.


        Returns:
            List[str]: The stripped lines.
        """
        new_lines = []

        last_line = ""

        line_cnt = 0

        line_compress_cnt = 0

        # Find last unclosed bracket for finding error messages
        # counter, last open line, last closed line
        bracket_stack = []
        for i, ln in enumerate(lines):
            for j, ch in enumerate(ln):
                if ch in bracket_map.keys(): 
                    # special case: ignore when inside "<" and ">"
                    if bracket_stack and bracket_stack[-1][0] == "<": continue

                    bracket_stack.append((ch, i, j))
                elif ch in bracket_map.values():
                    if not bracket_stack:
                        logging.error("could not find opening bracket!")
                        print()
                        self.__print_error_pos(i, j, "could not find opening bracket")
                        return None

                    last = bracket_stack.pop()
                    if ch != bracket_map[last[0]]:
                        logging.error("brackets do not match!")
                        print()
                        self.__print_error_pos(last[1], last[2], "opening bracket")
                        self.__print_error_pos(i, j, "closing bracket (error!)")
                        return None
            
                # print(normal_bracket_track, curly_bracket_track)

            ln = ln.replace("[", "(").replace("]", ")") # Square brackets are the same as normal brackets
            ln = re.sub(comment_pattern, "", ln)

            ln = ln.rstrip()

            # If there is a bracket waiting to be closed
            if bracket_stack:
                last_line += ln
                line_compress_cnt += 1
                continue
            
            if ln: 
                new_lines.append(last_line + ln)
                self.line_map[line_cnt] = (i - line_compress_cnt, line_compress_cnt)
                line_compress_cnt = 0
                line_cnt += 1
                last_line = ""
        
        # Unclosed bracket, throw error
        if bracket_stack:
            logging.error("bracket not closed!")
            print()
            last = bracket_stack.pop()
            self.__print_error_pos(last[1], last[2], "this bracket is not closed")
            return None

        return new_lines

    def __handle_flag(self, flag:str, value:str) -> None:
        """Handles a flag match after feeding in a line.

        Args:
            flag (str): The flag.
            value (str): The value of the flag.
        """
        if flag == "NAME":
            self.major_name = value
        elif flag == "CODE":
            self.major_code = value
        elif flag == "OPTION":
            # Add the option currently being read
            if self.cur_option_name:
                self.major_options[self.cur_option_name] = self.cur_option 

            self.cur_option_name = value
            self.cur_option = {}

    # Small enough scale, can handle each function properly :P In the future may be good to introduce a typing system.
    def no_of_courses_fn(self, param_list:List[str]):
        return {
            "type": "restriction",
            "fn": "noOfCourses",
            "N": self.__evaluate_token(param_list[0])
        }
        pass
    def from_each_fn(self, param_list:List[str]):
        return {
            "type": "restriction",
            "fn": "fromEach",
            "N": self.__evaluate_token(param_list[0])
        }
        
    def from_specific_fn(self, param_list:List[str]):
        if len(param_list) == 2:
            M = self.__evaluate_token(param_list[1])
        else:
            M = 65535
        return {
            "type": "restriction",
            "fn": "fromSpecific",
            "N": self.__evaluate_token(param_list[0]),
            "M": M
        }

    def parse_item_or_list(self, token):
        val = self.__evaluate_token(token)
        # List of list
        if isinstance(val, list) and len(val) > 0 and isinstance(val[0], list): return val
        else: return [val]
    
    def from_group_fn(self, param_list:List[str]):
        # parse list of courses
        courses = self.parse_item_or_list(param_list[0])
        N = self.__evaluate_token(param_list[1])
        if len(courses) == 0:
            self.error = True
            logging.error("there must be at least one course for a fromGroup function!")
            print()
            self.__print_error_lines(self.line_map[self.line_no], "there must be at least one course here")
            return None
        if len(param_list) == 3:
            M = self.__evaluate_token(param_list[2])
        else:
            M = 65535
        return {
            "type": "restriction",
            "fn": "fromGroup",
            "courses": courses,
            "N": N,
            "M": M
        }
        
    def electives_fn(self, param_list:List[str]):
        # parse list of courses
        courses = self.parse_item_or_list(param_list[0])
        if len(courses) == 0:
            self.error = True
            logging.error("there must be at least one course for an Electives function!")
            print()
            self.__print_error_lines(self.line_map[self.line_no], "there must be at least one course here")
            return None
        restrictions = self.parse_item_or_list(param_list[1])
        if len(restrictions) == 0:
            self.error = True
            logging.error("there must be at least one restriction for an Electives function!")
            print()
            self.__print_error_lines(self.line_map[self.line_no], "there must be at least one restriction here")
            return None
        return {
            "type": "electives",
            "courses": courses,
            "restrictions": restrictions
        }
    

    def option_fn(self, param_list:List[str]):
        return {
            "type": "option",
            "option": param_list[0]
        }

    def __evaluate_expression(self, expression:str):
        return requisite_parser.make_expr_tree(expression, self.__evaluate_token_static)

    def __evaluate_token(self, token:str):
        token = token.strip()

        if token in self.name_dict:
            return self.name_dict[token]

        # Handle digit
        if token.isdigit():
            return int(token)

        # special case: "infinity"
        if token == "infinity":
            return 65535

        # Handle list
        if token[0] == "{" and requisite_parser.is_bracket_complete(token, ("{", "}")):
            token = token[1:-1]
            token = re.split(not_in_bracket_pattern, token)
            vals = []

            for e in token:
                vals.append(self.__evaluate_expression(e))
        
            return vals
        
        # Handle functions
        for fn_name in self.__functions:
            if token.startswith(fn_name):
                params = token[len(fn_name):].strip()[1:-1]
                param_list = re.split(not_in_bracket_pattern, params)
                
                # Check parameter count
                l = len(param_list)
                p = self.__function_parameters[fn_name]
                if not (p[0] <= l < p[1]):
                    logging.error(f"incorrect number of parameters for function {fn_name}!")
                    self.error = True
                    print()
                    cnt_text = str(p[0]) if p[0] == p[1] - 1 else f"{p[0]} to {p[1]-1}"
                    self.__print_error_lines(self.line_map[self.line_no], f"expected {cnt_text} parameter(s), received {l}")
                    return None
                return self.__functions[fn_name](param_list)

        return token


    def __handle_assignment(self, key:str, value:str) -> None:
        """Handles assignment after feeding in a line.

        Args:
            key (str): The key for the value to be assigned to.
            value (str): The value to be assigned.
        """
        # print("assign", key, value)
        
        self.name_dict[key] = self.__evaluate_expression(value)

    def feed_line(self, line:str, line_no:int) -> None:
        """Feeds in a line to the parser.

        Args:
            line (str): The text to feed in.
            line_no (int): The line number.
        """

        self.line_no = line_no
        
        flag_match = re.match(flag_pattern, line)
        if flag_match:
            groups = flag_match.groups()
            self.__handle_flag(groups[0], groups[1])
            return
        
        assign_match = re.match(assignment_pattern, line)
        if assign_match:
            groups = assign_match.groups()
            self.__handle_assignment(groups[0], groups[1])
            return

        # Replace OR with &, AND with &
        line = re.sub(or_pattern, "/", line)
        line = re.sub(and_pattern, "&", line)

        val = self.__evaluate_expression(line)
        self.requirements.append(val)
    
    def compile_file(self, file_name) -> None:
        """Compiles a major requirement file into JSON.

        Args:
            file_name (_type_): The name of the file to compile.
        """
        lines = self.read_file_lines(file_name)
        self.lines_og = lines
        lines = self.preprocess(lines)

        self.lines = lines

        if not lines: 
            self.error = True
            return

        for i, ln in enumerate(lines):
            self.feed_line(ln, i)
        
        # Add the final option, if it exists
        if self.cur_option_name:
            self.major_options[self.cur_option_name] = self.cur_option 

if __name__ == "__main__":

    ap = argparse.ArgumentParser(description='Compile a major requirement to JSON.')
    ap.add_argument('file', metavar="F", type=str,
                        help='The major requirement file to be compiled')

    ap.add_argument('-o', type=str,
                        help='The file to output the JSON to.', default="major_req.json")

    args = ap.parse_args()
    
    p = MajorReqParser()

    file = args.file

    p.compile_file(file)

    if p.error: sys.exit(1)

    final = {
        "name": p.major_code,
        "code": p.major_code,
        "requirements": p.requirements,
        "options": p.major_options 
    }

    with open(args.o, "w") as f:
        f.write(json.dumps(final))

