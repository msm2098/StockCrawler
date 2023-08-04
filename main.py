from importlist import *
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
url2 = 'https://finance.naver.com/sise/field_submit.naver?menu=market_sum&returnUrl=http://finance.naver.com/sise/sise_market_sum.naver?&page=&fieldIds=open_val&fieldIds=high_val&fieldIds=low_val'
session = requests.Session()
session.headers.update(headers)  # 헤더정보 업데이트

# 체크박스를 통해서 원하는 항목 업데이트
field_update_data = {"menu": "market_sum", "returnUrl": "http://finance.naver.com/sise/sise_market_sum.naver?&page=", "fieldIds": "open_val",
                     "fieldIds": "high_val", "fieldIds": "low_val"}
ups = session.get(url2, data=field_update_data)
print(ups.status_code)


get_info = session.get(url)
file = open('test.html', 'w')
file.write(get_info.text)


for idx in range(1, 42):  # 페이지가 40까지 있음
    page = session.get(url+str(idx)).text
    df = pandas.read_html(page)[1]
    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)
    if len(df) == 0:
        break

    f_name = "sise.csv"
    if os.path.exists(f_name):
        df.to_csv(f_name, encoding='utf-8-sig',
                  index=False, mode="a", header=False)
    else:
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f"{idx} 페이지 완료")
