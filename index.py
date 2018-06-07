from flask import Flask, render_template, request, session
import os
import pandas as pd
import xlrd
import seaborn as sns
import shutil
import pathlib

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.secret_key='abcd'

@app.route('/')
def index():
        session.clear()
        return render_template('index.html')


@app.route('/avg/<sheet>')
def avg(sheet=None):
    return render_template('avg.html')


@app.route('/<sheet>/<column>/<column1>',methods=['POST','GET'])
@app.route('/<sheet>/<column>')
@app.route('/<sheet>')
@app.route('/explore', methods=['POST','GET'])
def explore(sheet=None,argument=None,column=None,column1=None):
    ##############################################"
        #argument=request.args['argument']
    argument=request.form.get("argument")

    if sheet is not None:
        sheet_selection(sheet).to_html('templates/table_sheet.html')

    if column is not None and column1 is None:
        agg_count(sheet_selection(sheet), column).to_html('templates/table_count.html')
        sns.set_style("whitegrid")
        ax = sns.barplot( y='Count', x=column,data=agg_count(sheet_selection(sheet), column).head())
        ax.set(xlabel='\n Number of '+column )
        shutil.rmtree('static/img')
        os.makedirs('static/img', exist_ok=True)
        ax.figure.savefig('static/img/'+column+'.png')
    if argument is not None:
        try:
            my_data = sheet_selection(sheet)
            agg_count(my_data[my_data[column1] == int(argument)], column).to_html('templates/table_count_dep.html')
            sns.set_style("whitegrid")
            ax2 = sns.barplot(y='Count', x=column, data=agg_count(my_data[my_data[column1] == int(argument)], column).head())
            ax2.set(xlabel='\n Number of ' + column + ' in ' + argument)
            ax2.figure.savefig('static/img/'+ argument +'.png')
        except ValueError:
            return "Error: this graph can't be displayed <a href='"+"/"+sheet+"/"+column+"' > go to your page </a>"

    #agg_avg(sheet_selection(sheet),column).to_html('templates/table_avg.html')
    if 'filename' not in session:
            target = os.path.join(APP_ROOT,"files/")
            print(target)
            if not os.path.isdir(target):
                os.mkdir(target)
            for file in request.files.getlist("file"):
                print(file)
                filename= file.filename
                if(filename.lower().endswith(('xlsx'))) :
                    destination = "/".join([target, filename])
                    print(destination)
                    file.save(destination)
                elif ((filename.lower().endswith(('xlsx')))==False):
                    return render_template('index.html',echec="Error",msg="the file extension is not valid, chose a xlsx data file.")

                else:
                    return render_template('index.html',echec="Error",msg="please, you should upload a file")
                session['filename']=filename
    ##############################################
    header_smart = pd.read_excel(session['filename'], header=None, sheet_name=0, usecols=1)
    header_smart.head(7).to_html('templates/header_smart.html')

        ################
    xlsx = pd.ExcelFile(session['filename'])
    smart_sheets = []
    i = 0
    sheet_names = xlsx.sheet_names
    for isheet in sheet_names:
        smart_sheets.append(pd.read_excel(session['filename'], sheet_name=i, skiprows=10))
        i = i + 1


    ################################


    ################################

    return render_template('test.html',filename=session['filename'],argument=argument,sheet=sheet, column1=column1, column=column,sheet_names=sheet_names,columns=column_name(sheet))




def sheet_selection( str ):
    xlsx = pd.ExcelFile(session['filename'])
    smart_sheets = []
    i = 0
    sheet_names = xlsx.sheet_names
    for sheet in sheet_names:
        smart_sheets.append(pd.read_excel(session['filename'], sheet_name=i, skiprows=10))
        i = i + 1
    ExcelFileName = session['filename']
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


def column_name(str) :
    xlsx = pd.ExcelFile(session['filename'])
    smart_sheets = []
    i = 0
    sheet_names = xlsx.sheet_names
    for sheet in sheet_names:
        smart_sheets.append(pd.read_excel(session['filename'], sheet_name=i, skiprows=10))
        i = i + 1
    ExcelFileName = session['filename']
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
        return smart_selected_row[0][9]
    elif (str == sheet_names[1]):
        return smart_selected_row[1][9]
    elif (str == sheet_names[2]):
        return smart_selected_row[2][9]
    elif (str == sheet_names[3]):
        return smart_selected_row[3][9]
    elif (str == sheet_names[4]):
        return smart_selected_row[4][9]
    elif (str == sheet_names[5]):
        return smart_selected_row[5][9]
    else:
        return


def agg_count(df, group_field):
    grouped = df.groupby(group_field, as_index=False).size()
    #grouped.sort(ascending = False)
    grouped = pd.DataFrame(grouped).reset_index()
    grouped.columns = [group_field, 'Count']
    return grouped

def agg_avg(df, group_field, calc_field):
    grouped = df.groupby(group_field, as_index=False)[calc_field].mean()
    #grouped = grouped.sort(calc_field, ascending = False)
    grouped.columns = [group_field, 'Avg ' + str(calc_field)]
    return grouped

if __name__ == '__main__':
    app.run(debug=True)