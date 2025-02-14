import streamlit as st
import requests
import pandas as pd

# Streamlit page setup
st.set_page_config(page_title="Real Estate Listings Viewer", layout="wide")
st.title("Real Estate Listings from Pages 1 to 10")
st.markdown("This page fetches and displays real estate listings from pages 1 to 10 using the Naver Real Estate API.")

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

# Function to get data from the API for pages 1 to 10
@st.cache_data
def fetch_all_data():
    all_articles = []
    for page in range(1, 11):
        try:
            # Make the request for the specific page
            # url = f'https://new.land.naver.com/api/articles/complex/111515?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount=300&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=111515&buildingNos=&areaNos=&type=list&order=prc'
            # url = f'https://new.land.naver.com/api/articles/complex/117911?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount=300&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=111515&buildingNos=&areaNos=&type=list&order=prc'
            # url = f'https://new.land.naver.com/api/articles/complex/117911?realEstateType=APT%3APRE&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=117911&buildingNos=&areaNos=&type=list&order=rank'
            url = f'https://new.land.naver.com/api/articles/complex/117911?realEstateType=APT%3APRE&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=117911&buildingNos=&areaNos=&type=list&order=rank'
            response = requests.get(url, cookies=cookies, headers=headers)

            print(response)

            # Verify response is valid JSON
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articleList", [])
                all_articles.extend(articles)
            else:
                st.warning(f"Failed to retrieve data for page {page}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except ValueError:
            st.error(f"Non-JSON response for page {page}.")

    return all_articles

# Fetch data for all pages
data = fetch_all_data()

# Transform data into a DataFrame if data is available
if data:
    df = pd.DataFrame(data)
    # Select columns to display
    # df_display = df[["articleNo", "articleName", "realEstateTypeName", "tradeTypeName", "floorInfo",
    #                  "dealOrWarrantPrc", "areaName", "direction", "articleConfirmYmd", "articleFeatureDesc",
    #                  "tagList", "buildingName", "sameAddrMaxPrc", "sameAddrMinPrc", "realtorName"]]
    df_display = df[["articleNo", "buildingName", "tradeTypeName", "floorInfo",
                     "dealOrWarrantPrc", "sameAddrCnt", "areaName", "direction", "articleFeatureDesc",
                     "sameAddrMinPrc", "sameAddrMaxPrc",  "realtorName"]]

    # df_display.sort_values(['buildingName', 'tradeTypeName', 'dealOrWarrantPrc'], ascending=[True, True, True], inplace=True)

    # Display the table in Streamlit with a clean, readable layout
    st.write("### Real Estate Listings - Pages 1 to 10")
    st.dataframe(df_display)
else:
    st.write("No data available.")
