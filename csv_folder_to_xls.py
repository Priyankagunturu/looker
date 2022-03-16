import glob

import pandas as pd

csv_folder = './dashboard-agency_dashboard/' + '*.csv'
excel_file = './exporte_excel.xlsx'

excel_writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

for file in glob.iglob(csv_folder, recursive=True):
    df = pd.read_csv(file)
    df.to_excel(excel_writer, sheet_name=file.split('\\')[-1], index=False)


excel_writer.save()
print('Task Completed')
