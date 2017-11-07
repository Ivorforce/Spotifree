import requests
import urllib
from lxml import html
from cssselect import GenericTranslator

def try_tracks(tracks, write_out=lambda x: None):
    searched = 0

    for track in tracks:
        query = "https://soundcloud.com/search?q=" + urllib.parse.quote(track, safe='')
        request = requests.get(query)

        tree = html.fromstring(request.text)
        elements = tree.xpath(GenericTranslator().css_to_xpath('ul>li>h2>a'))

        if len(elements) == 0:
            continue

        href = elements[0].get('href')

        track_url = "https://soundcloud.com" + href
        song_html = requests.get(track_url).text
        song_title = html.fromstring(song_html).findtext(".//title")

        if "\"purchase_title\":\"Free Download" in song_html or "\"purchase_title\":\"Free DL" in song_html\
                or "Free Download" in song_title or "Free DL" in song_title:
            track_info = "%s (%s)" % (track, track_url)
            print(track_info)
            write_out(track_info + "\n")

        searched += 1
        if searched % 20 == 0:
            print("Searched %d tracks" % searched)

