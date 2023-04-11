import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rdp import rdp
import streamlit as st
from io import StringIO
st.set_page_config(page_title="rdp",layout="wide",page_icon = 'hs.png')

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Reduce the curve using Ramer–Douglas–Peucker algorithm")
st.header("Made by Ram -TECH SUPPORT II ")
st.subheader('Use only 2 column data .csv format to reduce the curve')
uploaded_file = st.file_uploader("Choose a csv file")
try:
 if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    # st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    # st.write(string_data)
 df=pd.read_csv(uploaded_file)

# st.dataframe(df)

 header_list = df.columns.values
 v1=header_list[0]
 v2=header_list[1]
 col1, col2 = st.columns(2)
 with col1:
  option = st.selectbox(
    'choose X component',
    (v1,v2))
 with col2:
  option2 = st.selectbox(
    'choose Y component',
    (v1,v2))
 x = df[option]
 y = df[option2]

 with col1:
  values = st.slider(
    'Select Epsilon',
    0.0,0.5,step=0.0001)
  st.write('Values:', values)
 points = np.column_stack([x,y])
 points_after_rdp=rdp(points, epsilon=values)
# print(points_after_rdp)
# print(len(x))
 A1=np.array(points_after_rdp[:, 0])
 A2=np.array(points_after_rdp[:, 1])
# print(len(A1))
# names=["True_strain","True_Stress (Mpa)"]
 CK= pd.DataFrame([A1,A2]).transpose()
 headerList = [option,option2]
 CK.columns=headerList
 CK.reset_index(drop=True)
# df2=pd.DataFrame(CK,columns=headerList)
 with col2:
  st.subheader("Reduced data points")
  st.dataframe(CK)

 def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

 csv = convert_df(CK)

# CK.to_csv('tx.csv',header=headerList,index=False)
 plt.plot(x,y,label='Input curve')
 plt.scatter(points_after_rdp[:, 0], points_after_rdp[:, 1], marker='o',color="red", label="Reduded curve")
 plt.legend()
 plt.xlabel(option)
 plt.ylabel(option2)
 with col1:
  st.pyplot()
 with col2:
  st.download_button(
    label="Download Reduced Data",
    data=csv,
    file_name='reduced_points.csv',
    mime='text/csv',
  )
except:
    st.write("")


