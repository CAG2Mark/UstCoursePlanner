# UstCoursePlanner
Course planner for HKUST to automatically handle major, minor, extended major and universal graduation requirements.

Roadmap:
- Scrape and parse all HKUST courses in the 2021-2022 term (plus 3711H) (Done!)
- Build language for creating major requirements (not done)
- Create major requirements (ongoing effort)
- Build the actual web app (in progress)

# Special Thanks
Special thanks to some of my peers https://github.com/151044 and https://github.com/TheHakkaman for helping scrape some of the course data
and digging out some weird formatting that I eventually parsed.

# I want to use the course data!
Please do! I don't want you to go through the pain of parsing their horribly inconsistent formatting :P. 
This entire repo is licensed under the GPL v3 license, so use the data however you wish within the guidelines of the license.
The data is in `data/courses.json`.

Each course is stored in the following JSON format (take COMP2711 as an example):
```json
"COMP 2711": {
    "attrs": [
        "Common Core (QR) for 4Y programs"
    ],
    "preReqs": ...,
    "coReqs": ...,
    "excls": [
        "COMP 2711H",
        "MATH 2343"
    ],
    "description": "Basic concepts in discrete mathematics needed for the study of computer science: enumeration techniques, basic number theory, logic and proofs, recursion and recurrences, probability theory and graph theory. The approach of this course is specifically computer science application oriented.",
    "dept": "COMP",
    "code": "2711",
    "title": "Discrete Mathematical Tools for Computer Science",
    "credits": 4,
    "coReqIfNoPrereq": true,
    "ccType": "QR",
    "isSsc": false
}
```
## Explanation of some paramaters
- `coReqIfNoPrereq` is a special parameter for courses where a student will need the co-requisite courses **if and only if** they do not have the pre-requiisite courses.
- Some courses will have the property `handleReqsManually` set to `true`. These are courses that have school/major-sepcific requirements that are too complicated to parse and handle in code. If you use this data, please take care to handle those special cases manually. There are only a few such courses and are listed under data/specialCases.
## Explanation of how `preReqs` and `coReqs` are stored
The pre-requisites and co-requisites are stored as an **expression tree**. For example, consider the following pre-requisites for `COMP 3711H`:
```
(Grade B+ or above in COMP 2011 / COMP 2012 / COMP 2012H) AND (grade A- or above in COMP 2711 / COMP 2711H / MATH 2343)
```
This has been parsed and stored in an expression tree like this:
![Graph showing the expression tree of COMP 3711H's prerequisites](https://user-images.githubusercontent.com/55091936/172394365-a7b72656-4575-4c24-a060-9facc32e3c0f.png)

... where `/` is an `OR` operator and `&` is an `AND` operator.

The value of `preReqs` and `coReqs` is the **root** node of the tree. Each node will have the two properties:
```json
{
    "value": "something",
    "children": [ ... ],
}
```
where `value` is what is stored in the node, and `children` are the connected nodes below the current node.
