#!/usr/bin/env python3

# Major requirement representation language compiler

# Note: this is very much bodged and is not efficient :)

import sys
import os
import logging
import re
from typing import List
import requisite_parser
logging.basicConfig(format='%(levelname)s - %(message)s')

comment_pattern = re.compile(r"(?<!\<)#.*$")
assignment_pattern = re.compile(r"^([A-Za-z][A-Za-z\s]*?)\s*=\s*(.*)$")
flag_pattern = re.compile(r"^!(.+?)\s(.+)$")
or_pattern = re.compile(r"\sOR\s")
and_pattern = re.compile(r"\sAND\s")
course_pattern = re.compile(r"([A-Z]{4})\s?(\d{4}[A-Z]?)")

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

        def expr_callback_static(expr):
            self.__evaluate_expression(expr)

        self.__evaluate_expression_static = expr_callback_static

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
            print(f"{i+1}\t{self.lines[i].rstrip()}")
        spaces = " "*pos
        print(f"\t{spaces}^")
        spaces_msg = " "*(pos - len(message)//2)
        print(f"\t{spaces_msg}{message}")
        

    def preprocess(self, lines:List[str]) -> List[str]:
        """Strips comments, right whitespace, and empty lines from a given list of lines. Also pre-processes expressions to be readable by the parser.

        Args:
            lines (List[str]): The lines to strip.


        Returns:
            List[str]: The stripped lines.
        """
        new_lines = []

        last_line = ""

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
                continue
            
            if ln: 
                new_lines.append(last_line + ln)
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
    
    def __evaluate_expression(self, expression):

        return expression

    def __handle_assignment(self, key, value) -> None:
        """Handles assignment after feeding in a line.

        Args:
            key (_type_): The key for the value to be assigned to.
            value (_type_): The value to be assigned.
        """
        # print("assign", key, value)

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

        tree = requisite_parser.make_requisite_tree(line, self.__evaluate_expression_static)
    
    def compile_file(self, file_name) -> None:
        """Compiles a major requirement file into JSON.

        Args:
            file_name (_type_): The name of the file to compile.
        """
        lines = self.read_file_lines(file_name)
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

    args = sys.argv
    if len(args) < 2:
        logging.fatal("No input files.")
        sys.exit(1)
    
    p = MajorReqParser()

    file = args[1]

    p.compile_file(file)

    if p.error: sys.exit(1)