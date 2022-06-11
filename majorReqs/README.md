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
COMP 1021 OR BIEN 1010 OR CENG 1000 OR CIVL 1100 OR ELEC 1100 OR ELEC 1200 OR ENGG 1100 OR IEDA 2010 OR IEDA 2200 OR ISDN 1002 OR ISDN 1006 OR MECH 1901 OR MECH 1902 OR MECH 1905 OR MECH 1906 OR MECH 1907 OR COMP 1022P OR COMP 1022Q
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

# Electives

The `Electives()` function handles all electives.

The function has parameters as follows:

```
Electives(elective group OR list of elective groups, restrictions OR list of restrictions)
```
## Elective Groups
**Elective groups** can be defined using the following syntax:
```
electiveGroup = {COMP 2011, COMP 2012, COMP 2012H}
```
All together, these form what is called an **elective group**. There are also pre-defined elective groups, such as:
* `COMP2XXX` meaning COMP 2000-level or above electives
* `SSCI4XXX` meaning School of Science 2000 or above electives
* All other departments and schools's electives can be written in this format

## Restrictions
**Restrictions** stipulate certain requirement or restrictions on which courses can and cannot be taken to fulfill an elective
requirement. The following restrictions are available:

---
```
noOfCourses(N)
```
This means at least `N` courses must be taken from the elective group(s) specified.

---
```
fromEach(N)
```
This means at least `N` courses must be taken **from each** specified elective group.

---
```
fromSpecific(N, M=1)
```
This means at least `N` courses must be taken from `M` specific elective groups.

---
```
fromGroup(elective group or list of elective groups, N, M=infinity)
```
This means that, from the specified list of elective groups:
* You must take at least N courses from these elective group(s)
* No more than M courses from these elective group(s) may be used to satisfy this overall elective requirement

## Other properties of the electives functions

The `Electives()` and `ElectiveAreas()` functions may be treated like an individual "object". For example, you can do things like `COMP 2011 OR Electives(...)`.

One place where this may be useful is the MATH(CS) major requirements:
![MATH CS Requirement 1](https://user-images.githubusercontent.com/55091936/172811138-0d927768-c78f-4c95-84c0-15de9c4a2536.png)
![MATH CS Requirement 2](https://user-images.githubusercontent.com/55091936/172811145-a829a373-8aef-4eeb-9044-6cc5ee220bb3.png)
To handle something like this, you could combine these two requirements into one requirement like so:
```
(COMP 2011 AND COMP 2012) OR (COMP2012H AND Electives({COMP2XXX}, noOfCourses(1))
```

Note that courses may **not** be re-used within `ElectiveAreas()`. This makes it useful to handle cases like:
```
MATH Depth Electives (1 course from the specified elective list.
Students may use MATH 4424 to count towards either, but not
both, the MATH Depth Elective or the Statistics or Financial
Mathematics Elective requirement.)
```
In this case, you can just use the `ElectiveAreas` function and you would not have to worry about MATH 4424 counting towards both.

## Example
![COMP Electives](https://user-images.githubusercontent.com/55091936/173176406-4090a88c-224e-4ccc-8adc-6976705dcd99.png)

In this case:
```
aiArea = ... # These need to be defined
graphicsArea = ...
softwareArea = ...
networkingArea = ...
deepLearning = {COMP 4471, COMP 5523}

Electives({aiArea, graphicsArea, softwareArea, networkingArea}, {
    noOfCourses(5), # total number of courses >= 5
    fromSpecific(3), # 3 from one specific area
    fromGroup(deepLearning, 0, 1) # no more than one deep learning elective
})
```

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

## Tracks/options referencing other tracks/options
Consider the following option in the MATH+IRE track:

When encountering this, one should simply use the `Option()` function to reference the requirements of another option. In this example, it should be specified like this
![Math IRE requirement](https://user-images.githubusercontent.com/55091936/172811207-f8b15bd8-c26d-4493-99a8-fc8318fd612b.png)
```
[Option(PMA) OR Option(APPLIED) OR Option(STATFIN)] AND MATH 2431
```
