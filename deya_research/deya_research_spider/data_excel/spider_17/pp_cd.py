import pandas as pd
from sqlalchemy import create_engine

con = create_engine(
    'mysql+pymysql://deya_research_dev:research123@192.168.1.183:3306/deya_research_dev?charset=utf8'
)

df = pd.DataFrame()
df_pp = pd.ExcelFile('PP仓单（20170101-20200807）.xlsx')
df_sheet1 = df_pp.parse(sheet_name='Sheet1')
df_sheet1['date'] = df_sheet1['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
df_sheet1['index_id'] = 78
df_sheet1.to_sql(name="dy_index_data", con=con, if_exists="append", index=False)
print('123')
