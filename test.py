import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


ami = pd.read_excel('smartgrid.xlsx',sheet_name=0,header=8).head()
#ami1 = pd.read_excel('smartgrid.xlsx',sheet_name=1,header=8)
#ami2 = pd.read_excel('smartgrid.xlsx',sheet_name=2,header=8)


#movies = pd.concat([ami, ami1, ami2])
ami.to_html('table.html')

#print(ami)

header_smart = pd.read_excel("smartgrid.xlsx", header=None, sheet_name=0, usecols=1)
header_smart.head(7)

import xlrd
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
        if (str == "AMI"):
            return smart_sheets[0]
        elif (str == " Customer System "):
            return smart_sheets[1]
        elif (str == " DER"):
            return smart_sheets[2]
        elif (str == "   Distribution "):
            return smart_sheets[3]
        elif (str == " Transmission"):
            return smart_sheets[4]
        elif (str == " Data Descriptions"):
            return smart_sheets[5]
        else:
            return

print(sheet_selection("AMI"))