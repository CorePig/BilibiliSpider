import pprint

import requests
import re
import json
import subprocess
headers = {
             'referer': 'https://www.bilibili.com/video/BV1N5411Q75n?spm_id_from=333.1007.extension.content.click',
             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
           }
html=requests.get('https://www.bilibili.com/video/BV1N5411Q75n?spm_id_from=333.1007.extension.content.click').content.decode('utf-8')
try:
    ans=json.loads(re.findall('<script>window.__playinfo__=(.*?)</script>',html)[0])
    # pprint.pprint(ans)
    audio_url=ans['data']['dash']['audio'][0]['baseUrl']
    video_url=ans['data']['dash']['video'][0]['base_url']
    # print(audio_url)
    # print(video_url)
    audio=requests.get(audio_url,headers=headers).content
    video=requests.get(video_url,headers=headers).content
    with open("声音.mp3","wb") as f1:
        f1.write(audio)
    with open("视频.mp4","wb") as f2:
        f2.write(video)
    comend = f'D:/apache-tomcat-9.0.53-windows-x64/ffpmeg/ffpmeg/bin/win64/ffmpeg.exe -i 视频.mp4 -i 声音.mp3 -c:v copy -c:a aac -strict experimental output.mp4'
    subprocess.run(comend)
except Exception as e:
    print("json出错")
