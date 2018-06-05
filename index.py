from flask import Flask, render_template, request
import os
import pandas as pd
import xlrd
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
        return render_template('index.html')


@app.route('/explore', methods=['POST'])
def explore():
    target = os.path.join(APP_ROOT,"files/")
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        if(filename.lower().endswith(('xlsx'))) :
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
        elif ((filename.lower().endswith(('xlsx')))==False):
            return render_template('index.html',echec="Error",msg="the file extension is not valid, chose a xlsx data file.")

        else:
            return render_template('index.html',echec="Error",msg="please, you should upload a file")

    header_smart = pd.read_excel(filename, header=None, sheet_name=0, usecols=1)
    header_smart.head(7).to_html('templates/header_smart.html')

    ################
    xlsx = pd.ExcelFile(filename)
    smart_sheets = []
    i = 0
    sheet_names = xlsx.sheet_names
    for sheet in sheet_names:
        smart_sheets.append(pd.read_excel('smartgrid.xlsx', sheet_name=i, skiprows=10))
        i = i + 1

    return render_template('explore.html',filename=filename,sheet_names=sheet_names)


@app.route('/user')
def user():

    return render_template('user.html')


def sheet_selection( str ):
    xlsx = pd.ExcelFile('smartgrid.xlsx')
    smart_sheets = []
    i = 0
    sheet_names = xlsx.sheet_names
    for sheet in sheet_names:
        smart_sheets.append(pd.read_excel('smartgrid.xlsx', sheet_name=i, skiprows=10))
        i = i + 1
    ExcelFileName = 'smartgrid.xlsx'
    workbook = xlrd.open_workbook(ExcelFileName)
    smart_selected_row = []
    for j in range(0, 5, 1):
        worksheet = workbook.sheet_by_name(sheet_names[j])  # We need to read the data
        num_rows = worksheet.nrows  # Number of Rows
        num_cols = worksheet.ncols  # Number of Columns
        result_data = []
        for curr_row in range(0, num_rows, 1):
            row_data = []
            for curr_col in range(0, num_cols, 1):
                data = worksheet.cell_value(curr_row, curr_col)  # Read the data in the current cell
                if data != '':
                    row_data.append(data)
            result_data.append(row_data)
        # for data in range(0,len(result_data),1):
        smart_selected_row.append(result_data)
        # for i in range(0,len(smart_sheets),1) :
        smart_sheets[j].columns = result_data[9]
        ami_names_column = ['ProjectId', 'ContractType', 'PrimeRecipient', 'Year of PeriodEndDate',
                            'Quarter of PeriodEndDate', 'Month of PeriodEndDate', 'Day of PeriodEndDate',
                            'NercRegion', 'UtilityType', 'AmiSmartMtrCommType', 'AmiSmartMtrBackHaulNetType',
                            'TotalCustomerCount', 'ResidentialCustomerCount', 'CommercialCustomerCount',
                            'IndustrialCustomerCount', 'AmiSmartMtrCount', 'ami_AmiSmartMtrTotalCount',
                            'ami_AmiSmartMtrResidentialCount', 'ami_AmiSmartMtrCommercialCount',
                            'ami_AmiSmartMtrIndustrialCount', 'ami_AmiIntervalReads', 'ami_AmiRemoteDisconnectMtrCount',
                            'ami_AmiOutageReportingMtrCount', 'ami_AmiTamperDetectionMtrCount', 'AmiSmartMtrCost',
                            'AmiCommEquipCost', 'AmiBackOfficeCost', 'AmiOtherCost']

        smart_sheets[0].columns = ami_names_column
        if (str == sheet_names[0]):
            return smart_sheets[0]
        elif (str == sheet_names[1]):
            return smart_sheets[1]
        elif (str == sheet_names[2]):
            return smart_sheets[2]
        elif (str == sheet_names[3]):
            return smart_sheets[3]
        elif (str == sheet_names[4]):
            return smart_sheets[4]
        elif (str == sheet_names[5]):
            return smart_sheets[5]
        else:
            return

print(sheet_selection("AMI"))
if __name__ == '__main__':
    app.run(debug=True)