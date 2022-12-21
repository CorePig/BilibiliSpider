import requests
headers = {
"authority": "api.bilibili.com",
"method": "GET",
"path": "/x/v2/dm/web/history/seg.so?type=1&oid=808284217&date=2022-10-03",
"scheme": "https",
# "accept": "application/json, text/plain, */*",
# "accept-encoding": "gzip, deflate, br",
# "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
# "cookie": "buvid3=8AA5AF44-1224-42AC-AA47-6F5BAB7ABA12138378infoc; rpdid=|(JYlmkm|JmR0J'uY|RJ|m~Y|; LIVE_BUVID=AUTO7216309177959752; _uuid=3838ADE4-D936-FEEB-DE68-32173A5F777130941infoc; CURRENT_QUALITY=80; video_page_version=v_old_home; buvid4=12EE9EE4-B027-088E-E6AE-9BEB8A60E25349670-022012612-OiqJJgeV6VRyf6OrX1wL5A%3D%3D; nostalgia_conf=-1; CURRENT_BLACKGAP=0; hit-dyn-v2=1; i-wanna-go-back=-1; buvid_fp_plain=undefined; DedeUserID=349405615; DedeUserID__ckMd5=e0c3d8270d202edd; b_ut=5; blackside_state=0; fingerprint=98f34c97701ac24ca8e8dc1473cc0878; buvid_fp=98f34c97701ac24ca8e8dc1473cc0878; b_nut=100; SESSDATA=5b46e5cc%2C1678442024%2C795af%2A91; bili_jct=170edf326ad6cd1d3e36a48426c3c6c9; sid=7fizsdkf; bp_video_offset_349405615=713061293988249700; b_lsid=67D4B3AE_183A317D8D8; innersign=1; CURRENT_FNVAL=4048; PVID=5",
"origin": "https://www.bilibili.com",
"referer": "https://www.bilibili.com/video/BV1Dg411678M/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=305425bcd5d36a142296a40e931d6f00",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53",
}
url = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=808284217&date=2022-10-03'
# req = request.Request(url = url,headers = headers)
# data  = request.urlopen(req).read()
temp=requests.get(url,headers=headers).content.decode("utf-8","ignore")
print(temp)
# with open("./弹幕.txt","w",encoding="utf-8") as f:
#     f.write(data)
