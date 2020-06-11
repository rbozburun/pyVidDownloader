from pytube import YouTube
import os
from bs4 import BeautifulSoup
from time import sleep
import requests

#  <Stream: itag="22" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">,
# https://www.hocalarageldik.com/ders/konu-anlatimi/9406

def main():
    request_func()

def request_func():
    print("Sistem başlatılıyor...")
    url = 'https://www.hocalarageldik.com/ders/konu-anlatimi/8851'
    page_req = requests.get(url)
    status = str(page_req.status_code)
    print("Statü: "+ status)

    if(status == str(200)):
        print("Bağlantı Sağlandı... Parçalama başlıyor")
        parse_html(page_req)
    else:
        print("Bağlantı sağlanamadı")

def parse_html(req):
    soup = BeautifulSoup(req.text, "html.parser")
    videoKategorileri = soup.find_all('div',class_='category-wrapper')
    href_list =  []

    for kategori in videoKategorileri:
        category_item = kategori.find_all('div',class_='category-item')
        for item in category_item:
            konular = item.find_all('a',class_='list-title')
            for konu in konular:
                href = konu.get('href')
                href_list.append(href)
    createLinks(href_list)

def createLinks(list):
    links = []
    for href in list:
        link = "https://www.hocalarageldik.com" + href
        links.append(link)

    createYoutueLinks(links)

def createYoutueLinks(list):
    yt = "https://www.youtube.com/watch?v="
    youtubeLinks = []

    for url in list:
        page_req = requests.get(url)
        status = str(page_req.status_code)
        print("Video Sayfası Statü: " + status)

        if (status == str(200)):
            print("Video sayfasına bağlandı... Parçalama başlıyor")
            videoKey = parse_htmlof_VideoURL(page_req)
            youtubeLink = yt+videoKey
            youtubeLinks.append(youtubeLink)

        else:
            print(" Video Sayfasına Bağlantı sağlanamadı")

    download(youtubeLinks)

def download(youtubeLinks):
    c = 1
    for link in youtubeLinks:
        video = YouTube(link)
        video.streams.get_by_itag(22).download()
        newFileName = "{}_".format(c) + video.streams.first().default_filename
        os.rename(video.streams.first().default_filename, newFileName)
        print('{}. video indirildi'.format(c))
        c = c+1

def parse_htmlof_VideoURL(req):
    soup = BeautifulSoup(req.text, "html.parser")
    videoBox = soup.find('div',class_='shadow')
    video = videoBox.find('iframe')
    videoLink = video.get('src')

    videoKey = videoLink[30:-17]
    return videoKey

main()




