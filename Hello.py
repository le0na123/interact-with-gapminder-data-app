# Import libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title = 'My Dashboard', page_icon = ':bar_chart:', layout = 'wide')
st.title('Dashboard MT Khu vực Đông Nam Bộ 1')
st.sidebar.title('My dashboard')

# Upload file

upload = st.sidebar.file_uploader(label = 'Tải báo cáo 1.14 vào đây',type = ['xlsx', 'xls'])

if upload is not None:
    filename = upload.name
    df = pd.read_excel(filename)
else:
    os.chdir(r"C:\Users\Tuan\Desktop\Vinasoy\Analysis")
    df = pd.read_excel('Vinasoy.xlsx')

uploadTarget = st.sidebar.file_uploader(label = 'Tải file chỉ tiêu vào đây',type = ['xlsx', 'xls'])

if uploadTarget is not None:
    filename2 = uploadTarget.name
    dfTarget = pd.read_excel(filename2)
else:
    os.chdir(r"C:\Users\Tuan\Desktop\Vinasoy\Analysis")
    dfTarget = pd.read_excel('Target.xlsx')

# Choose start date and end date

col1, col2 = st.columns((2))

df['Ngày lấy đơn'] = pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)

startDate = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).min()
endDate = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).max()

# Process

df['Month'] =(pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True).dt.month)
SBM = df.groupby(by = 'Month').agg({'Thành tiền': 'sum'}).reset_index()
SBM['Month'] = SBM['Month'].map({
    1: 'Tháng 1/2023',
    2: 'Tháng 2/2023',
    3: 'Tháng 3/2023',
    4: 'Tháng 4/2023',
    5: 'Tháng 5/2023',
    6: 'Tháng 6/2023',
    7: 'Tháng 7/2023',
    8: 'Tháng 8/2023',
    9: 'Tháng 9/2023',
    10: 'Tháng 10/2023',
    11: 'Tháng 11/2023',
    12: 'Tháng 12/2023'
})
process = (SBM.set_index('Month').join(dfTarget.set_index('Month'))).reset_index()
months = st.subheader('Hoàn thành tiến độ tháng')
process['Hoàn thành'] = process['Thành tiền'] / process['Target'] * 100

months = st.radio('Chọn tháng: ', process['Month'])
st.table(process[process['Month'] == months])

with col1:
    date1 = pd.to_datetime(st.sidebar.date_input('Từ ngày: ', startDate), dayfirst = True)

with col2:
    date2 = pd.to_datetime(st.sidebar.date_input('Đến ngày: ', endDate), dayfirst = True)

df = df[(df['Ngày lấy đơn'] >= date1) & (df['Ngày lấy đơn'] <= date2)].copy()

# Line chart   
lineChart = px.line(SBM, x = SBM['Month'], y = SBM['Thành tiền'], title = 'THỰC HIỆN DOANH SỐ KÊNH MT ĐÔNG NAM BỘ 1 TỪ THÁNG 01/2023')
st.plotly_chart(lineChart, use_container_width = True, height = 200)



col3, col4 = st.columns((2))

with col3:
        
    # Bar chart by Suppliers

    sup = df.groupby(by = 'Tên NPP').agg({'Thành tiền': 'sum'}).reset_index()

    barChartSuppliers = px.bar(sup, x = sup['Tên NPP'], y = sup['Thành tiền'], title = 'DOANH SỐ BÁN RA THEO NHÀ PHÂN PHỐI')
    st.plotly_chart(barChartSuppliers, use_container_width = True, height = 200)

with col4:
    # Pie chart

    sys = df['Tên KH'].str.split(' ')
    system = sys.agg(lambda x: x[0])
    df['Hệ thống'] = system
    systems = df.groupby(by = 'Hệ thống').agg({'Thành tiền': 'sum'}).reset_index()
    systems['Hệ thống'] = systems['Hệ thống'].map({
        'BHX': 'Bách Hóa Xanh',
        'VMP': 'Vincommerce',
        'Lotte': 'Lotte Mart',
        'MM': 'Mega Market',
        'VM': 'Vincommerce',
        'BigC': 'BigC và Go!',
        'Coopfood': 'Sài Gòn Coop',
        'Coopmart': 'Sài Gòn Coop'
    })
    pieChart = px.pie(systems, values = systems['Thành tiền'], names = systems['Hệ thống'], title = 'TỶ LỆ ĐÓNG GÓP CỦA CÁC HỆ THỐNG SIÊU THỊ')
    st.plotly_chart(pieChart, use_container_width = True, height = 200)


# Sorting by SKUs

skus = df.groupby(by = 'Tên sản phẩm').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
skus = skus.sort_values('Hàng bán (Thùng)', ascending = True)

barChartSkus = px.bar(skus, y = skus['Tên sản phẩm'], x = skus['Hàng bán (Thùng)'], title = 'Sản lượng bán ra theo SKUs', orientation = 'h')
st.plotly_chart(barChartSkus, use_container_width = True, height = 1000)
