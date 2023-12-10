import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def getAllEnterprise():
    conn = create_connection('identifier.sqlite')

    cur = conn.cursor()
    cur.execute("select DISTINCT Enterprise_Id, Enterprise_name from Enterprises;")

    rows = cur.fetchall()

    return rows


def getEnterpriseCountrywise(countryId):
    conn = create_connection('identifier.sqlite')

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Enterprise_Id, Enterprise_name FROM Enterprises WHERE Country_Code = ?;", (countryId,))

    rows = cur.fetchall()
    return rows


def getEnterpriseIndustrywise(industryId):
    conn = create_connection('identifier.sqlite')

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Enterprise_Id, Enterprise_name FROM Enterprises WHERE Sector_Id = ?;", (industryId,))

    rows = cur.fetchall()

    return rows

def get_distinctcountries():
    conn = create_connection('identifier.sqlite')

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Country_Code FROM Enterprises ;")
    rows = cur.fetchall()
    D_rows =[]
    for r in rows:
        D_rows.append(r[0])
    return D_rows
def getCountries():
    listOutCountries()
    conn = create_connection('identifier.sqlite')

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT * FROM CurrentCountries ;")
    rows = cur.fetchall()
    return rows
def listOutCountries():
    conn = create_connection('identifier.sqlite')

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT * FROM CurrentCountries ;")
    currentCountries = get_distinctcountries()
    rows = cur.fetchall()


    CountryId = []
    for row in rows:
        ListItem = row
        CountryId.append(ListItem[0])
    difference = list(set(CountryId) - set(currentCountries))
    for i in difference:
        cur.execute("DELETE FROM CurrentCountries WHERE Country_Code= ?;", (i,))
        conn.commit()


def removeEnterprise(ID):
    conn = create_connection('identifier.sqlite')

    cur = conn.cursor()
    cur.execute("DELETE FROM Project WHERE Project_Id= ?;", (ID,))
    cur.execute("DELETE FROM Enterprises WHERE Enterprise_Id= ?;", (ID,))
    cur.execute("DELETE FROM project_Descriptions WHERE Enterprise_Id= ?;", (ID,))
    conn.commit()
    print("Success")
def getAllCountries():
    conn = create_connection('identifier.sqlite')

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT * FROM country_Actual ;")

    rows = cur.fetchall()
    CountryId = []
    CountryName = []
    for row in rows:
        ListItem = list(row)
        CountryId.append(ListItem[0])
        CountryName.append(ListItem[1])

    return rows


def getSectors():
    conn = create_connection('identifier.sqlite')

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT * FROM Industries ;")

    rows = cur.fetchall()
    return rows


def getEnterpriseName(id):
    conn = create_connection('identifier.sqlite')

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Enterprise_name FROM Enterprises WHERE Enterprise_Id = ?;", (id,))

    rows = cur.fetchall()
    return rows


def getProjectDescription(id):
    conn = create_connection('identifier.sqlite')

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT * FROM project_Descriptions WHERE Enterprise_Id = ?;", (id,))

    rows = cur.fetchall()
    return rows

print(getCountries())