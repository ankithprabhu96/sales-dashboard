import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

### read excel
def read_csv(file):
    df = pd.read_csv(file)
    return df
df=pd.read_csv('data/sales.csv')
st.title('Sales Data Analysis')
st.write('This is a simple Streamlit app to ' \
'analyze sales data.')
st.write("shape of the dataset")
st.write(df.shape)
st.dataframe(df.head())
print(df.shape)


# file = st.file_uploader("Upload File")

# if file is not None:
#     st.write(f"Uploaded File: {file}")
#     st.write(f"File path: {file.name}")
    # df1 = pd.read_csv(file.upload_url)
    # print(df1.shape)

