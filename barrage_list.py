import requests
import re
import pandas as pd
from openpyxl import Workbook


def get_aid():  # 调用哔哩哔哩自带接口获取视频aid
    aid_list = []
    num = 42  # bilibili视频搜索页一页显示42个视频
    for page in range(1, 8, 1):
        if (page == 7):
            num = 6  # 300个视频除42余6
        url = 'https://api.bilibili.com/x/web-interface/wbi/search/type'  # api接口网址
        headers = {
            'Accept':
            'application/json, text/plain, */*',
            'Accept-Encoding':
            'gzip, deflate, br',
            'Accept-Language':
            'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cookie': 'buvid3=E67CB295-83A3-A563-E644-236AF830FBA673250infoc; b_nut=1692101073; i-wanna-go-back=-1; _uuid=10A5101496-1BB6-41A5-BC89-748C767D1107572173infoc; buvid4=5998C4A2-C9D5-0A48-E931-BC5142733CA474776-023081520-uUajf7V0bWzw\
                %2F3HUmWdhDfSR1xmc80cn4sUJHWIOoGX5Q3EKTkLa2Q%3D%3D; nostalgia_conf=-1; rpdid=0zbfVHbtw8|hoQQirQR|3Ib|3w1QvSNs; header_theme_version=CLOSE; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; buvid_fp_plain=undefined; DedeUserID=384702268; \
                    DedeUserID__ckMd5=afe9156cebbd8c67; b_ut=5; home_feed_column=5; browser_resolution=1872-924; fingerprint=53bf4653e22ae2b5c724a9ba669f6882; buvid_fp=a637bc4a9ec7f3b796e4405a7a515f7a; PVID=1; CURRENT_QUALITY=0; SESSDATA=3dcf46b3\
                        %2C1709459413%2C591d6%2A92_Ic9u_rYzUWmyqvGyjGOb4izxt8G8yMwhpo55v90CX7TjoDMhtREOPZQNU3fRDV35PqhIAAARAA; bili_jct=05995cffdbae6362647406c22adf3359; bp_video_offset_384702268=837812591758671881; bili_ticket=\
                            eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQxNjkxMTEsImlhdCI6MTY5MzkwOTkxMSwicGx0IjotMX0.4HVGLSXCrQ2U4fcx018BjGdbrMqQKqBkE1mXhc2Ut6I; bili_ticket_expires=1694169111; b_lsid=42F102AA1_18A6806DCEC;\
                                  sid=5xzz20pl',
            'Origin':
            'https://search.bilibili.com',
            'Referer':
            'https://search.bilibili.com/all?keyword=%E6%97%A5%E6%9C%AC%E6%A0%B8%E6%B1%A1%E6%B0%B4%E6%8E%92%E6%B5%B7&from_source=webtop_search&spm_id_from=333.1007&search_source=3&page=2&o=36',
            'Sec-Ch-Ua':
            "'Chromium';v='116', 'Not)A;Brand';v='24', 'Microsoft Edge';v='116'",
            'Sec-Ch-Ua-Mobile':
            '?0',
            'Sec-Ch-Ua-Platform':
            "Windows",
            'Sec-Fetch-Dest':
            'empty',
            'Sec-Fetch-Mode':
            'cors',
            'Sec-Fetch-Site':
            'same-site',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69'
        }
        params = {
            '_refresh__': 'true',
            '_extra': '',
            'context': '',
            'page': page,
            'page_size': num,
            'from_source': '',
            'from_spmid': '333.337',
            'platform': 'pc',
            'highlight': '1',
            'single_column': '0',
            'keyword': '日本核污水排海',
            'qv_id': 'hUNHoLasQHg1rRLFz9l8oJupm00F6uKc',
            'ad_resource': '5654',
            'source_tag': '3',
            'gaia_vtoken': '',
            'category_id': '',
            'search_type': 'video',
            'dynamic_offset': '36',
            'web_location': '1430654',
            'w_rid': 'f884f51a25d399ef101e3a4e7113ff7a',
            'wts': '1693964838'
        }
        response = requests.get(url=url, headers=headers, params=params)  # 调用requests方法获取json文件
        aid_json = response.json()  # 处理json文件获取aid数据
        aid_list.extend(aid_json['data']['result'])
    return aid_list


def get_oid(aid_list):  # 根据aid获取视频oid
    oid_list = []
    for i in aid_list:
        url = 'https://api.bilibili.com/x/player/pagelist?aid=' + str(i['id']) + '&jsonp=jsonp'  # 字符串拼接获取url
        r = requests.get(url=url)
        data = r.text
        oid_list.extend(re.findall('"cid":(.*?),', data))
    return oid_list


def get_barrage(oid_list):  # 根据视频oid直接调用b站接口获取弹幕数据
    barrage_list = []
    for oid in oid_list:
        url1 = 'https://api.bilibili.com/x/v1/dm/list.so?oid=' + str(oid)
        response = requests.get(url1)
        response.encoding = response.apparent_encoding
        barrage_list.extend(re.findall('<d p=".*?">(.*?)</d>', response.text))  # 利用正则表达式获取弹幕数据
    return barrage_list


def barrage_statistics(barrage):
    data = pd.Series(barrage)
    barrage_sorting = data.value_counts()
    danmu_dict = {}
    for i in range(20):  # 输出排名前二十的弹幕信息
        data = barrage_sorting.index[i]
        num = barrage_sorting[data]
        danmu_dict = {data: num}
        print(danmu_dict)
    return barrage_sorting


def create_workbook(barrage_sorting):
    wb = Workbook()  # 创建工作簿对象
    ws = wb['Sheet']  # 创建子表
    ws.append(['弹幕内容', '弹幕数量'])  # 添加表头
    for i in range(len(barrage_sorting)):
        data = barrage_sorting.index[i]
        d = data, barrage_sorting[data]
        ws.append(d)
    wb.save("barrage_statistics.xlsx")


def main():
    aid_list = get_aid()
    oid = get_oid(aid_list=aid_list)
    barrage = get_barrage(oid_list=oid)
    # 利用pands库对弹幕数据进行统计处理
    barrage_sorting = barrage_statistics(barrage=barrage)
    # 创建一个xlsx文件，将弹幕数据导入xlsx文件内
    create_workbook(barrage_sorting=barrage_sorting)


if __name__ == '__main__':
    main()
