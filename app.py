# -*- coding: utf-8 -*-

from multiprocessing import Pool
from requests import get
from bs4 import BeautifulSoup
from re import match
from os.path import join, expanduser, exists
from os import makedirs

default_url = "https://alpha.wallhaven.cc/search?q=&search_image=&categories=100&purity=100&resolutions=1920x1080&sorting=random&order=desc&page={}" 

def get_folder():
    folder = None
    while True:
        folder = input("Onde eu salvo estas imagens?: ")
        if folder:
            break;
    
    save_folder = expanduser(folder.strip())
    print("Salvando imagens em: {}".format(save_folder))
    if not exists(save_folder):
        print("Criando pasta: {}".format(save_folder))
        makedirs(save_folder)

    return save_folder 


def extract(url, element, attribute):
    print ("Baixando '{}' ....".format(url))
    html = get(url)
    print("Convertendo '{}'....".format(url))
    bs = BeautifulSoup(html.text, 'html.parser')
    for el_a in bs.find_all(element):
        if el_a.has_attr(attribute):
            yield el_a[attribute]

def download(image_src, save_folder):
    print("Encontrado {}".format(image_src))
    save_path = join(save_folder, image_src.split("/")[-1])
    print("Salvando imagens no caminho: {}".format(save_path))

    content = get("https:{}".format(image_src)).content
    
    with open(save_path, "ab") as img:
        img.write(content)

def _download_image(image_src):
    if match(".*/wallpapers/full/.*", image_src):
        download(image_src, save_path)  

def start():    
    global save_path
    save_path = get_folder()
    for pageNumber in range(1, 5):
        url = default_url.format(pageNumber)
        for extracted_url in extract(url, "a", "href"):   
            if match(".*/wallpaper/.*", extracted_url):
                images = extract(extracted_url, "img", "src")
                #for image_src in images:
                with Pool(20) as p:
                    p.map(_download_image, images) 
                        
if __name__ == '__main__':
    start()
