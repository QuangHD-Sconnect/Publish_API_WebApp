#Khai báo thư viện
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
import streamlit_authenticator as stauth


st.header("Youtube API")

names = ["Tubrr"]
usernames = ["Tubrr"]
#load hashed passwords
file_path = Path(__file__).parent/"hashed_pw.pkl"
with file_path.open("rb") as file:
	hash_passwords = pickle.load(file)

authenticator =stauth.Authenticate(names, usernames, hash_passwords, "API web", "abcdef", cookie_expiry_days=30)

names, authentication_status, usernames = authenticator.login("Login", "main")

if authentication_status == False:
	st.error("Username/Password is incorrect")
if authentication_status == None:
	st.warning("Please enter your username and password")
if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.write("Chọn hành động bạn cần làm với Youtube API")
    action_1 = st.selectbox(
            'Bạn muốn làm gì?',
            ('Thu thập dữ liệu', 'Content ID')
        )
    if action_1 == 'Thu thập dữ liệu':
        CMS_list,  CMS_name, channel_ID_list, start_date, end_date, metric, metric_display = get_filter()
        if st.button('OK'):
            access_token = get_access_token()
            df, df_sum_up = get_data(CMS_list,  CMS_name, channel_ID_list, start_date, end_date, metric, metric_display, access_token)
            st.markdown('##')
            st.write('Bảng thống kê')
            st.write(df_sum_up)
            st.markdown('##')
            st.write('Bảng thống kê theo từng ngày')
            st.write(df)

    else:
        st.write('Hãy chọn bộ lọc')
        # Chọn CMS
        CMS_name = st.selectbox(
            'Chọn CMS',
            ('Music', 'O&O', 'Affiliate')
        )

        if CMS_name == 'Music':
            CMS_ID = 'VPnBCOtNVpcOk_n_aYeAxg'      
        elif CMS_name == 'O&O':
            CMS_ID = 'Fjf1aHeWKjckbpg6IyRr9w'
        elif CMS_name == 'Affiliate':
            CMS_ID = 'igvyrn2bq4Akdefq3XIRfgA'

        claim_ID = st.text_input('Nhập Claim ID',placeholder = 'Có thể nhập nhiều Id được ngăn cách bởi dấu phẩy hoặc cách')
        if st.button('OK'):
            if claim_ID != "":
                Claim_CID(claim_ID)
                
