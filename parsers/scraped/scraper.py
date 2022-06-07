import requests
import os
import time

sems = ["2110", "2120", "2130", "2140"]

if not os.path.exists("data") or not os.path.isdir("data"):
    os.mkdir("data")

depts = [ # Fall, Winter, Spring, Summer
    ['ACCT', 'AESF', 'AIAA', 'AMAT', 'BIBU', 'BIEN', 'BSBE', 'BTEC', 'CBME', 'CENG', 'CHEM', 'CHMS', 'CIEM', 'CIVL', 'CMAA', 'COMP', 'CPEG', 'CSIT', 'DASC', 'DBAP', 'DSAA', 'DSCT', 'ECON', 'EEMT', 'EESM', 'ELEC', 'EMBA', 'ENEG', 'ENGG', 'ENTR', 'ENVR', 'ENVS', 'EOAS', 'EVNG', 'EVSM', 'FINA', 'FTEC', 'FUNH', 'GBUS', 'GFIN', 'GNED', 'HART', 'HHMS', 'HLTH', 'HMMA', 'HUMA', 'IBTM', 'IDPO', 'IEDA', 'IIMP', 'IMBA', 'INFH', 'INTR', 'IOTA', 'IPEN', 'ISDN', 'ISOM', 'JEVE', 'LABU', 'LANG', 'LIFS', 'MAED', 'MAFS', 'MARK', 'MASS', 'MATH', 'MECH', 'MESF', 'MFIT', 'MGCS', 'MGMT', 'MICS', 'MILE', 'MIMT', 'MSBD', 'MSDM', 'MTLE', 'NANO', 'OCES', 'PDEV', 'PHYS', 'PPOL', 'RMBI', 'ROAS', 'SBMT', 'SCIE', 'SEEN', 'SHSS', 'SMMG', 'SOCH', 'SOSC', 'SUST', 'SYSH', 'TEMG', 'UGOD', 'UROP', 'WBBA'],
    ['CENG', 'CIVL', 'COMP', 'ECON', 'ELEC', 'EMBA', 'ENEG', 'ENGG', 'ENTR', 'ENVR', 'EVSM', 'GFIN', 'IEDA', 'IMBA', 'ISDN', 'ISOM', 'LIFS', 'MAED', 'MATH', 'MGCS', 'MGMT', 'PHYS', 'SBMT', 'SHSS', 'SOSC', 'TEMG'],
    ['ACCT', 'AESF', 'AIAA', 'AMAT', 'BIBU', 'BIEN', 'BSBE', 'BTEC', 'CBME', 'CENG', 'CHEM', 'CHMS', 'CIEM', 'CIVL', 'CMAA', 'COMP', 'CPEG', 'CSIT', 'DBAP', 'DSAA', 'DSCT', 'ECON', 'EEMT', 'EESM', 'ELEC', 'EMBA', 'ENEG', 'ENGG', 'ENTR', 'ENVR', 'ENVS', 'EOAS', 'EVNG', 'EVSM', 'FINA', 'FTEC', 'FUNH', 'GBUS', 'GFIN', 'GNED', 'HART', 'HHMS', 'HLTH', 'HMMA', 'HUMA', 'IBTM', 'IDPO', 'IEDA', 'IIMP', 'IMBA', 'INFH', 'INTR', 'IOTA', 'IPEN', 'ISDN', 'ISOM', 'JEVE', 'LABU', 'LANG', 'LIFS', 'MAED', 'MAFS', 'MARK', 'MASS', 'MATH', 'MECH', 'MESF', 'MFIT', 'MGCS', 'MGMT', 'MICS', 'MILE', 'MIMT', 'MSBD', 'MSDM', 'MTLE', 'NANO', 'OCES', 'PDEV', 'PHYS', 'PPOL', 'RMBI', 'ROAS', 'SBMT', 'SCIE', 'SEEN', 'SHSS', 'SMMG', 'SOSC', 'SUST', 'SYSH', 'TEMG', 'UGOD', 'UROP', 'WBBA'],
    ['ACCT', 'AESF', 'BIEN', 'BTEC', 'CBME', 'CENG', 'CHEM', 'CHMS', 'CIEM', 'CIVL', 'COMP', 'CSIT', 'ECON', 'EEMT', 'EESM', 'ELEC', 'ENEG', 'ENGG', 'ENTR', 'EVSM', 'FINA', 'GFIN', 'HUMA', 'IBTM', 'IEDA', 'ISDN', 'ISOM', 'JEVE', 'LABU', 'LANG', 'LIFS', 'MAED', 'MAFS', 'MARK', 'MATH', 'MECH', 'MESF', 'MGCS', 'MGMT', 'MIMT', 'MSBD', 'MTLE', 'OCES', 'PHYS', 'PPOL', 'SBMT', 'SCIE', 'SHSS', 'SOSC', 'UROP']
    ]

def get_url(sem, dept):
    return f"https://w5.ab.ust.hk/wcq/cgi-bin/{sem}/subject/{dept}"

for i, sem in enumerate(sems):
    sem_depts = depts[i]
    
    for dept in sem_depts:
        url = get_url(sem, dept)
        print(f"Downloading {url}...")
        text = requests.get(get_url(sem, dept)).text
        with open(f"data/{sem}_{dept}.html", "w") as o:
            o.write(text)
        time.sleep(0.5)
