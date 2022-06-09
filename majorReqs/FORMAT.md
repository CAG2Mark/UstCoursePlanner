# Preamble
At the start of the document, you must declare the human-readable name of the major and a computer-friendly code (ie, one without spaces).

For example, for COMP:
```
!NAME BEng COMP
!CODE COMP
```

Different tracks/options within majors will be declared later.
# Course Requirements
Each line indicates the start of a new requirement.

For example, this would be written as a single requirement.

![SENG Requirement](https://user-images.githubusercontent.com/55091936/172810926-8b5fadc9-4568-4c22-a918-a272714d6c80.png)


It could be written as:

```
COMP 1021 OR BIEN 1010 OR CENG 1000 OR CIVL 1100 OR ELEC 1100 OR ELEC 1200 OR ENGG 1100 OR IEDA 2010 OR IEDA 2200 OR ISDN 1002 OR ISDN 1006 OR MECH 1901 OR MECH 1902 OR MECH 1905 OR MECH 1906 OR MECH 1907 OR COMP1022P OR COMP1022Q
```

This requirmement can be evaluated by substituting **TRUE** into a course that a student has taken, and **FALSE** into any other course.

For example, if a student has taken `COMP 1021` but not `ELEC 1200`, then the following requiremenent can be evaluated like so:

```
= COMP 1021 OR ELEC 1200
= TRUE OR FALSE
= TRUE
```

Course requirements should be written using `OR`, `AND`  operators in infix notation, and any combination of the following brackets: `(`, `[`. Operators may be evaluated in any order, ie. left-to-right or right-to-left is not guaranteed.

# Comments
Comments begin with `#`. Any text after `#` will be ignored.

# Major Tracks/Options
Some majors like MATH or MECH may have different options for students to choose from.  Options must be defined at the **end** of the file. To define the start of an option, use the following syntax:

```
!OPTION <name>
```

For example, to begin the MATH(CS) option inside the MATH major requirement file, use:

```
!OPTION CS
```

Everything after this, and until the next `!OPTION` tag or the end of file, will be treated as requirements the MATH(CS) option.

After defining all the options, you **must** use the `Option()` function to declare the option as part of the overall major requirement. For example, for MATH, you must type this **before** writing any `!OPTION`:

```
Option(APPLIED) OR Option(CS) OR Option(GM) OR Option(IRE) OR Option(PHYS) OR Option(PMA) OR Option(PM) OR Option(STATFIN)
```

# Electives
## Level X000 or above electives
If, for example, a requirement states you need one COMP elective of 2000-level or above, use the following syntax:

```
Electives(1, COMP, 2000)
```

* The first parameter specifies the number of credits. 
* The second parameter specifies the department. 
* The third parameter specifices the level requirement of the elective.

## Elective from multiple areas
Consider the following requirement:

![Elective Requirement](https://user-images.githubusercontent.com/55091936/172811017-54426178-3cf6-41ba-b64b-d0b4d77a0857.png)


When encountring such a requirement, one must first define the different elective groups like so:

```
aiArea = {COMP 3211, COMP 3721, COMP 4211, (... and so on)}
multimediaArea = {COMP 4411, COMP 4421, COMP 4421 (... and so on)}
softwareArea = {COMP 3021, COMP 3031, COMP 3311 (... and so on)}
networkingArea = {COMP 3632, COMP 4511, COMP 4521 (... and so on)}
```

Then, you can use this syntax to describe the above requirement:

```
ElectiveAreas(5, 3, {aiArea, multimediaArea, softwareArea, networkingArea})
```

* The first parameter specifies the number of courses needed. 
* The second parameter specifies how many courses need to be taken from one area. 
* The third parameter specifices the list of areas one can choose from.

The `Electives()` and `ElectiveAreas()` functions may be treated like an individual "object". For example, you can do things like `COMP 2011 OR Elective(...)`.

One place where this may be useful is the MATH(CS) major requirements:
![MATH CS Requirement 1](https://user-images.githubusercontent.com/55091936/172811138-0d927768-c78f-4c95-84c0-15de9c4a2536.png)
![MATH CS Requirement 2](https://user-images.githubusercontent.com/55091936/172811145-a829a373-8aef-4eeb-9044-6cc5ee220bb3.png)


To handle something like this, you could combine these two requirements into one requirement like so:
```
(COMP 2011 AND COMP 2012) OR (COMP2012H AND Elective(1, COMP, 2000))
```

## Tracks/options referencing other tracks/options
Consider the following option in the MATH+IRE track:

When encountering this, one should simply use the `Option()` function to reference the requirements of another option. In this example, it should be specified like this
![Math IRE requirement](https://user-images.githubusercontent.com/55091936/172811207-f8b15bd8-c26d-4493-99a8-fc8318fd612b.png)
```
[Option(PMA) OR Option(APPLIED) OR Option(STATFIN)] AND MATH 2431
```
