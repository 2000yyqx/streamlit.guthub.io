import requests
import streamlit as st
import pandas as pd
# 百度地图API密钥
api_key = 'edDhvvYKU8qh9KdV5f2CvBg73GSVrMy2'

st.title('景点附近感兴趣点查询（学校、酒店、医院、银行、商场）')
# 获取POI点
def get_poi(location, radius, poi_type):
    url = f"http://api.map.baidu.com/place/v2/search?query={poi_type}&location={location}&radius={radius}&output=json&ak={api_key}"
    response = requests.get(url)
    data = response.json()

    # 解析数据，获取POI点名称
    pois = data['results']

    poi_names = []
    for poi in pois:
        name = poi['name']
        poi_names.append(name)

    return poi_names

# Streamlit应用程序
def main():
    st.title("POI点查询")
    #url="https://github.com/2000yyqx/Yangqian-QI/blob/main/CQ.csv"
    #locations_df = pd.read_csv(url,encoding='utf-8')
    locations_df = pd.read_csv(r'ChongQing.csv',encoding='gbk')
    places= st.selectbox("请选择一个景点",locations_df['景点名称'].values)
    place=locations_df.loc[locations_df['景点名称'] ==places, ['景点纬度', '景点经度']].squeeze()
    lat=place["景点纬度"]
    lng=place["景点经度"]
    location=f"{lat},{lng}"
    radius = st.slider("请选择邻近距离（米）：",0,5000,2000)
    poi_type = st.selectbox("请选择POI类型：", ['学校', '医院', '酒店', '银行', '商场'])

    if st.button("查询"):
        if location:
            pois = get_poi(location, radius, poi_type)
            if pois:
                st.subheader(f"附近的{poi_type}有：")
                for poi_name in pois:
                    st.write(poi_name)
            else:
                st.write("未找到相关的POI点")
        else:
            st.warning("请输入地点坐标")

if __name__ == "__main__":
    main()
