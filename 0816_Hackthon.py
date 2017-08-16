
# coding: utf-8

# In[1]:


import requests
import os
import json
import time
from bs4 import BeautifulSoup
import telepot
from telepot.loop import MessageLoop
from watson_developer_cloud import VisualRecognitionV3


# In[2]:


def get_img(msg):
    url = msg["text"][8:]
    if url[:4] != "http":
        url = "http://" + url
    
    raw = requests.get(url)
    soup = BeautifulSoup(raw.text, "html.parser")

    data = soup.find_all("img")
    cnt = 0
    for d in data:
        if cnt == 100:
            break
    
        imgUrl = str(d.get("src"))
        if imgUrl[:2] == "//":
            imgUrl = "http:" + imgUrl
        elif imgUrl[:4] != "http":
            imgUrl = url + imgUrl
        
        imgNow = requests.get(imgUrl)
        imgType = imgUrl.split('.')[-1]
    
        if imgType == "jpg" or imgType == "png" or imgType == "bmp":
            rawJson = vr.classify(images_url = imgUrl)
            imgClass = rawJson["images"][0]["classifiers"][0]["classes"][0]["class"]
            imgName = imgUrl.split('/')[-1]
        
            if os.path.exists(imgClass) == False:
                print("__New dir: " + imgClass)
                os.system("mkdir \"" + imgClass + '\"')
            
            with open(imgClass + '/' + imgName, "wb") as img:
                print(imgName, end = "......")
                img.write(imgNow.content)
                print("done!")
            cnt += 1
    bot.sendMessage(msg["chat"]["id"], "All process(es) done!")
    print("All process(es) done!")
'''
    data = soup.find_all("a")
    for d in data:
        if cnt == 100:
            break
    
        now = str(d.get("href"))
        if now[:2] == "//":
            now = "http:" + now
        elif now[:4] != "http":
            now = url + now
        
        imgUrl = requests.get(now)
        imgType = now.split('.')[-1]
    
        if imgType == "jpg" or imgType == "png" or imgType == "bmp" or imgType == "gif":
            imgName = now.split('/')[-1]
            with open(imgName, "wb") as img:
                print(imgName, end = "......")
                img.write(imgUrl.content)
                print("done!")
            cnt += 1
'''
    
    
def on_chat(msg):
    print(json.dumps(msg, indent=4))
    
    if msg["text"][0] == '/':
        if msg["text"] == "/start":
            bot.sendMessage(msg["chat"]["id"], "Hello, " + msg["chat"]["first_name"] + ", I'm PicDownloader. By just giving me the url of the website, I can give you all the pictures on it. Type: /DLimgs <url>\n(Note: The success rate is NOT 100%. You may recieve no pictures.)")
        elif msg["text"][:7] == "/DLimgs" and len(msg["text"]) > 8:
            get_img(msg)
        elif msg["text"][:8] == "/GETimgs":
            if len(msg["text"]) == 8:
                toSend = ""
                for dirPath, dirNames, fileNames in os.walk("."):
                    for f in dirNames:
                        imgType = f[-3:]
                        if f[0] != '.':
                            toSend += f + '\n'
                bot.sendMessage(msg["chat"]["id"], toSend)
            else:
                imgClass = msg["text"][9:]
                if os.path.exists(imgClass):
                    for dirPath, dirNames, fileNames in os.walk(imgClass):
                        for f in fileNames:
                            with open(imgClass + '/' + f, "rb") as imgToSend:
                                bot.sendPhoto(msg["chat"]["id"], imgToSend)
                else:
                    bot.sendMessage(msg["chat"]["id"], "Directory " + imgClass + " not exsist!")
    else:
        bot.sendMessage(msg["chat"]["id"], "Yeee")


# In[3]:


# API setting
apiKey = "5cdbc86bce65513f6323f510042ae0d008f95d61"
version = time.strftime("%F")
vr = VisualRecognitionV3(version, api_key = apiKey)

TOKEN = "361996215:AAGenvAYaQ0AK5WTQhPIqHesdXNxt8GNe9E"
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {
    'chat': on_chat,
}).run_as_thread()

print('Listening ...')


# In[ ]:





# In[ ]:





# In[ ]:




