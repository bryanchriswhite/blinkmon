#!/usr/bin/env python3

import re
import requests
import semver

DOCKERHUB_STORAGENODE_IMAGES_URL = 'https://hub.docker.com/v2/repositories/storjlabs/storagenode/tags' #?page_size=50&page=1

def supports_arm_v5(image):
    for _image in image['images']:
        if _image['architecture'] == 'arm' and _image['variant'] == 'v5':
            return True
    return False
    

def get_page(page_num, page_size):
    return requests.get(
        DOCKERHUB_STORAGENODE_IMAGES_URL,
        params={
                'page': page_num,
                'page_size': page_size,
            }
    ).json()

def get_images():
    return parse_page(get_page(1, 350))

def parse_page(page):
    return [image for image in page['results'] if supports_arm_v5(image)]

#def should_update(rollout_cursor):


if __name__ == "__main__":
    images = get_images()
    #print(images)
    for image in images:
        if re.match("\w{,9}-v\d+\.", image['name']) is not None:
            print(image['name'])
        #for subimage in image['images']:
            #print(subimage)
            #print(subimage['architecture'] == 'arm' and subimage['variant'] == 'v5')
        #print('--')

    #try:
    #    stats = requests.get('http://localhost:14002/api/sno').json()
    #    current_version = stats['version']

    #    versions = requests.get('https://version.storj.io')
    #    cursor = versions.json()['processes']['storagenode']['rollout']['cursor']
    #    int_cursor = int(cursor, 10)
    #    dec_cursor = int(cursor, 16)
    #    print(f'hex cursor: {int_cursor}\nlength: {len(str(int_cursor))}')
    #    print(f'dec cursor: {dec_cursor}\nlength: {len(str(dec_cursor))}')
    #    max32B = 2**((8*32)-1)
    #    print(f'max 32B: {max32B}\nlength: {len(str(max32B))}')

    #    #new_version, 
    #    #if should_update():
    #except requests.exceptions.ConnectionError as e:
    #    print(e)
    #    pass
        

