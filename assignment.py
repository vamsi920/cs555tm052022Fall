# file_path = 'gedcom.ged'
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.parser import Parser
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
from prettytable import DOUBLE_BORDER
from random import randint
import datetime
from datetime import date

x = PrettyTable()
y = PrettyTable()
filep = input("enter gedcom file path: ")
# filep = "gedcom.ged"
gedcom_parser = Parser()
gedcom_parser.parse_file(filep)
root_child_elements = gedcom_parser.get_root_child_elements()
x.field_names = ["ID","Name", "Gender", "Birth date", "Alive", "Death", "Child", "Spouse"]

def bigamy(husbands):
    if(len(husbands) != len(set(husbands))):
        return True
    else: 
        return False

def parentsTooOld(mom,dad): # pass the DoB of mom and dad from below stored data to check and then use. 
    if(2022 - int(mom.split(" ")[-1])> 80 or 2022 - int(dad.split(" ")[-1])> 80):
        return True
    else:
        return False

def valid_date_of_marriage(start,end):
    if(start.split(" ")[-1]>end.split(" ")[-1]):
        return "Not valid"
    else:
        return "Valid"
def DOB_before_marriage(start,end):
    if(start.split(" ")[-1]>end.split(" ")[-1]):
        return False
    else:
        return True

def valid_date_of_birth_current(start,end):
    if(start.split(" ")[-1]>end.split(" ")[-1]):
        return "Not valid"
    else:
        return "Valid"

def valid_divorce_before_death(start,end):
    if(start.split(" ")[-1]>end.split(" ")[-1] or start=="NA"):
        return False
    else:
        return True

def ageBelow100(age):
    if(2022 - int(age.split(" ")[-1])>100):
        return False
    else:
        return True

def DOB_after_Death(start,end):
    if(start.split(" ")[-1]>end.split(" ")[-1]):
        return False
    else:
        return True

def Store_DOB(dob,x):
    dobs = x.get_string(fields =["Birth date"])
    if dob not in dobs:
        x.add_row([" ", " ", " ", dob," ", " "," ", " "])
    else: 
        return "dob exists"

def Store_name(name,x):
    names = x.get_string(fields =["Name"])
    if name not in names:
        x.add_row([" ", name, " ", " "," ", " "," ", " "])
    else: 
        return "name exists"

def check_marital(name, x):
    names = x.get_string(fields =["Name"])
    spouses = x.get_string(fields =["Spouse"])
    if name in names:
        id = names.index(name)
        if(spouses[id] !="NA"):
            return "married"
        else:
            return "not married"

def check_living_status(name, x):
    names = x.get_string(fields =["Name"])
    alive = x.get_string(fields =["Alive"])
    if name in names:
        id = names.index(name)
        if(alive[id] =="True"):
            return "alive"
        else:
            return "dead"

def Add_to_table_if_alive_and_not_married(name, x):
    if(check_marital(name,x) == "not married" and check_living_status(name,x) == "alive"):
        Store_name(name,x)
        return "added"
    else:
        return "not added"

mapall = {}
for element in root_child_elements:
    
    if isinstance(element, IndividualElement):
        # print(element.get_individual())
        # spouses = 
        Children = ""
        spouseid = ""
        family = str(element.get_individual()).split("\n")
        for i in family:
            familyparts = i.split(" ")
            # print(familyparts)
            if("FAMS" in familyparts):
                spouseid = familyparts[2].strip('\r') if familyparts[2] != " " else ""
            elif("FAMC" in familyparts):
                Children = familyparts[2].strip('\r') if familyparts[2] != " " else ""
        birth = element.get_birth_data()[0]
        death = "NA" if element.get_death_data()[0]=="" else element.get_death_data()[0]
        Alive = True if death == "NA" else False
        chi = Children if Children!="" else "NA"
        sp = spouseid if spouseid != "" else "NA"
        mapall[element.get_pointer()] = [element.get_name()[0]+" "+element.get_name()[1], element.get_birth_data()[0]]
        x.add_row([element.get_pointer(), element.get_name()[0]+" "+element.get_name()[1], element.get_gender(), element.get_birth_data()[0],Alive, death,chi, spouseid])
# print(mapall['@I6000000187342139825@'])
x.set_style(DOUBLE_BORDER)
print(x.get_string())
Husbands = []
y.field_names = ["FAM ID","Married","Divorced","Husband ID","Husband Name", "Wife ID",  "Wife Name","Children", "Birth Before Marriage", "Death Before Birth"]
for element in root_child_elements:
    if isinstance(element, FamilyElement):
        
        Husbandid = ""      
        Wifeid = "" 
        Children = []
        point = element.get_pointer() 
        d = str(datetime.date(randint(1973,2000), randint(1,12),randint(1,28))).split("-")
        Divorced = "NA"
        if(Divorced != "NA"):
            valid_date_of_marriage(d,Divorced)
        family = str(element.get_individual()).split("\n")
        td = date.today()
        tdformat = td.strftime("%m/%d/%y")
        if (death != "NA"):
            valid_date_of_birth_current(tdformat,birth)
        for i in family:
            familyparts = i.split(" ")
            # print(familyparts)
            if("HUSB" in familyparts):
                Husbandid = familyparts[2].strip('\r')
            elif("WIFE" in familyparts):
                Wifeid = familyparts[2].strip('\r')
            elif("CHIL" in familyparts):
                Children.append(familyparts[2].strip('\r'))
        # print(mapall[Husbandid.strip('\r')])
        if(DOB_before_marriage(mapall[Children[0]][1].split(" ")[-1],d[-1])):
            birth_before_marriage = "Yes"
        else:
            birth_before_marriage = "No"
        if(DOB_after_Death(death,birth)):
            death_before_birth = "Yes"
        else:
            death_before_birth = "No"
        Husbands.append(Husbandid)
        y.add_row([point,d[1]+"/"+ d[2]+"/"+d[0],Divorced,Husbandid,mapall[Husbandid.strip('\r')][0],Wifeid, mapall[Wifeid.strip('\r')][0], Children,birth_before_marriage, death_before_birth ])   
# bigamy(Husbands)
print(y)
