import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for

import Ent_Editor
import Enterprise
from Ent_Editor import validateUser, CheckTin, UpdateDB

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/aboutUs')
def aboutUs():
    return render_template('AboutUs.html')


@app.route('/whySrilanka')
def whySrilanka():
    return render_template('whySrilanka.html')


@app.route('/biyagamaEPZ')
def biyagamaEPZ():
    return render_template('Biyagama.html')


@app.route('/LayoutBpz')
def LayoutBpz():
    return render_template('LayoutBpz.html')


@app.route('/Enterprises')
def Enterprises():
    DataList = Enterprise.getAllEnterprise()
    countries = Enterprise.getCountries()
    sectors = Enterprise.getSectors()
    print(DataList)
    jsonData = jsonify(DataList)
    jsonCountries = jsonify(countries)
    return render_template('Enterprises.html', data_lists=DataList, Sectors=sectors, Countries=countries)


@app.route('/locData', methods=['GET'])
def locData():
    DataList = Enterprise.getAllEnterprise()
    print(DataList)
    jsonData = jsonify(DataList)
    return render_template('Enterprises.html', data_list=DataList)


@app.route('/secData', methods=['GET', 'POST'])
def secData():
    if request.method == 'POST':
        print('Post')
    DataList = Enterprise.getEnterpriseIndustrywise()
    print(DataList)
    jsonData = jsonify(DataList)
    return render_template('Enterprises.html', data_list=DataList)


@app.route('/country_Input', methods=['GET', 'POST'])
def country_Input():
    if request.method == 'POST':
        country = request.form['countryRadio']
        print(country)
        DataList = Enterprise.getEnterpriseCountrywise(country)
        countries = Enterprise.getCountries()
        sectors = Enterprise.getSectors()
        return render_template('Enterprises.html', data_lists=DataList, Sectors=sectors, Countries=countries)
    return redirect('Enterprises.html')


@app.route('/sector_Input', methods=['GET', 'POST'])
def sector_Input():
    if request.method == 'POST':
        sector = request.form['sectorRadio']
        print(sector)
        DataList = Enterprise.getEnterpriseIndustrywise(sector)
        countries = Enterprise.getCountries()
        sectors = Enterprise.getSectors()
        return render_template('Enterprises.html', data_lists=DataList, Sectors=sectors, Countries=countries)
    return redirect('Enterprises.html')


@app.route('/location_Input', methods=['GET', 'POST'])
def location_Input():
    return render_template('Enterprises.html')


@app.route('/conData', methods=['GET'])
def conData():
    DataList = Enterprise.getEnterpriseCountrywise('C004')
    print(DataList)
    jsonData = jsonify(DataList)
    return render_template('Enterprises.html', data_list=DataList)


@app.route('/AboutBepz')
def AboutBepz():
    return render_template('AboutBepz.html')


@app.route('/Departments')
def Departments():
    return render_template('Departments.html')


@app.route('/DepLayout')
def DepLayout():
    return render_template('DepLayout.html')


@app.route('/depDrZone')
def depDrZone():
    return render_template('department/DirectorZone.html')


@app.route('/depIndRel')
def depIndRel():
    return render_template('department/depIndRel.html')


@app.route('/depInvSvc')
def depInvSvc():
    return render_template('department/depInvSvc.html')


@app.route('/depZoneMan')
def depZoneMan():
    return render_template('department/depZoneMan.html')


@app.route('/depIntAud')
def depIntAud():
    return render_template('department/depIntAud.html')


@app.route('/depEngSvc')
def depEngSvc():
    return render_template('department/depEngSvc.html')


@app.route('/depEnv')
def depEnv():
    return render_template('department/depEnv.html')


@app.route('/depSecFir')
def depSecFir():
    return render_template('department/depSecFir.html')


@app.route('/depFire')
def depFire():
    return render_template('department/depFire.html')


@app.route('/depFin')
def depFin():
    return render_template('department/depFin.html')


@app.route('/projectRedirect/<itemId>')
def projectRedirect(itemId):
    print(itemId)
    projectName = Enterprise.getEnterpriseName(itemId)
    projectDescription = Enterprise.getProjectDescription(itemId)
    print(projectDescription)
    return render_template('projectDetails.html', prjName=projectName, prjDesc=projectDescription)


@app.route('/EntManagement')
def EntManagement():
    Error = ""
    return render_template('Enterprise_edit.html', ErrorMessage=Error)


@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        validation = validateUser(username, password)
        sectors = Enterprise.getSectors()
        countries = Enterprise.getAllCountries()
        if validation:
            # Redirect to a new page on successful login
            return render_template('Editor_page.html', ID=None, ErrorMessage=None, Sectors=sectors, Countries=countries)

        # Render the login form for GET requests or failed login attempts
    Error = "Incorrect Username or Password"
    return render_template('Enterprise_edit.html', ErrorMessage=Error, ID=None)


@app.route('/entEdit', methods=['GET', 'POST'])
def entEdit():
    if request.method == 'POST':
        return 0


@app.route('/SubmitValues', methods=['GET', 'POST'])
def SubmitValues():
    sectors = Enterprise.getSectors()
    countries = Enterprise.getAllCountries()
    if request.method == 'POST':
        companyID = request.form['ID']
        companyName = request.form['EntName']
        companyYear = request.form['year']
        products = request.form['products']
        employ = request.form['emp']
        parentCompany = request.form['parent']
        collaboration = request.form['colab']
        globalPresence = request.form['global']
        keyMarkets = request.form['market']
        contact = request.form['contact']
        moreInfo = request.form['info']

        if 'vid' in request.files and request.files['vid']:
            vidFile = request.files['vid']
            vidFilename = vidFile.filename
            vidFile.save('static/videos/' + vidFilename)
        else:
            vidFilename = 'demo.mp4'

        if 'img1' in request.files and request.files['img1']:
            im1File = request.files['img1']
            im1Filename = im1File.filename
            im1File.save('static/Images/CompanyImages/' + im1Filename)
        else:
            im1Filename = None

        if 'img2' in request.files and request.files['img2']:
            im2File = request.files['img2']
            im2Filename = im2File.filename
            im2File.save('static/Images/CompanyImages/' + im2Filename)
        else:
            im2Filename = None

        if 'img3' in request.files and request.files['img3']:
            im3File = request.files['img3']
            im3Filename = im3File.filename
            im3File.save('static/Images/CompanyImages/' + im3Filename)
        else:
            im3Filename = None

        if 'img4' in request.files and request.files['img4']:
            im4File = request.files['img4']
            im4Filename = im4File.filename
            im4File.save('static/Images/CompanyImages/' + im4Filename)
        else:
            im4Filename = None
        dataRetrieval = {
            "Enterprise_Id": companyID,
            "Enterprise_name": companyName,
            "Est_Year": companyYear,
            "Products_Services": products,
            "Employment": employ,
            "Parent_com_name": parentCompany,
            "Country_collaboration": collaboration,
            "Global_presence": globalPresence,
            "KeyMarkets": keyMarkets,
            "Contact": contact,
            "MoreInfo2": moreInfo,
            "Video_url": vidFilename,
            "Image_url1": im1Filename,
            "Image_url2": im2Filename,
            "Image_url3": im3Filename,
            "Image_url4": im4Filename

        }
        print(dataRetrieval)
        Result = UpdateDB(dataRetrieval)
        print(Result)

        return render_template('Editor_page.html', ID=None, ErrorMessage=None, Descs=None, result=Result,
                               Sectors=sectors, Countries=countries)
    else:
        return render_template('Editor_page.html', ID=None, ErrorMessage="Data not passed", Descs=None, Sectors=sectors,
                               Countries=countries)


@app.route('/AddNewEnterprise', methods=['GET', 'POST'])
def AddNewEnterprise():
    sectors = Enterprise.getSectors()
    countries = Enterprise.getAllCountries()
    if request.method == 'POST':
        tin = request.form['tin2']
        prjID, validation, Descriptions = CheckTin(tin)
        if validation:
            er = "TIN already registered"
            return render_template('Editor_page.html', Sectors=sectors, Countries=countries, ER2=er)
        if 'sectorRadio2' in request.form and request.form['sectorRadio2']:
            ProjectName = request.form['EntName2']
            sector = request.form['sectorRadio2']
            countryList = request.form.getlist('countryCheckbox')
            print(countryList)
            progress = Ent_Editor.updateIndustry(sector, countryList, tin, ProjectName)

            if progress:
                msg = "Success"
            else:
                msg = "Error Occurred"
            return render_template('Editor_page.html', Sectors=sectors, Countries=countries, Message=msg)

        return render_template('Editor_page.html', Sectors=sectors, Countries=countries)




    return render_template('Editor_page.html', ID=None, ErrorMessage=None, Sectors=sectors, Countries=countries)


@app.route('/removeEnterprise', methods=['GET', 'POST'])
def removeEnterprise():
    sectors = Enterprise.getSectors()
    countries = Enterprise.getAllCountries()
    if request.method == 'POST':
        tin = request.form['tin3']
        prjID, validation, Descriptions = CheckTin(tin)
        print(tin)
        if validation:
            Enterprise.removeEnterprise(prjID)
            msg = "Successfully Removed Enterprise : "+str(tin)
            return render_template('Editor_page.html',  Sectors=sectors, Countries=countries, Message=msg)
        er = "Incorrect Tin Number"
        return render_template('Editor_page.html', Message=er, ID=None, Sectors=sectors, Countries=countries)
    return render_template('Editor_page.html', Sectors=sectors, Countries=countries)

@app.route('/tinValidation', methods=['GET', 'POST'])
def tinValidation():
    sectors = Enterprise.getSectors()
    countries = Enterprise.getAllCountries()
    if request.method == 'POST':
        tin = request.form['tin']
        prjID, validation, Descriptions = CheckTin(tin)
        print(tin)
        if validation:
            print(validation)
            return render_template('Editor_page.html', ID=prjID, ErrorMessage=None, Descs=Descriptions, Sectors=sectors,
                                   Countries=countries)
        er = "Not a Valid Tin Number"
        return render_template('Editor_page.html', ErrorMessage=er, ID=None, Sectors=sectors, Countries=countries)
    return render_template('Editor_page.html', ID=None, ErrorMessage=None, Sectors=sectors, Countries=countries)


def editor_page():
    # Access the project ID from the query parameters
    prjID = request.args.get('ID')
    er = request.args.get('ErrorMessage')
    # Render the Editor page with the project ID
    return render_template('Editor_page.html', ID=prjID, ErrorMessage=er)


@app.route('/check_activity', methods=['GET'])
def check_activity():
    last_activity = app.config.get('last_activity_time', datetime.utcnow())
    now = datetime.utcnow()

    if now - last_activity > timedelta(seconds=10):
        app.config['last_activity_time'] = now
        print("this should be reloaded")
        return jsonify(reload=True, template='index.html')
    else:
        return jsonify(reload=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
