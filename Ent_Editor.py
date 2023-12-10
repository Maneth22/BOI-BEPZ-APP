import sqlite3
from sqlite3 import Error

from Enterprise import getProjectDescription


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def validateUser(username, password):
    conn = create_connection('identifier.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT * FROM UserTable ;")
    rows = cur.fetchall()
    user_dictionary = {}
    validation = False
    for row in rows:
        userID = str(row[0])
        user = {"Username": row[1],
                "Password": row[2]}
        user_dictionary[userID] = user
    for x in user_dictionary:
        current_dictionary = user_dictionary[x]
        for y in current_dictionary:
            if current_dictionary["Username"] == username and current_dictionary["Password"] == password:
                validation = True
            else:
                return False
    return validation


def CheckTin(tin):
    conn = create_connection('identifier.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT * FROM Project ;")
    rows = cur.fetchall()
    validation = False
    ProjectID = None
    print(tin)
    Descriptions = None
    for row in rows:
        Actual_tin = str(row[2])
        if Actual_tin == tin:
            ProjectID = row[0]
            validation = True
            print("working")
            Descriptions = getProjectDescription(ProjectID)
            return ProjectID, validation, Descriptions
    return ProjectID, validation, Descriptions


def UpdateDB(data):
    conn = create_connection('identifier.sqlite')
    cur = conn.cursor()
    x = None
    try:
        cur.execute(
            "UPDATE project_Descriptions SET Enterprise_name = ?, Est_Year = ?, Products_Services=?, Employment=?, Parent_com_name=?, Country_collaboration=?, Global_presence=?, KeyMarkets=?, Contact=?, MoreInfo2=?, Video_url=?, Image_url1=?, Image_url2=?, Image_url3=?, Image_url4=?  WHERE Enterprise_Id = ?;",
            (data["Enterprise_name"], data["Est_Year"], data["Products_Services"], data["Employment"],
             data["Parent_com_name"], data["Country_collaboration"], data["Global_presence"], data["KeyMarkets"],
             data["Contact"], data["MoreInfo2"], data["Video_url"], data["Image_url1"], data["Image_url2"],
             data["Image_url3"], data["Image_url4"], data["Enterprise_Id"],))
        conn.commit()
        x = True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        x = False
    return x


def updateIndustry(sectors, countries, tin, companyName):
    conn = create_connection('identifier.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT Project_Id FROM Project ORDER BY Project_Id DESC LIMIT 1;")
    ID = cur.fetchall()
    tuple_element = ID[0]
    newId = increment_ID(tuple_element[0])
    updateProject(newId, companyName, tin)
    updateEnterprise(companyName, newId, countries, sectors)
    AddProjectDesc(newId, companyName)
    print(newId)

    return True


def increment_ID(s):
    # Find the numeric part at the end of the string
    head = s.rstrip('0123456789')
    tail = s[len(head):]
    if not tail:
        tail = '0'
    new_tail = str(int(tail) + 1).zfill(len(tail))
    result = head + new_tail
    return result


def updateProject(ID, CompanyName, tin):
    conn = create_connection('identifier.sqlite')
    cur = conn.cursor()
    cur.execute("INSERT INTO Project (Project_Id, Project_Name, Tin_No) VALUES (?, ?, ?);", (ID, CompanyName, tin))
    conn.commit()


def AddProjectDesc(ID, CompanyName):
    conn = create_connection('identifier.sqlite')
    cur = conn.cursor()
    cur.execute("INSERT INTO Project_Descriptions (Enterprise_Id, Enterprise_name, video_url) VALUES (?, ?, ?);",
                (ID, CompanyName, "demo.mp4"))
    conn.commit()


def updateEnterprise(name, ID, countries, sectors):
    conn = create_connection('identifier.sqlite')
    cur = conn.cursor()
    for country in countries:
        if not checkCountry(country):
            cur.execute("SELECT CTRYNAME FROM country_Actual WHERE CTRYCD =? ;",(country,))
            rows = cur.fetchone()
            countryName=rows[0]
            print(countryName)
            countrImage =countryName+".png"
            cur.execute("INSERT INTO CurrentCountries (Country_Code, Country_Name, Country_Image) VALUES (?, ?, ?);",( country, countryName, countrImage,))
        cur.execute(
            "INSERT INTO Enterprises (Enterprise_Name, Sector_Id, Enterprise_Id, Country_Code) VALUES (?, ?, ?, ?);",
            (name, sectors, ID, country))
        conn.commit()


def checkCountry(countryID):
    conn = create_connection('identifier.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT Country_Code FROM CurrentCountries ;")
    rows = cur.fetchall()
    state = False
    for row in rows:
        if row[0] == countryID:
            print(row)
            state = True
    return state

