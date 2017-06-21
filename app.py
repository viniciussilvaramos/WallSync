# -*- coding: utf-8 -*-

from requests import get
from bs4 import BeautifulSoup
from re import match
from os.path import join

urls = [
    "https://alpha.wallhaven.cc/search?q=&search_image=&categories=100&purity=100&sorting=random&order=desc&page=1",
    "https://alpha.wallhaven.cc/search?q=&search_image=&categories=100&purity=100&sorting=random&order=desc&page=2",
    "https://alpha.wallhaven.cc/search?q=&search_image=&categories=100&purity=100&sorting=random&order=desc&page=3",
    "https://alpha.wallhaven.cc/search?q=&search_image=&categories=100&purity=100&sorting=random&order=desc&page=4",
    "https://alpha.wallhaven.cc/search?q=&search_image=&categories=100&purity=100&sorting=random&order=desc&page=5",
]

save_folder = "C:\\Users\\one\\Pictures\\wallpapers"

def extract(url, element, attribute):
    print ("Downloading '{}' ....".format(url))
    html = get(url)
    print("Parsing '{}'....".format(url))
    bs = BeautifulSoup(html.text, 'lxml')
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
    for url in urls:
        for extracted_url in extract(url, "a", "href"):   
            if match(".*/wallpaper/.*", extracted_url):
                images = extract(extracted_url, "img", "src")
                for image_src in images:
                    if match(".*/wallpapers/full/.*", image_src):
                        download(image_src)  
                        


if __name__ == '__main__':
    start()