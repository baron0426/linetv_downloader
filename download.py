import os
import urllib
import requests
import m3u8

m3u8_link = 'https://gamer-cds.cdn.hinet.net/vod_gamer/_definst_/smil:gamer2/093488c70ee0dbbdc6e1b2add5b63f5c6bc957f0/hls-s-ae-2s.smil/chunklist_b600000.m3u8?token=dCNof3rEa6ZvPndxS-FNfw&expires=1596438387&bahaData=02cc534c6dd4c7d2515923f8660b6f8a2deab9387bd4f9655f27793e0706%3A10618%3A0%3APC%3Aa533e'
base_video_path = os.path.dirname(m3u8_link)
m3u8_link_parse = urllib.parse.urlparse(m3u8_link)
essential_query = urllib.parse.parse_qs(m3u8_link_parse.query)

custom_header = {'origin': 'https://ani.gamer.com.tw'}
response = requests.get(m3u8_link, headers=custom_header)
m3u8_obj = m3u8.loads(response.content.decode('UTF-8'))
m3u8_key = requests.get(m3u8_obj.keys[0].uri, headers=custom_header).content
with open('key.key', 'wb') as handle:
    handle.write(m3u8_key)

# print(m3u8_obj.segments.uri)
for ts_part_path in m3u8_obj.segments.uri:
    ts_content = requests.get(base_video_path + '/' + ts_part_path, params=essential_query, headers=custom_header).content
    ts_file_basename = urllib.parse.urlparse(ts_part_path).path
    with open(ts_file_basename, 'wb') as handle:
        handle.write(ts_content)

# origin = os.path.join("response.ts")
#
