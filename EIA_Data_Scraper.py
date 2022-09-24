import os
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


URL = 'https://www.eia.gov/dnav/pet/pet_cons_prim_dcu_nus_m.htm'


def main():
    try:
        main_html_code = get_html_code(URL)
        
        motor_gas_url = get_motor_gasolink_url(main_html_code)
        
        motor_gas_html_code = get_html_code(motor_gas_url)    
        
        table = motor_gas_html_code.find('table', class_ = 'FloatTitle')
        
        df = html_tbl_to_df(table)
        print(df)
        
        df_to_csv(df)
    except Exception as e:
        print(e)


def df_to_csv(df):
    timestr = time.strftime("%Y%m%d_%H%M%S")
    output_filename = f'EIA_Motor_Gasoline_{timestr}.csv'
    
    df.to_csv(output_filename, index=False)
    
    print(f'\n* Data have been exported [{output_filename}]')


def html_tbl_to_df(table):
    headers = []
    
    for i in table.find_all('th'):
        title = i.text
        headers.append(title)
    
    df = pd.DataFrame(columns = headers)
    
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [tr.text.replace(',', '') for tr in row_data]
        if len(row) == 1: continue
        df.loc[len(df)] = row
    
    # Remove whitespace from the first column
    df.iloc[:,0] =  df.iloc[:,0].apply(lambda x: re.sub("[^0-9]", "", x))
      
    return df


def get_motor_gasolink_url(html_code):
    tbl_rows = html_code.find_all('tr', class_ = 'DataRow')
   
    motor_gasoline_row = [r for r in tbl_rows if r.find('td', class_ = 'DataStub1').text == 'Motor Gasoline'][0]
    
    motor_gas_url = motor_gasoline_row.find('a', class_='Hist').get('href')
    if motor_gas_url.startswith('.'):
        motor_gas_url = motor_gas_url[1:]
    
    return os.path.dirname(URL) + motor_gas_url


def get_html_code(url):
    try:
        page = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    return BeautifulSoup(page.text, 'lxml')


if __name__ == "__main__":
    main()
