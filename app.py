# -*- coding: utf-8 -*-

from requests import get
from bs4 import BeautifulSoup
from re import match
from os.path import join, expanduser, exists
from os import mkdir

default_url = "https://alpha.wallhaven.cc/search?q=&search_image=&categories=100&purity=100&resolutions=1920x1080&sorting=random&order=desc&page={}" 

save_folder = expanduser("~\\Pictures\\Wallpaper")
if not exists:
    print("Creating folder: {}".format(save_folder))
    mkdir(save_folder)


def extract(url, element, attribute):
    print ("Downloading '{}' ....".format(url))
    html = get(url)
    print("Parsing '{}'....".format(url))
    bs = BeautifulSoup(html.text)
    for el_a in bs.find_all(element):
        if el_a.has_attr(attribute):
            yield el_a[attribute]

def download(image_src):
    print("Found {}".format(image_src))
    save_path = join(save_folder, image_src.split("/")[-1])
    print("Saving image into {}".format(save_path))

    content = get("https:{}".format(image_src)).content
    
    with open(save_path, "ab") as img:
        img.write(content)

def start():    
    for pageNumber in range(1, 5):
        url = default_url.format(pageNumber)
        for extracted_url in extract(url, "a", "href"):   
            if match(".*/wallpaper/.*", extracted_url):
                images = extract(extracted_url, "img", "src")
                for image_src in images:
                    if match(".*/wallpapers/full/.*", image_src):
                        download(image_src)  
                        
if __name__ == '__main__':
    start()