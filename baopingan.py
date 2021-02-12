#_*_coding: utf-8 _*_
import datetime
import time
import requests
import json
import re
import os
import execjs
import traceback
import random
# import http.cookiejar as cj


def push_notices(title, desp=''):
    serverchan_url = 'https://sctapi.ftqq.com/'
    serverchan_key = os.environ["SERVERCHAN_KEY"]
    post_url = serverchan_url + serverchan_key + '.send'
    postdata = {'title': title, 'desp': desp}
    requests.get(post_url, postdata)


user = os.environ["USER"]
passwd = os.environ["PASSWORD"]

# 获取北京时间
utcnow = datetime.datetime.utcnow()
bjinow = utcnow + datetime.timedelta(hours=8)
bjitoday = bjinow.strftime("%Y-%m-%d")
print(bjinow)  # 输出北京时间

session = requests.Session()

healthurl = 'https://enroll.scut.edu.cn/door/health/h5/health.html'
loginurl = 'https://sso.scut.edu.cn/cas/login?service=https%3A%2F%2Fenroll.scut.edu.cn%2Fdoor%2Fhealth%2Fh5%2Fhealth.html'
geturl = 'https://enroll.scut.edu.cn/door/health/h5/get'
addurl = 'https://enroll.scut.edu.cn/door/health/h5/add'

getheaders = {
    'Host':
    'enroll.scut.edu.cn',
    "sec-ch-ua":
    '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile':
    '?0',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'Referer':
    'https://enroll.scut.edu.cn/door/health/h5/health.html',
    'Accept-Encoding':
    'gzip, deflate, br',
    'Accept-Language':
    'zh-CN,zh-HK;q=0.9,zh;q=0.8,ja-JP;q=0.7,ja;q=0.6,en-US;q=0.5,en;q=0.4'
}

addheaders = {
    "Host":
    "enroll.scut.edu.cn",
    "sec-ch-ua":
    "\"Google Chrome\";v=\"87\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"87\"",
    "Accept":
    "*/*",
    "X-Requested-With":
    "XMLHttpRequest",
    "sec-ch-ua-mobile":
    "?0",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Content-Type":
    "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin":
    "https://enroll.scut.edu.cn",
    "Referer":
    "https://enroll.scut.edu.cn/door/health/h5/health.html",
    "Accept-Encoding":
    "gzip, deflate, br",
    "Accept-Language":
    "zh-CN,zh-HK;q=0.9,zh;q=0.8,ja-JP;q=0.7,ja;q=0.6,en-US;q=0.5,en;q=0.4"
}

try:
    # 假装访问一下
    session.get(healthurl)

    #利用des.js文件加密，得到登陆表单数据rsa
    r = session.get(loginurl)
    lt = re.findall('name="lt" value="(.*?)"', r.text)[0]
    execution = re.findall('name="execution" value="(.*?)"', r.text)[0]

    with open('des.js') as f:
        ctx = execjs.compile(f.read())
    string1 = user + passwd + lt
    rsa = ctx.call('strEnc', string1, '1', '2', '3')

    #登陆所需的表单数据
    login_data = {
        'rsa': rsa,
        'ul': len(user),
        'pl': len(passwd),
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit'
    }
    #进行登陆
    # 随机延误
    time.sleep(random.randint(1, 10))
    session.post(loginurl, data=login_data)
except BaseException as e:
    msg = traceback.format_exc()
    print(msg)
    print("登录失败！")
    push_notices('github_scut_iamok系统登录失败！', msg)

try:
    # 随机延误
    time.sleep(random.randint(1, 10))
    getdata = session.get(geturl, headers=getheaders).json()['data']
except BaseException as e:
    msg = traceback.format_exc()
    print(msg)
    print("获取健康信息记录失败！")
    push_notices('github_scut_iamok获取上次健康信息记录失败！', msg)

lastdate = getdata['healthRptInfor']["dRptDate"]

if lastdate != bjitoday:
    try:
        # 随机延误
        time.sleep(random.randint(1, 10))

        params = [
            'dRptDate', 'sPersonName', 'sPersonCode', 'sPhone', 'sParentPhone',
            'iIsGangAoTai', 'iIsOversea', 'sHomeProvName', 'sHomeProvCode',
            'sHomeCityName', 'sHomeCityCode', 'sHomeCountyName',
            'sHomeCountyCode', 'sHomeAddr', 'iSelfState', 'iFamilyState',
            'sNowProvName', 'sNowProvCode', 'sNowCityName', 'sNowCityCode',
            'sNowCountyName', 'sNowCountyCode', 'sNowAddr', 'iNowGoRisks',
            'iRctRisks', 'iRctKey', 'iRctOut', 'iRctTouchKeyMan',
            'iRctTouchBackMan', 'iRctTouchDoubtMan', 'iRptState',
            'iPersonType', 'iSex', 'sCollegeName', 'sCampusName', 'sDormBuild',
            'sDormRoom', 'sMajorName', 'sClassName', 'iInSchool'
        ]

        adddata = {}

        for tables in ('healthRptPerson', 'healthRptInfor', 'basePersonAttr'):
            temp = getdata[tables]
            for (k, v) in temp.items():
                if k in params:
                    adddata[k] = v

        adddata["dRptDate"] = bjitoday

        addpost = session.post(addurl, adddata, headers=addheaders)

    except BaseException as e:
        msg = traceback.format_exc()
        print(msg)
        print("健康信息提交失败！")
        push_notices('github_scut_iamok健康信息提交失败！', msg)
    else:
        # f = open('iamok.log', 'w', encoding='utf-8')
        # f.write(
        #     time.strftime("%Y-%m-%d", time.localtime()) + "\n" +
        #     time.strftime("%H:%M:%S", time.localtime()) + "\n" + addpost.text)
        if addpost.json()['msg']=='执行成功!':
            print("您已成功提交健康信息！")
            # push_notices("github_scut_iamok健康信息已成功提交！", addpost.text)
        else:
            print("提交健康信息答复错误！/n返回信息错误")
            push_notices("github_scut_iamok提交健康信息答复错误！", addpost.text)
else:
    print('今天的健康信息已提交过了哦！')
    # with open('check_again.log', 'w', encoding='utf-8') as f:
    #     f.write(lastdate)
