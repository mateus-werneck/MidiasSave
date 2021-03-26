import requests, re, time, urllib, os, webbrowser, json
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from moviepy.editor import VideoFileClip, concatenate_videoclips
from natsort import natsorted


firefox_options = Options()
firefox_options.add_argument("--headless")
firefox = webdriver.Firefox(options=firefox_options)
decoded = []

def getMedia(url, formato, response, media):
    global decoded

    if (media.group(0) == 'https://www.instagram.com/p'):
        firefox.get(url)
        time.sleep(1)
        html = firefox.page_source
        time.sleep(1)
        encodedImg = re.search(r'"display_url":"(.*?)",', html)
        encodedVideo = re.search(r'"video_url":"(.*?)",', html)
        if (encodedImg == None and encodedVideo == None):
            exit()
        else:
            if (encodedVideo == None):
                decoded.append(encodedImg.group(1).replace(r"\u0026", "&"))
            else:
                decoded.append(encodedVideo.group(1).replace(r"\u0026", "&"))
            for url in decoded:
                if (url != ''):
                    size = len(decoded) - 1
                    if (response == 'Computador'):
                        if (formato == '.jpg'):
                            name = 'instagram' + '0' + str(size) + formato
                            for i in range(100):
                                if (os.path.isfile(directory + '/' + 'instagram' + '0' + str(i) + '.jpg') == True):
                                    count += 1
                                    name = 'instagram' + '0' + str(count) + '.jpg'
                                else:
                                    break
                            urllib.request.urlretrieve(decoded[size], name)
                            return True
                        elif(formato == '.mp4'):
                            name = 'instagram' + '0' + str(size) + formato
                            for i in range(100):
                                if (os.path.isfile(directory + '/' + 'instagram' + '0' + str(i) + '.mp4') == True):
                                    count += 1
                                    name = 'instagram' + '0' + str(count) + '.mp4'
                                else:
                                    break
                            urllib.request.urlretrieve(decoded[size], name)
                            return True
                        elif(response == 'Navegador'):
                            webbrowser.open(url)
                            return True

                        else:
                            exit()
                else:
                    exit()

    elif(media.group(0) == 'https://www.instagram.com/stories'):
        firefox.get(url)
        time.sleep(2)
        view = firefox.find_element_by_class_name('sqdOP.L3NKy.y1rQx.cB_4K ')
        view.click()
        time.sleep(1)
        if (response == 'Computador'):
            if (formato == ' .jpg'):
                decoded.append(firefox.find_element_by_tag_name("img").get_attribute("src"))
                size = len(decoded) - 1
                name = 'instagram' + '0' + str(size) + formato
                for i in range(100):
                    if (os.path.isfile(directory + '/' + 'instagram' + '0' + str(i) + '.jpg') == True):
                        count += 1
                        name = 'instagram' + '0' + str(count) + '.jpg'
                    else:
                        break
                urllib.request.urlretrieve(decoded[size], name)
                return True
            elif(formato == ' .mp4'):
                decoded.append(firefox.find_element_by_tag_name('source').get_attribute("src"))
                size = len(decoded) - 1
                name = 'instagram' + '0' + str(size) + formato
                for i in range(100):
                    if (os.path.isfile(directory + '/' + 'instagram' + '0' + str(i) + '.mp4') == True):
                        count += 1
                        name = 'instagram' + '0' + str(count) + '.mp4'
                    else:
                        break
                urllib.request.urlretrieve(decoded[size], name)
                return True

        elif(response == 'Navegador'):
            if (formato == ' .jpg'):
                file = firefox.find_element_by_tag_name("img").get_attribute("src")
            elif(formato == ' .mp4'):
                file = firefox.find_element_by_tag_name('source').get_attribute("src")
            webbrowser.open(file)

            return True


    elif(media.group(0) == 'https://twitter.com/'):
        if (response == 'Computador'):
            if (formato == '.jpg'):
                firefox.get(url)
                time.sleep(4)
                media = firefox.find_elements_by_css_selector('img.css-9pa8cd[alt="Image"]')
                for pbs in media:
                    decoded.append(pbs.get_attribute("src"))
                    size = len(decoded) - 1
                    name = 'twitter' + '0' + str(size) + formato
                    count = 0
                    for i in range(100):
                        if (os.path.isfile(directory + '/' + 'twitter' + '0' + str(i) + '.jpg') == True):
                            count += 1
                            name = 'twitter' + '0' + str(count) + '.jpg'
                        else:
                            break
                    urllib.request.urlretrieve(decoded[size], name)
                    return True

            elif(formato == 'gif'):
                firefox.get(url)
                time.sleep(4)
                decoded.append(firefox.find_element_by_tag_name('video').get_attribute("src"))
                size = len(decoded) - 1
                name = 'twitter' + '0' + str(size) + ' .mp4'
                if (decoded[size] != ''):
                    count = 0
                    for i in range(100):
                        if (os.path.isfile(directory + '/' + 'twitter' + '0' + str(i) + '.mp4') == True):
                            count += 1
                            name = 'twitter' + '0' + str(count) + '.mp4'
                        else:
                            break
                    urllib.request.urlretrieve(decoded[size], name)
                    return True

            elif(formato == '.mp4'):
                firefox.get(url)
                time.sleep(10)
                log = firefox.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")
                video =''
                with open("items.json", "w") as jsonFile:
                    json.dump(log, jsonFile, indent = 6)
                jsonFile.close()
                with open ("items.json", "r") as jsonFile:
                    json_decoded = json.load(jsonFile)
                    for i in range(len(json_decoded)):
                        if (re.match('https://video.twimg.com/', json_decoded[i]['name']) != None):
                            video = json_decoded[i]['name']
                            break
                jsonFile.close()
                m3u8c = re.search('https://video.twimg.com(.*?)?tag=', video)
                encoded = []
                if (m3u8c == None):
                    urllib.request.urlretrieve(video, 'temp.txt')
                    with open ("temp.txt", "r") as temp:
                        for line in temp:
                            if(re.search(r'.ts', line) != None):
                                encoded.append('https://video.twimg.com' + line)
                            continue
                    temp.close()
                    directory = os.getcwd()
                    collection =[]
                    for i in range(len(encoded)):
                        name ='temp' + '0' + str(i) + ' .ts'
                        urllib.request.urlretrieve(encoded[i], name)
                        video = VideoFileClip(directory + '/' + name)
                        collection.append(video)
                    twitter = concatenate_videoclips(collection)
                    size = len(decoded)
                    name = 'twitter' + '0' + str(size) + '.mp4'
                    count = 0
                    for i in range(100):
                        if (os.path.isfile(directory + '/' + 'twitter' + '0' + str(i) + '.mp4') == True):
                            count += 1
                            name = 'twitter' + '0' + str(count) + '.mp4'
                        else:
                            break
                    twitter.to_videofile(name)
                    for i in range(len(encoded)):
                        os.remove(directory + '/temp' + '0' + str(i) + ' .ts')
                    os.remove(directory + '/temp.txt')
                    os.remove(directory + '/items.json')
                    decoded.append('twittervideo')
                    return True

                elif (m3u8c != None):
                    urllib.request.urlretrieve(video, 'temp.txt')
                    with open ("temp.txt", "r") as temp:
                        for line in temp:
                            if(re.search(r'.m3u8', line) != None):
                                m3u8c2 = 'https://video.twimg.com' + line
                            continue
                    temp.close()
                    urllib.request.urlretrieve(m3u8c2, 'temp.txt')
                    with open ("temp.txt", "r") as temp:
                        for line in temp:
                            if(re.search(r'.ts', line) != None):
                                encoded.append('https://video.twimg.com' + line)
                            continue
                    temp.close()
                    directory = os.getcwd()
                    collection =[]
                    for i in range(len(encoded)):
                        name ='temp' + '0' + str(i) + ' .ts'
                        urllib.request.urlretrieve(encoded[i], name)
                        video = VideoFileClip(directory + '/' + name)
                        collection.append(video)
                    twitter = concatenate_videoclips(collection)
                    size = len(decoded)
                    name = 'twitter' + '0' + str(size) + '.mp4'
                    count = 0
                    for i in range(100):
                        if (os.path.isfile(directory + '/' + 'twitter' + '0' + str(i) + '.mp4') == True):
                            count += 1
                            name = 'twitter' + '0' + str(count) + '.mp4'
                        else:
                            break
                    twitter.to_videofile(name)
                    for i in range(len(encoded)):
                        os.remove(directory + '/temp' + '0' + str(i) + ' .ts')
                    os.remove(directory + '/temp.txt')
                    os.remove(directory + '/items.json')
                    decoded.append('twittervideo')
                    return True

        elif(response == 'Navegador'):
            if (formato == '.jpg'):
                firefox.get(url)
                time.sleep(5)
                decoded = firefox.find_element_by_css_selector('img.css-9pa8cd').get_attribute("src")
                if (decoded != ''):
                    webbrowser.open(decoded)
                    return True
            elif(formato == 'gif'):
                firefox.get(url)
                time.sleep(5)
                decoded = firefox.find_element_by_tag_name('video').get_attribute("src")
                if (decoded != ''):
                    webbrowser.open(decoded)
                    return True
                else:
                    firefox.quit()
                    return 0

    else:
        firefox.quit()
        return 0

def auth(button):
    if (button == 0):
        username = 'pythonauthusr1234'
        password = 'instagramauthpass123'
        firefox.get("https://www.instagram.com/accounts/login/")
        time.sleep(1)
        usern = firefox.find_element_by_name("username")
        usern.send_keys(username)
        passw = firefox.find_element_by_name("password")
        passw.send_keys(password)
        time.sleep(1)
        log_cl = firefox.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
        log_cl.click()
        time.sleep(4)
        title = firefox.title
        if (title == "Login • Instagram"):
            time.sleep(1)
            username = 'pythonauthusr12345'
            usern = firefox.find_element_by_name("username")
            usern.send_keys(username)
            passw = firefox.find_element_by_name("password")
            passw.send_keys(password)
            time.sleep(1)
            log_cl = firefox.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
            log_cl.click()
            time.sleep(4)
            title = firefox.title
            if (title == "Login • Instagram"):
                firefox.quit()
                return 0
            else:
                return True

        else:
            return True
    elif(button > 0):
        return True

def killFirefox():
    firefox.close()
    firefox.quit()
    return 0
