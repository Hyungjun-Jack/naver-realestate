import requests
import json
import xmltodict

from threading import Timer


period = 10


aptSeqs = {
    "용현자이크레스트" : "28177-6824",
    "인천 SK Sky VIEW" : "28177-6035",
    "엘에이치미추홀퍼스트" : "28177-6446",
}


def get_data():
    headers = {
    'accept': '*/*',
    }

    params = {
        'LAWD_CD': '28177',
        'DEAL_YMD': '202503',
        'serviceKey': 'c9kMarZn2s9YL7PZtEE/Xao+7KlEfF90wAgcvpNhzLs08xuY4Fby4+mgaYnpvUAFd5N9pJxEslrPWvYXJ0ymuA==',
        'pageNo': '1',
        'numOfRows': '10000',
    }

    response = requests.get(
        'http://apis.data.go.kr/1613000/RTMSDataSvcAptRent/getRTMSDataSvcAptRent',
        params=params,
        headers=headers,
    )

    xml = xmltodict.parse(response.text)
    json_data = json.loads(json.dumps(xml))

    items = json_data["response"]["body"]["items"]["item"]


    filtered_items = [item for item in items if item["aptNm"] in aptSeqs.keys()]

    # print(json.dumps(filtered_items, indent=4, ensure_ascii=False))
    for item in filtered_items:
        # print(item)
        print(item["aptNm"], item["dealYear"], item["dealMonth"], item["dealDay"], item["floor"], item["excluUseAr"], item["deposit"], item["monthlyRent"])


def period_job():
    print("period_job")
    get_data()
    # Timer(period, period_job).start()


period_job()


if __name__ == "__main__":
    while 1:
        pass