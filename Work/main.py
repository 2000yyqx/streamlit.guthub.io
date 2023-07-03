import pandas as pd
import folium
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import folium_static
st.title('重庆旅游简易导览（下方为景点热力图）')
# 读取CSV文件
#url="https://github.com/2000yyqx/Yangqian-QI/blob/main/CQ.csv"
#locations_df = pd.read_csv(url,encoding='utf-8')
locations_df = pd.read_csv(r'ChongQing.csv',encoding='gbk')
# 创建地图
m = folium.Map(location=[29.5636, 106.5516], zoom_start=12)

# 提取经纬度数据
heat_data = locations_df[['景点纬度', '景点经度']].values

# 生成热力图
HeatMap(heat_data).add_to(m)

# 在Streamlit中显示地图
folium_static(m)
