import requests
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MeasureControl
from streamlit_folium import folium_static

st.title('景点间不同出行方式的路程和耗时')
# 读取CSV文件
#url="https://github.com/2000yyqx/Yangqian-QI/blob/main/CQ.csv"
#locations_df = pd.read_csv(url,encoding='utf-8')
locations_df = pd.read_csv(r'ChongQing.csv',encoding='gbk')

# 显示输入表单
start_location = st.selectbox('请选择起始地点', locations_df['景点名称'].values)
end_location = st.selectbox('请选择目的地点', locations_df['景点名称'].values)

# 匹配起始地和目的地的经纬度
start_coords = locations_df.loc[locations_df['景点名称'] == start_location, ['景点纬度', '景点经度']].squeeze()
end_coords = locations_df.loc[locations_df['景点名称'] == end_location, ['景点纬度', '景点经度']].squeeze()

# 创建地图
m = folium.Map(location=[end_coords['景点纬度'], end_coords['景点经度']], zoom_start=14, control_scale=True)
MeasureControl().add_to(m)

# 添加起始和目的地标记
folium.Marker([start_coords['景点纬度'], start_coords['景点经度']], popup=start_location).add_to(m)
folium.Marker([end_coords['景点纬度'], end_coords['景点经度']], popup=end_location).add_to(m)

api_key = 'edDhvvYKU8qh9KdV5f2CvBg73GSVrMy2'
def get_driving_route(start_coords, end_coords):
    url = f"http://api.map.baidu.com/directionlite/v1/driving?origin={start_coords['景点纬度']},{start_coords['景点经度']}&destination={end_coords['景点纬度']},{end_coords['景点经度']}&ak={api_key}"
    response = requests.get(url)
    data = response.json()

    if 'result' in data and 'routes' in data['result'] and len(data['result']['routes']) > 0:
        route = data['result']['routes'][0]
        distance = route['distance']  # 路线长度，单位：米
        duration = route['duration']  # 预计耗时，单位：秒
        return distance, duration
    
    return None, None

# 获取步行路线和耗时
def get_walking_route(start_coords, end_coords):
    url = f"http://api.map.baidu.com/directionlite/v1/walking?origin={start_coords['景点纬度']},{start_coords['景点经度']}&destination={end_coords['景点纬度']},{end_coords['景点经度']}&ak={api_key}"
    response = requests.get(url)
    data = response.json()

    if 'result' in data and 'routes' in data['result'] and len(data['result']['routes']) > 0:
        route = data['result']['routes'][0]
        distance = route['distance']  # 路线长度，单位：米
        duration = route['duration']  # 预计耗时，单位：秒
        return distance, duration
    
    return None, None

# 获取公交路线和耗时
def get_transit_route(start_coords, end_coords):
    url = f"http://api.map.baidu.com/directionlite/v1/transit?origin={start_coords['景点纬度']},{start_coords['景点经度']}&destination={end_coords['景点纬度']},{end_coords['景点经度']}&ak={api_key}"
    response = requests.get(url)
    data = response.json()

    if 'result' in data and 'routes' in data['result'] and len(data['result']['routes']) > 0:
        route = data['result']['routes'][0]
        distance = route['distance']  # 路线长度，单位：米
        duration = route['duration']  # 预计耗时，单位：秒
        return distance, duration
    
    return None, None

# 在Streamlit中显示地图
folium_static(m)

# 在Streamlit应用程序中调用API函数，并显示路线和耗时信息
if st.button('生成路程（km）和耗时(分钟)'):
    driving_distance, driving_duration = get_driving_route(start_coords, end_coords)
    walking_distance, walking_duration = get_walking_route(start_coords, end_coords)
    transit_distance, transit_duration = get_transit_route(start_coords, end_coords)

    if driving_distance is not None:
        st.write('驾车路程：', driving_distance/1000)
    else:
        st.write('无可用驾车路线')

    if driving_duration is not None:
        st.write('驾车耗时：', driving_duration//60)
    else:
        st.write('无可用驾车耗时信息')

    if walking_distance is not None:
        st.write('步行路程：', walking_distance/1000)
    else:
        st.write('无可用步行路线')

    if walking_duration is not None:
        st.write('步行耗时：', walking_duration//60)
    else:
        st.write('无可用步行耗时信息')

    if transit_distance is not None:
        st.write('公交路程：', transit_distance/1000)
    else:
        st.write('无可用公交路线')

    if transit_duration is not None:
        st.write('公交耗时：', transit_duration//60)
    else:
        st.write('无可用公交耗时信息')

