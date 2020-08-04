import os
import urllib
import requests
import m3u8
import time
import json

current_milli_time = lambda: int(round(time.time() * 1000))
def DownloadLineTV(dramaID, episodeID, **kwargs):
    web_link = 'https://www.linetv.tw/api/part/{dramaID}/eps/{episodeID}/part/'.format(dramaID=dramaID, episodeID=episodeID)
    video_info = json.loads(requests.get(web_link).content)
    m3u8_link = kwargs['m3u8_link'] or video_info['epsInfo']['source'][0]['links'][0]['link']
    m3u8_link = m3u8_link.split('_',1)[0]+'_FHD.m3u8'
    # Getting key for video
    get_token_data = {'keyId': video_info['epsInfo']['source'][0]['links'][0]['keyId'], 'keyType': video_info['epsInfo']['source'][0]['links'][0]['keyType']}
    video_key_token = json.loads(requests.post('https://www.linetv.tw/api/part/dinosaurKeeper', data=get_token_data).content)


    # LOCATING FILES
    base_path = os.path.dirname(m3u8_link) + '/'
    response = requests.get(m3u8_link)
    m3u8_obj = m3u8.loads(response.content.decode('UTF-8'))

    # WORKING ON SUBTITLES
    subtitle_obj = next(item for item in m3u8_obj.media if item.type == "SUBTITLES")
    subtitle_base_path = urllib.parse.urljoin(base_path, subtitle_obj.uri)
    subtitle_response = requests.get(subtitle_base_path)
    subtitle_base_path = os.path.dirname(subtitle_base_path) + '/'
    subtitle_obj = m3u8.loads(subtitle_response.content.decode('UTF-8'))
    subtitle_obj.base_path = subtitle_base_path[:-1]
    subtitle_response = requests.get(subtitle_obj.segments.uri[0])


    # WORKING ON VIDEOS AND KEYS
    video_obj = m3u8_obj.playlists[-1]
    video_obj.base_uri = base_path
    video_base_path = video_obj.absolute_uri
    video_response = requests.get(video_base_path)
    video_base_path = os.path.dirname(video_base_path) + '/'
    video_obj = m3u8.loads(video_response.content.decode('UTF-8'))
    params = {'time': current_milli_time()}
    key_content = requests.get(video_obj.keys[0].uri, headers={'Authorization': video_key_token["token"]}, params=params).content
    video_obj.base_path = video_base_path[:-1]
    video_paths = set(video_obj.segments.uri)
    video_paths = list(video_paths)
    #print(video_paths)
    # SAVE DOWNLOAD FILM LINK, KEY AND SUBTITLE
    with open('videos_to_be_download.txt', 'a+') as handle:
        for video_path in video_paths:
            handle.write(video_path + '\n')
    with open(os.path.join('decrypted', os.path.splitext(os.path.basename(video_paths[0]))[0] + '.vtt'), 'wb+') as handle:
        handle.write(subtitle_response.content)
    with open(os.path.splitext(os.path.basename(video_paths[0]))[0] + '.key', 'wb+') as handle:
        handle.write(key_content)
    # for video_path in video_paths:
    #     video_content = requests.get(video_path)
    #     with open(os.path.basename(video_path), 'wb+') as handle:
    #         handle.write(video_content)


if not os.path.exists('decrypted'):
    os.makedirs('decrypted')


# CHANGE HERE
dramaID = 10738
#for k in range(4,31):
#    DownloadLineTV(dramaID,k)
DownloadLineTV(dramaID,3, m3u8_link='https://d3c7rimkq79yfu.cloudfront.net/10738/3/v3/10738-eps-3_FHD.m3u8')