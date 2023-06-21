#! /usr/bin/env python3.11

import os
import openai
import requests
import shutil
import glob

openai.api_key = "YOUR KEY HERE"

def check_if_exists():
    folders = glob.glob("./*")
    if "./dalle-gens" not in folders:
        os.mkdir("./dalle-gens")
    else:
        print("[OK] DALL-E output folder.")

check_if_exists()

BASE_PATH = os.path.join("../", "dalle-gens")
IMAGE_EXT = ".png"

IMAGE_WIDTH = "512"

def list_images_in_path():
    pngs = glob.glob(BASE_PATH+'*.png')
    for i in range(len(pngs)):
        print(f"{i} - "+pngs[i].split('/')[-1])
    return pngs

def pick_images_in_path():
    pngs = list_images_in_path()
    selection = input("select the image from above options...\n")
    try: 
        return pngs[int(selection)]
    except:
        print("invalid selection")
        exit(0)

def create_image(prompt, n=1, size=IMAGE_WIDTH):
    if prompt == "":
        print("need a prompt")
        exit(0)
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size+"x"+size
    )
    url = response['data'][0]['url']
    return url

def variate_existing_image_from_path(img_path, n=1, size=IMAGE_WIDTH):
    try:
        IMAGE_SIZE = os.path.getsize(img_path)/1e6 # in MB
        if IMAGE_SIZE > 4:
            print("file too large, must be less than 4MB")
            exit(0)
        response = openai.Image.create_variation(
            image = open(img_path, "rb"),
            n=n,
            size=size+"x"+size
        )
        url = response['data'][0]['url']
        return url
    except:
        print('error')
        exit(0)
    
def save_generated_image_from_url_with_name(url,name):
    res = requests.get(url, stream=True)
    SAVE_PATH = BASE_PATH+"/"+name+IMAGE_EXT
    with open(SAVE_PATH, "wb") as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)
    return SAVE_PATH
