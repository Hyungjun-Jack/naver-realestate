import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import math
from sqlalchemy import create_engine

# Streamlit page setup
st.set_page_config(page_title="네이버부동산 매물", layout="wide")
# st.title("Real Estate Listings from Pages 1 to 10")
# st.markdown("This page fetches and displays real estate listings from pages 1 to 10 using the Naver Real Estate API.")

buildingNames = {
    "더샵부평센트럴시티":147824,
    "e편한세상부평그랑힐스":139343,
    "올림픽파크포레온":155817,
    "래미안용산더센트럴(주상복합)":109123,
    "센트럴파크(주상복합)":117804,
    "용현자이크레스트":142022,
    "용현엘크루윈드포레": 117911,
    "인천SK스카이뷰": 107437,
    "힐스테이트숭의역(주상복합)":145969,
    "힐스테이트숭의역(오피스텔)":143998,
    "힐스테이트학익":123141,
    "시티오씨엘1단지":142108,
    "시티오씨엘3단지(주상복합)":140483,
    "시티오씨엘3단지(오피스텔)":140258,
    "시티오씨엘4단지(주상복합)":144065,
    "시티오씨엘4단지(오피스텔)":143861,
    "래미안라그란데": 163360,
    "이문아이파크자이(3-1BL)": 174562,
    "휘경자이디센시아": 157123,
    "휘경SK뷰": 112482,
    "장위자이레디언트": 160539,
}


# Function to get data from the API for pages 1 to 10
@st.cache_data(show_spinner="데이터 조회 중...")
def fetch_all_data(complex):
    all_articles = []

    page = 1

    while True:
        try:
            # Make the request for the specific page
            # url = f'https://new.land.naver.com/api/articles/complex/111515?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount=300&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=111515&buildingNos=&areaNos=&type=list&order=prc'
            # url = f'https://new.land.naver.com/api/articles/complex/117911?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount=300&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=111515&buildingNos=&areaNos=&type=list&order=prc'
            # url = f'https://new.land.naver.com/api/articles/complex/117911?realEstateType=APT%3APRE&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=117911&buildingNos=&areaNos=&type=list&order=rank'
            url = f'https://new.land.naver.com/api/articles/complex/{complex}?realEstateType=APT%3APRE&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=117911&buildingNos=&areaNos=&type=list&order=rank'
            response = requests.get(url, cookies=cookies, headers=headers)

            # Verify response is valid JSON
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articleList", [])


                if len(articles) > 0:
                    all_articles.extend(articles)
                else:
                    break
            else:
                st.warning(f"Failed to retrieve data for page {page}. Status code: {response.status_code}")
                break
            page = page + 1
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except ValueError:
            st.error(f"Non-JSON response for page {page}.")

    return all_articles

def print_func():
    now = datetime.now()
    print(f'{now.minute}m{now.second}s')
    for i in st.session_state.keys():
        if i.startswith('dynamic_checkbox_') and st.session_state[i]:
            st.session_state[i] = False

st.write("### 아파트 선택")
articleName = st.selectbox("아파트 선택", list(buildingNames.keys()), label_visibility="hidden")
complex = buildingNames[articleName]

if "complex" not in st.session_state:
    st.session_state.complex = complex

if st.session_state.complex != complex:
    st.session_state.complex = complex
    print_func()
    fetch_all_data.clear()

if 'checkbox_매매' not in st.session_state:
    st.session_state['checkbox_매매'] = "0"
    st.session_state['checkbox_전세'] = "0"
    st.session_state['checkbox_월세'] = "0"

# MySQL 데이터베이스 연결 설정
user = "root"
password = "yes_yes0716"
host = "localhost"
port = 3306
database = "test_db"

if "engine" not in st.session_state:
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
    st.session_state.engine = engine

# if complex:

#     for i in st.session_state.keys():
#         if i.startswith('dynamic_checkbox_') and st.session_state[i]:
#             print("WHAT")
#             st.session_state[i] = False


# Define the cookies and headers as provided
cookies = {
    'NNB': '2NWNJKPJZKOWO',
    '_fwb': '83jmvbZeoW1P82PFaiDHtf.1738549557392',
    'landHomeFlashUseYn': 'Y',
    '_fwb': '83jmvbZeoW1P82PFaiDHtf.1738549557392',
    'nid_inf': '23232436',
    'NID_AUT': 'KkBR8BO9TRLU5qDUH7RZHhyJwZ8QtwkXYxdyO1qdROV/XS1Tnla6tv55vFJ/LfWK',
    'NID_JKL': '0/Wr/dyApEdpKByiscnVUFhT2D3otzPbb3tj2K/nuyo=',
    'NSCS': '2',
    'ASID': '0e2332a000000194df1babc90000004f',
    'NAC': 'B04bBgAHTTlfB',
    'REALESTATE': 'Thu%20Feb%2013%202025%2010%3A40%3A23%20GMT%2B0900%20(Korean%20Standard%20Time)',
    'NACT': '1',
    'page_uid': 'iI2Zsdqo1fsss4zJSLdssssst/K-061112',
    'SRT30': '1739430247',
    'NID_SES': 'AAAB42GYKteZS2YspLhgQau+xQgefMGpTBWqB/okFqSjK3Y20q0yUyx2jM/i+mCyaTf9IPX0zN3JSNkWuy3mSFw9D1TnrI90P3kwAbUqgZ5VQx05l2+8hVfqLnBksY4GfMQLhnw7UZK9eRSdjo+38RzaGIDFmehOjbfFw7SCP7tryrffBOdkLYHpdXfymsm0m6eyDi9TdgQlUH9p1KGw9r9FZwQtuCsK1kGydNvL7XiHQLpNe6jglWVKtORsbbJM4mwQehotrQ0K5ExrOMCgBQoFbyZZbuAk5e+dAtf3HWB84gIS/YaJxFc+0TqphJbodiWdPaT0COSk4M78mfhrgATDdIktoa2K/awYkcaiP3bBoGRpTgvxqbX2x/UAMf81BTZJgaYb67b+YQJpQQLBIzqx8+j6FoiJdrW/IF4ilVsLrA+0LRgnauz5vOo2hZ07o1HTYbqZV5CY70zPI9ukcdikpGelHMCrRAKQPbnTgzXKAys52tI4qk/cCq3Rn6BGSirN4NO72SAUy2HJQEvMgXnESa3D3d8J5HjciX02ut4iG4Kk62byoqZJjJ6QMnJ5fgILttMW60VoGTuP40QlDyLUo9NqwzJv6IaTfdF5Bw8QY2As7/QR2954pXxSbQx2wVlPG33qvVgwioAi0xDaqA0Bw8k=',
    'SRT5': '1739434133',
    'BUC': 'pj4SHX-9hg4jXZBY181BeNE5e8fzoerDI6foH4RAngU=',
}
headers = {
    'accept': '*/*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3Mzk0MTA4MjMsImV4cCI6MTczOTQyMTYyM30.35U17aoAs2BVOE6TQFpaWelEj820PIMbc3yZ12h2Te4',
    'priority': 'u=1, i',
    'referer': 'https://new.land.naver.com/complexes/117911?ms=37.4570849,126.6442774,17&a=APT:PRE&e=RETAIL&ad=true',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    # 'cookie': 'NNB=2NWNJKPJZKOWO; _fwb=83jmvbZeoW1P82PFaiDHtf.1738549557392; landHomeFlashUseYn=Y; _fwb=83jmvbZeoW1P82PFaiDHtf.1738549557392; nid_inf=23232436; NID_AUT=KkBR8BO9TRLU5qDUH7RZHhyJwZ8QtwkXYxdyO1qdROV/XS1Tnla6tv55vFJ/LfWK; NID_JKL=0/Wr/dyApEdpKByiscnVUFhT2D3otzPbb3tj2K/nuyo=; NSCS=2; ASID=0e2332a000000194df1babc90000004f; NAC=B04bBgAHTTlfB; REALESTATE=Thu%20Feb%2013%202025%2010%3A40%3A23%20GMT%2B0900%20(Korean%20Standard%20Time); NACT=1; page_uid=iI2Zsdqo1fsss4zJSLdssssst/K-061112; SRT30=1739430247; NID_SES=AAAB42GYKteZS2YspLhgQau+xQgefMGpTBWqB/okFqSjK3Y20q0yUyx2jM/i+mCyaTf9IPX0zN3JSNkWuy3mSFw9D1TnrI90P3kwAbUqgZ5VQx05l2+8hVfqLnBksY4GfMQLhnw7UZK9eRSdjo+38RzaGIDFmehOjbfFw7SCP7tryrffBOdkLYHpdXfymsm0m6eyDi9TdgQlUH9p1KGw9r9FZwQtuCsK1kGydNvL7XiHQLpNe6jglWVKtORsbbJM4mwQehotrQ0K5ExrOMCgBQoFbyZZbuAk5e+dAtf3HWB84gIS/YaJxFc+0TqphJbodiWdPaT0COSk4M78mfhrgATDdIktoa2K/awYkcaiP3bBoGRpTgvxqbX2x/UAMf81BTZJgaYb67b+YQJpQQLBIzqx8+j6FoiJdrW/IF4ilVsLrA+0LRgnauz5vOo2hZ07o1HTYbqZV5CY70zPI9ukcdikpGelHMCrRAKQPbnTgzXKAys52tI4qk/cCq3Rn6BGSirN4NO72SAUy2HJQEvMgXnESa3D3d8J5HjciX02ut4iG4Kk62byoqZJjJ6QMnJ5fgILttMW60VoGTuP40QlDyLUo9NqwzJv6IaTfdF5Bw8QY2As7/QR2954pXxSbQx2wVlPG33qvVgwioAi0xDaqA0Bw8k=; SRT5=1739434133; BUC=pj4SHX-9hg4jXZBY181BeNE5e8fzoerDI6foH4RAngU=',
}



# Fetch data for all pages
data = fetch_all_data(complex)

def get_selected_checkboxes():
    return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]

def get_selected_area_type():
    return [int(i.replace('area_checkbox_','')) for i in st.session_state.keys() if i.startswith('area_checkbox_') and st.session_state[i]]
    
def get_selected_trade_type():
    return [i.replace('trade_type_checkbox_','') for i in st.session_state.keys() if i.startswith('trade_type_checkbox_') and st.session_state[i]]

def update_label(labels):
    # st.write(labels)
    
    if "매매" in labels.index:
        st.session_state['checkbox_매매'] = labels["매매"]
    else:
        st.session_state['checkbox_매매'] = "0"
    if "월세" in labels.index:
        st.session_state['checkbox_월세'] = labels["월세"]
    else:
        st.session_state['checkbox_월세'] = "0"
    if "전세" in labels.index:
        st.session_state['checkbox_전세'] = labels["전세"]
    else:
        st.session_state['checkbox_전세'] = "0"
    
    cols = st.columns([3, 3, 3, 20])

    cols[0].checkbox(f"매매({st.session_state['checkbox_매매']})", key="trade_type_checkbox_" + "매매")
    cols[1].checkbox(f"전세({st.session_state['checkbox_전세']})", key="trade_type_checkbox_" + "전세")
    cols[2].checkbox(f"월세({st.session_state['checkbox_월세']})", key="trade_type_checkbox_" + "월세")

def save_to_db(dataframe):
    # print(dataframe[["생성일", "단지"]])
    # print(st.session_state.engine)
    dataframe.to_sql("article_list", con=st.session_state.engine, if_exists="append", index=False)

def read_from_db(articleName, selected_buildings, selected_area, selected_trade_type):
    column_names = ["번호", 
                    "단지",
                    "등록일", 
                    "거래", 
                    "동",  
                    "층", 
                    "타입", 
                    "향", 
                    "동일매물", 
                    "동일가격 최소", 
                    "동일가격 최대", 
                    "가격변동", 
                    "중개사무소", 
                    "중개사무소ID",
                    "매물설명",
                    "전용면적", 
                    "DB저장일시"
                    ]
    
    # 현재 날짜 가져오기
    today = datetime.today()

    # 어제 날짜 계산
    yesterday = today - timedelta(days=1)

    # 어제 00:00:00 (YYYY-MM-DD HH:MM:SS)
    start_time = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")

    # 어제 23:59:59 (YYYY-MM-DD HH:MM:SS)
    end_time = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    query = f"SELECT * FROM article_list where articleName='{articleName}' and create_date <= '{end_time_str}'"
    # query = f"SELECT * FROM article_list where articleName='{articleName}'"

    st.markdown(query)

    df_from_db = pd.read_sql(query, con=st.session_state.engine)

    if len(selected_buildings) > 0:
        df_from_db = df_from_db.loc[df_from_db['buildingName'].isin(selected_buildings)]

    if len(selected_area) > 0:
        df_from_db = df_from_db.loc[df_from_db['area2'].isin(selected_area)]

    if len(selected_trade_type) > 0:
        df_from_db = df_from_db.loc[df_from_db['tradeTypeName'].isin(selected_trade_type)]

    df_from_db['articleNo'] = df_from_db["articleNo"].apply(lambda x:f"https://new.land.naver.com/complexes/{complex}?articleNo={x}")
    df_from_db['realtorId'] = df_from_db["realtorId"].apply(lambda x:f"https://new.land.naver.com/complexes/{complex}?realtorId={x}")

    df_from_db.columns = column_names

    df_from_db.insert(0, 'DB저장일시', df_from_db.pop('DB저장일시'))

    st.dataframe(df_from_db.drop(columns=['전용면적', '단지']), column_config={
        "번호": st.column_config.LinkColumn("매물보기", display_text="매물보기"),
        "중개사무소ID": st.column_config.LinkColumn("중개사보기", display_text="중개사보기"),
    })

# Transform data into a DataFrame if data is available
if data:
    
    df = pd.DataFrame(data)
    # Select columns to display
    # df_display = df[["articleNo", "articleName", "realEstateTypeName", "tradeTypeName", "floorInfo",
    #                  "dealOrWarrantPrc", "areaName", "direction", "articleConfirmYmd", "articleFeatureDesc",
    #                  "tagList", "buildingName", "sameAddrMaxPrc", "sameAddrMinPrc", "realtorName"]]

    df["areaName"] = df["areaName"] + "/" + df["area2"].astype(str) + "㎡"

    df_display = df[["articleNo", 
                     "articleName", 
                     "articleConfirmYmd", 
                     "tradeTypeName", 
                     "buildingName", 
                     "floorInfo",
                     "areaName", 
                     "direction", 
                     "sameAddrCnt", 
                     "sameAddrMinPrc", 
                     "sameAddrMaxPrc",  
                     "priceChangeState", 
                     "realtorName", 
                     "realtorId", 
                     "articleFeatureDesc",
                     "area2", ]].copy()

    # df_display.sort_values(['buildingName', 'tradeTypeName', 'dealOrWarrantPrc'], ascending=[True, True, True], inplace=True)

    # df_temp = df_display.loc[df_display["tradeTypeName"] == "매매"].copy()
    df_temp = df_display

    buildings = sorted(df_temp['buildingName'].unique())
    
    column_width = [1 for i in buildings]

    if len(buildings) < 10:
        column_width.append(10)

    cols = st.columns(column_width)

    for index, building in  enumerate(buildings):
        with cols[index]:
            st.checkbox(building,  key='dynamic_checkbox_' + building)

    areas = sorted(df_temp['area2'].unique())

    column_width = [3 for i in areas]

    if len(areas) < 10:
        column_width.append(20)

    cols = st.columns(column_width)

    for index, area in enumerate(areas):
        with cols[index]: 
            st.checkbox(f'{area}',  key=f'area_checkbox_{area}')
           
    # print(df_temp['realtorName'].value_counts())
    
    selected_buildings = get_selected_checkboxes()
    selected_area = get_selected_area_type()
    selected_trade_type = get_selected_trade_type()

    if len(selected_buildings) > 0:
        df_temp = df_temp.loc[df_temp['buildingName'].isin(selected_buildings)]

    if len(selected_area) > 0:
        df_temp = df_temp.loc[df_temp['area2'].isin(selected_area)]

    if len(selected_trade_type) > 0:
        df_temp = df_temp.loc[df_temp['tradeTypeName'].isin(selected_trade_type)]


    cols = st.columns([3, 3, 3, 20])

    trade_types = df_temp["tradeTypeName"].value_counts()

    trade_labels = ["매매", "전세", "월세"]

    for i, label in enumerate(trade_labels):
        count = trade_types.get(label, 0)  # 키가 없을 경우 기본값 0
        selected = next((True for i, v in enumerate(selected_trade_type) if v == label), False)
        
        cols[i].checkbox(f"{label}({count})", value=selected, key=f"trade_type_checkbox_{label}")

    # Display the table in Streamlit with a clean, readable layout
    st.write("### 네이버 부동산 매물")

    df_origin = df_temp.copy()

    column_names = ["번호", 
                    "단지",
                    "등록일", 
                    "거래", 
                    "동",  
                    "층", 
                    "타입", 
                    "향", 
                    "동일매물", 
                    "동일가격 최소", 
                    "동일가격 최대", 
                    "가격변동", 
                    "중개사무소", 
                    "중개사무소ID",
                    "매물설명",
                    "전용면적", 
                    ]


    test = df_temp.groupby(['tradeTypeName', "area2"])

    min = test["sameAddrMinPrc"].min()
    max = test["sameAddrMaxPrc"].max()
    count = test["area2"].value_counts()
    
    statistic = pd.concat([min, max, count], axis=1)

    statistic = statistic.rename(columns={'sameAddrMinPrc':'동일가격 최소', 'sameAddrMaxPrc':'동일가격 최대', 'count': '매물수',})
    statistic = statistic.rename_axis(["거래", "전용면적"], axis=0)

    st.dataframe(statistic, width=500)

    df_temp['articleNo'] = df_temp["articleNo"].apply(lambda x:f"https://new.land.naver.com/complexes/{complex}?articleNo={x}")
    df_temp['realtorId'] = df_temp["realtorId"].apply(lambda x:f"https://new.land.naver.com/complexes/{complex}?realtorId={x}")

    # https://new.land.naver.com/complexes/145969?realtorId=mis770414

    df_temp["articleConfirmYmd"] = pd.to_datetime(df_temp["articleConfirmYmd"], format="%Y%m%d")

    df_temp["articleConfirmYmd"] = df_temp["articleConfirmYmd"].dt.date

    df_temp.columns = column_names

    st.dataframe(df_temp.drop(columns=['전용면적', '단지']), column_config={
        "번호": st.column_config.LinkColumn("매물보기", display_text="매물보기"),
        "중개사무소ID": st.column_config.LinkColumn("중개사보기", display_text="중개사보기"),
    },)

    df_origin["create_date"] = datetime.now()
    
    # cols = st.columns([3, 3, 20])

    # with cols[0]:
    if st.button("DB에 저장"):
        save_to_db(df_origin)

    # with cols[1]:
    if st.button("지난 데이터 조회"):
        read_from_db(articleName, selected_buildings, selected_area, selected_trade_type)
else:
    st.write("No data available.")
