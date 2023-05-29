from function import *
import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
import datetime
from datetime import date
from PIL import Image
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests
import googleapiclient.discovery
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import json


def get_access_token():
    url = "https://www.googleapis.com/oauth2/v4/token"
    data = {'Content-Type': 'application/json',
    "client_id": '', #Đã copy client_ID trong file hướng dẫn
    "client_secret": '', #Đã copy server_ID trong file hướng dẫn
    "refresh_token": '', #Đã copy refresh_token trong file hướng dẫn
    "grant_type": "refresh_token"
    }
    x = requests.post(url, data=data)
    x = x.json()
    access_token = x["access_token"]
    return access_token

def get_data(CMS_list,  CMS_name, channel_ID_list, start_date, end_date, metric, metric_display, access_token):
    df = pd.DataFrame()
    df = pd.DataFrame(columns= ['Channel ID','Date'] + metric_display)
    if len(CMS_list) == 1:
       
       for channel_ID in channel_ID_list:
           url = 'https://youtubeanalytics.googleapis.com/v2/reports?' 
           dimensions = 'dimensions=day'
           ids = CMS_list[0]
           filters = 'filters=' + channel_ID
           startDate = 'startDate=' + start_date
           endDate = 'endDate=' + end_date
           metrics = 'metrics=' + metric
           keys = "key=AIzaSyAsf5RBA8c9L4FzYayL8ZkPqWX4LtDkbTY"
           url = url + "&".join([dimensions, ids, filters, startDate, endDate, metrics, keys])
           headers = {'Authorization': "Bearer " + access_token,
           'Accept': 'application/json'}
           response = requests.get(url, headers= headers)
           response = response.json()

           for i in range(len(response['rows'])):
                list = [channel_ID.replace('channel%3D%3D', '')]
                for j in range (len(metric_display) + 1):
                    data = response['rows'][i][j]
                    list.append(data)
                df.loc[len(df.index)] = list
         
    else:
        for CMS in CMS_list:
            url = 'https://youtubeanalytics.googleapis.com/v2/reports?'
            dimensions = 'dimensions=day'
            ids = CMS
            filters = 'filters=uploaderType%3D%3Dself'
            startDate = 'startDate=' + start_date
            endDate = 'endDate=' + end_date
            metrics = 'metrics=' + metric
            keys = "key=AIzaSyAsf5RBA8c9L4FzYayL8ZkPqWX4LtDkbTY"
            url = url + "&".join([dimensions, ids, filters, startDate, endDate, metrics, keys])
            headers = {'Authorization': "Bearer " + access_token,
           'Accept': 'application/json'}
            response = requests.get(url, headers= headers)
            response = response.json()
           
            for i in range(len(response['rows'])):
                list = [CMS.replace('contentOwner%3D%3D', '')]
                for j in range (len(metric_display) + 1):
                    data = response['rows'][i][j]
                    list.append(data)
                df.loc[len(df.index)] = list
            df.replace({'Channel ID': {'ids=VPnBCOtNVpcOk_n_aYeAxg':'Music',
                        'ids=gvyrn2bq4Akdefq3XIRfgA':'Affiliate',
                        'ids=Fjf1aHeWKjckbpg6IyRr9w':'O&O'}}, inplace=True)
   
    
    df_sum_up = df.loc[:, df.columns!='Date'].groupby(['Channel ID']).sum()
    df_sum_up.rename(index={'uploaderType%3D%3Dself':CMS_name}, inplace=True)
    if df.iat[0, 0] == 'uploaderType%3D%3Dself':
        df = df.drop('Channel ID', axis=1)

    return df, df_sum_up

def Claim_CID(claim_ID):
    claim_ID = claim_ID.replace("|",",")
    claim_ID = claim_ID.replace(";",",")
    claim_ID = claim_ID.replace(" ",",").split(",")
    claim_ID_list = list(filter(None,claim_ID)) #loại phần tử rỗng trong list
    n = 0
    access_token = get_access_token()
    for i in claim_ID_list:
        if n % 100 == 0:
            access_token = get_access_token()
        url = "https://www.googleapis.com/youtube/partner/v1/claims/"+ i + "?onBehalfOfContentOwner=" + CMS_ID + "&key=AIzaSyAsf5RBA8c9L4FzYayL8ZkPqWX4LtDkbTY"
        headers = {'Authorization': "Bearer " + access_token,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'}
        data = {"status":"active"}
        response = requests.patch(url, headers= headers, json = data)
        x = response.json()
        n = n +1
        st.write(n, "id: ", i, ", status: " , x['status'])

    st.write("done")


def channel_ID_checkbox():
    check = st.checkbox('Thêm ID Kênh')
    if check == True:
        channel_ID = st.text_input('Nhập ID kênh',placeholder = 'Có thể nhập nhiều Id được ngăn cách bởi dấu phẩy')
    else:
        channel_ID = ""  
    return channel_ID

def get_filter():
    st.write('Hãy chọn bộ lọc')
    # Chọn CMS
    CMS_name = st.selectbox(
        'Choose CMS',
        ('Music', 'O&O', 'Affiliate', 'All 3 CMS',)
    )

    if CMS_name == 'Music':
        CMS_list = ['ids=contentOwner%3D%3DVPnBCOtNVpcOk_n_aYeAxg']      
        channel_ID = channel_ID_checkbox()
    elif CMS_name == 'O&O':
        CMS_list = ['ids=contentOwner%3D%3DFjf1aHeWKjckbpg6IyRr9w']
        channel_ID = channel_ID_checkbox()
    elif CMS_name == 'Affiliate':
        CMS_list = ['ids=contentOwner%3D%3Dgvyrn2bq4Akdefq3XIRfgA']
        channel_ID = channel_ID_checkbox()
    else:
        CMS_list = ['ids=contentOwner%3D%3DVPnBCOtNVpcOk_n_aYeAxg',
                'ids=contentOwner%3D%3DFjf1aHeWKjckbpg6IyRr9w',
                'ids=contentOwner%3D%3Dgvyrn2bq4Akdefq3XIRfgA']
        channel_ID = ""
       
    col1, col2 = st.columns(2)

    #Chọn ngày tháng bắt đầu
    start_date = col1.date_input ( "Choose Start Date" , value=None , min_value=None , max_value=None , key=None )
    end_date = col2.date_input ( "Choose End Date" , value=None , min_value=None , max_value=None , key=None )

    #Chọn metric muốn xuất.
    st.write('Chọn chỉ tiêu')
    col1,col2,col3 = st.columns(3)
    metric_1_display = col1.multiselect('Các chỉ số về Lượt tiếp cận', ['Views','Premium View',  'Average View Duration', 'Average View Percentage'])
    metric_2_display = col2.multiselect('Các chỉ số về Lượt tương tác', ['Comments', 'Likes', 'Dislikes','Shares', 'Subscribers Gained','Subscribers Lost'])
    metric_3_display = col3.multiselect('Các chỉ số về Doanh thu', ['Revenue', 'Ads Revenue', 'Premium Revenue', 'CPM', 'Playback CPM'])
   
    #Custom Channel_ID
    if channel_ID != "":
        channel_ID = channel_ID.replace(";",",")
        channel_ID = channel_ID.replace(" ",",").split(",")
        channel_ID_list = list(filter(None,channel_ID)) #loại phần tử rỗng trong list
        channel_ID_list = list(map(lambda x: 'channel%3D%3D' + x, channel_ID_list))
    else:
        channel_ID_list = ['uploaderType%3D%3Dself']
    #Custom date and time
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    #Custom metric
    metric_display = metric_1_display + metric_2_display + metric_3_display
    metric_dict = {'Views':'views','Premium View':'redViews', 'Average View Duration': 'averageViewDuration', 'Average View Percentage': 'averageViewPercentage',
            'Comments':'comments', 'Likes': 'likes', 'Dislikes':'dislikes', 'Shares':'shares','Subscribers Gained':'subscribersGained','Subscribers Lost':'subscribersLost',
            'Revenue':'estimatedRevenue', 'Ads Revenue': 'estimatedAdRevenue', 'Premium Revenue': 'estimatedRedPartnerRevenue','CPM':'cpm', 'Playback CPM': 'playbackBasedCpm'}
    metric_list = []
    for i in metric_display:
        metric_list.append(metric_dict[i])
    metric = '%2C'.join([str(i) for i in metric_list])
    return CMS_list,  CMS_name, channel_ID_list, start_date, end_date, metric, metric_display
