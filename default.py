import sys
import xbmcgui   # deprecated
import xbmcplugin   # deprecated
from addon.common.addon import Addon   # provided by: script.module.addon.common
from addon.common.net import Net   # provided by: script.module.addon.common
from bs4 import BeautifulSoup   # provided by: script.module.beautifulsoup4
from urllib import quote_plus, unquote_plus   # provided by: script.module.urlresolver
import json   # provided by: script.module.somplejson
from xbmc import Player

addon = Addon('plugin.video.skeledrew.anime-watcher', argv=sys.argv)
net = Net()
kodi_player = Player()

addon_handle = addon.handle
ueError = '<<UnicodeEncodeError encountered in text>>'

#xbmcplugin.setContent(addon_handle, 'movies')

def test_area():
    url = 'http://localhost/some_video.mkv'
    li = xbmcgui.ListItem('My First Video!', iconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    stat = ""

    if addon:
        stat = "Import successful!"
    else:
        stat = "Import failed..."
    li = xbmcgui.ListItem(stat, iconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    addon.add_directory({'folder': 'fldr3'}, {'title': 'Folder #3'})
    addon.add_directory({'folder': 'fldr4'}, {'title': str(len(addon.queries))})
    addon.add_directory({'folder': 'fldr4'}, {'title': 'Did something go wrong?'})

    #xbmcplugin.endOfDirectory(addon_handle)
    addon.end_of_directory()

def uni_kill(char):
    # replace unicode characters
    
    if ord(char) > 127:
        return 'u[' + str(ord(char)) + ']'
    return char

def fix_uni(word):
    n_word = ''
    
    if not word:
        return ''
    
    for char in word:
        uni_kill(char)
        n_word = n_word + char
    return n_word

def get_json(url, src):
    # TODO: should probably do some error checking...
    headers = {}
    
    if src == 'aplus':
        # code from animego
        headers['User-Agent'] = 'okhttp/2.3.0'
        headers['Host']='api.animeplus.tv'
        headers['App-LandingPage']='http://www.mobi24.net/anime.html'
        headers['App-Name']='#Animania'
        headers['App-Version']='7.5'
        headers['Accept-Encoding'] = 'gzip'
        headers['Connection'] = 'keep-alive'
    return json.loads(net.http_GET(url, headers=headers).content.encode('UTF-8'))

class main:
    def __init__(self):
        
        if len(addon.queries) == 1 and addon.queries['mode'] == 'main':
            # default query
            dirs().root()
        
        if 'dir' in addon.queries:
            # navigate static local dirs
            target_dir = addon.queries['dir']
            
            if target_dir == 'lib':
                dirs().lib()
                
            if target_dir == 'aplus':
                dirs().aplus()
            
            if target_dir == 'ctun':
                dirs().ctun()
            return
        
        if 'list' in addon.queries and 'src' in addon.queries and addon.queries['src'] == 'aplus':
            # navigate dynamic site lists
            target_list = addon.queries['list']
            
            if target_list == 'index':
                lists().aplus_series_api()
                
            if target_list == 'pop':
                lists().aplus_series_api({'scope': 'Popular'})
                
            if target_list == 'new':
                lists().aplus_series_api({'scope': 'New'})
                
            #if target_list == 'recent':
                
            if target_list == 'ongoing':
                lists().aplus_series_api({'status': 'ONG'})
                
            if target_list == 'complete':
                lists().aplus_series_api({'status': 'CMP'})
                
            if target_list == 'genres':
                lists().aplus_series_api({'genres': []})
                
            if target_list == 'genre':
                lists().aplus_series_api({'genre': addon.queries['genre']})
            
            if target_list == 'recepi':
                lists().aplus_rec_epi_web()
                
            if target_list == 'recent':
                lists().aplus_rec_ser_web()
                
            if target_list == 'episodes':
                lists().aplus_episodes_api(addon.queries['seriesid'], addon.queries['name'])
                
            if target_list == 'sources':
                lists().aplus_sources_api(addon.queries['episodeid'], addon.queries['name'])
        
            if target_list == 'mplay':
                # NB: untested code; not triggered thus far by any sources
                links = addon.queries['urls'].split('|')
                total_links = len(links)-1
                loaded_links = 0
                play_list = addon.get_video_playlist(new=True)
                prog_dlg = xbmcgui.DialogProgress()
                prog_dlg.create('Loading playlist...')
                remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
                prog_dlg.update(0,'Please wait for the process to retrieve the video links.',remaining_display)
                
                for link in links:
                    CreateList(link)
                    loaded_links = loaded_links + 1
                    percent = loaded_links / total_links * 100
                    remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
                    prog_dlg.update(percent,'Please wait for the process to retrieve video link.',remaining_display)
                    
                    if prog_dlg.iscanceled():
                        return False
                kodi_player.play(play_list)
                
                if not kodi_player.isPlayingVideo():
                    addon.show_ok_dialog(['One or more of the playlist items','Check links individually.'], 'VideoUrl: ' + str(play_list))
                return True
        
        if 'list' in addon.queries and 'src' in addon.queries and addon.queries['src'] == 'ctun':
            # navigate dynamic site lists
            target_list = addon.queries['list']
            
            if target_list == 'index':
                couchtuner().index()
                
            if target_list == 'episodes':
                couchtuner().episodes(addon.queries)
                
            if target_list == 'sources':
                sources().couchtuner(addon.queries['url'], addon.queries['name'])
        
        if 'list' in addon.queries and addon.queries['list'] == 'play':
                # TODO: Implement other play options later
                kodi_player.play(addon.queries['url'])
                
        addon.end_of_directory()
        return
            
class dirs:
    
    def root(self):
        addon.add_directory({'dir': 'lib'}, {'title': 'Library'})
        addon.add_directory({'dir': 'fav'}, {'title': 'My List'})
        addon.add_directory({'dir': 'cfg'}, {'title': 'Settings'})
        addon.end_of_directory()
        
    def lib(self):
        addon.add_directory({'dir': 'aplus'}, {'title': 'Anime'})
        #addon.add_directory({'dir': 'adub'}, {'title': 'Anime Dub'})
        #addon.add_directory({'dir': 'acrazy'}, {'title': 'Anime Crazy'})
        #addon.add_directory({'dir': 'ablog'}, {'title': 'Anime Blog'})
        #addon.add_directory({'dir': 'afreak'}, {'title': 'Anime Freak'})
        #addon.add_directory({'dir': 'afav'}, {'title': 'Anime Fav'})
        #addon.add_directory({'dir': 'cdub'}, {'title': 'Cartoon Dub'})
        addon.add_directory({'dir': 'ctun'}, {'title': 'TV Shows'})
        addon.end_of_directory()
        
    def aplus(self):
        addon.add_directory({'src': 'aplus', 'list': 'index'}, {'title': 'Index'})
        addon.add_directory({'src': 'aplus', 'list': 'pop'}, {'title': 'Popular'})
        addon.add_directory({'src': 'aplus', 'list': 'new'}, {'title': 'New'})
        #addon.add_directory({'src': 'aplus', 'list': 'recent'}, {'title': 'Recent'})
        addon.add_directory({'src': 'aplus', 'list': 'ongoing'}, {'title': 'Ongoing'})
        addon.add_directory({'src': 'aplus', 'list': 'complete'}, {'title': 'Completed'})
        addon.add_directory({'src': 'aplus', 'list': 'genres'}, {'title': 'Genres'})
        addon.add_directory({'src': 'aplus', 'list': 'recepi'}, {'title': 'Recent Releases'})
        addon.add_directory({'src': 'aplus', 'list': 'recent'}, {'title': 'Recently Added Series'})
        addon.end_of_directory()
    
    def ctun(self):
        addon.add_directory({'src': 'ctun', 'list': 'index'}, {'title': 'Index'})
        addon.add_directory({'src': 'ctun', 'list': 'recepi'}, {'title': 'Recent Releases'})
        addon.add_directory({'src': 'ctun', 'list': 'sched'}, {'title': 'TV Schedule'})
        addon.end_of_directory()
        
class lists:
    
    def aplus_rec_epi_web(self):
        resp = net.http_GET('http://www.animeplus.tv/')
        soup = BeautifulSoup(resp.content, 'html5lib')
        recent_releases = soup.find_all('div', id="rr")[0].find_all('a')
        series_collection = get_json('http://api.animeplus.tv/GetAllShows', 'aplus')
        
        for episode in recent_releases:
            epi_name = episode.string.encode('UTF-8')   # NB: this could break at anytime...
            
            if ' Episode ' in epi_name:
                series_name = epi_name.split(' Episode ')[0]
                epi_num = epi_name.split(' Episode ')[1]
                
            elif ' OVA ' in epi_name:
                series_name = epi_name.split(' OVA ')[0]
                epi_num = epi_name.split(' OVA ')[1]
                
            else:
                err_msg = 'Unhandled name format encountered: ' + epi_name
                addon.show_small_popup(msg=err_msg, title='See log for more')
                addon.log_error(err_msg)
                addon.add_directory({}, {'title': err_msg})   # place holder
                continue
                
            
            for series in series_collection:
                
                if series['name'] == series_name:
                    seriesid = series['id']
                    episodes = get_json('http://api.animeplus.tv/GetDetails/' + seriesid, 'aplus')['episode']
                    
                    for idx in range(len(episodes)-1, -1, -1):
                        # index backwards for speed and accuracy
                        
                        if epi_num in episodes[idx]['name']:
                            episode = episodes[idx]
                            addon.add_directory({'src': 'aplus', 'list': 'sources', 'name': episode['name'], 'episodeid': episode['id']}, {'title': episode['name']}, img='http://www.animeplus.tv/images/series/big/' + str(seriesid)+'.jpg')
                            
                        ''' NB: doesn't work properly
                        elif idx == 0 and not epi_num in episodes[idx]['name']:
                            # end of the list, didn't find a match
                            addon.add_directory({}, {'title': 'Error: unable to find ' + series_name + ' in the series collection'})'''   # place holder
                        
    
    def aplus_rec_ser_web(self):
        resp = net.http_GET('http://www.animeplus.tv/')
        soup = BeautifulSoup(resp.content, 'html5lib')
        recent_series = soup.find_all('div', id="rs")[0].find_all('a')
        series_collection = get_json('http://api.animeplus.tv/GetAllShows', 'aplus')
        
        for name in recent_series:
            
            try:
                series_name = name.string.encode('UTF-8')
                #print 'Series name is ' + str(series_name)
                
                for series in series_collection:
                    
                    if series['name'] == series_name:
                        addon.add_directory({'src': 'aplus', 'list': 'episodes', 'name': series['name'], 'seriesid': series['id']}, {'title': series['name'].encode('UTF-8'), 'plot': series['description']}, img='http://www.animeplus.tv/images/series/big/' + str(series["id"])+'.jpg')
                        
            except:
                err_msg = 'Unhandled error involving: ' + str(name)
                addon.show_small_popup(msg=err_msg, title='See log for more')
                addon.log_error(err_msg)
                addon.add_directory({}, {'title': err_msg})   # place holder
        
    '''
    def aplus_episodes(self, url):
        # NB: Anime info also present on this page
        resp = net.http_GET(unquote_plus(url))
        soup = BeautifulSoup(resp.content, 'html5lib')
        episodes = soup.find_all('div', id="videos")[0].find_all('a')
        #addon.show_ok_dialog(episodes)
        #addon.add_directory({'series': True, 'name': 'def', 'url': 'def'}, {'title': str(episodes)})
        
        for idx in range(len(episodes)-1, -1, -1):
            # sort ascending, might be moot
            episode = episodes[idx]
            name = fix_uni(episode.string)
            url = quote_plus(episode['href'])
            
            try:
                addon.add_directory({'list': 'sources', 'name': name, 'url': url}, {'title': name})
                
            except UnicodeEncodeError:
                addon.add_directory({'list': 'sources', 'name': url, 'url': url}, {'title': '<< ' + unquote_plus(url).split('tv/')[1] + ' >>'})
        addon.end_of_directory()
        
    def aplus_sources(self, url):
        resp = net.http_GET(unquote_plus(url))
        soup = BeautifulSoup(resp.content, 'html5lib')
        sources = soup.find_all('div', id="streams")[0].find_all('iframe')
        #addon.add_directory({'series': True, 'name': 'def', 'url': 'def'}, {'title': str(episodes)})
        
        for source in sources:
            resp = net.http_GET(source['src'])
        '''
    
    def aplus_series_api(self, filters={}):
        '''series_collection = get_json(url, 'aplus')
        
        if not status == '':
            new_coll = []
            
            for series in series_collection:
                
                if series['status'] == status:
                    new_coll.append(series)
            series_collection = new_coll
            print str(series_collection)'''
        
        ### NB: 'scope' must be All, Popular or New and 'mtype' must be Shows or Movies; weird things may happen otherwise
        if not 'scope' in filters:
            filters['scope'] = 'All'
            
        if not 'mtype' in filters:
            filters['mtype'] = 'Shows'
        url = 'http://api.animeplus.tv/Get' + filters['scope'] + filters['mtype']
        series_collection = get_json(url, 'aplus')
        
        for key in filters:
            
            if not (key == 'scope' or key == 'mtype'):
                filt = filters[key]
                
                new_coll = []
                
                if key == 'genres':
                    self.aplus_genres(series_collection)
                    return
                
                if not key == 'genres':   # else: doesn't work for some reason
                    
                    for series in series_collection:
                        #print 'Current key is ' + key
                        #print series[key], filters[key], series['genres']
                        if (key in series and series[key] == filters[key]) or (key == 'genre' and filters[key] in series['genres']):
                            new_coll.append(series)
                series_collection = new_coll
        
        for series in series_collection:
            addon.add_directory({'src': 'aplus', 'list': 'episodes', 'name': series['name'], 'seriesid': series['id']}, {'title': series['name'].encode('UTF-8'), 'plot': series['description']}, img='http://www.animeplus.tv/images/series/big/' + str(series["id"])+'.jpg')
    
    def aplus_genres(self, coll):
        genres = []
        
        for series in coll:
            
            for genre in series['genres']:
                
                if not genre in genres:
                    genres.append(genre)
        genres.sort()
        
        for genre in genres:
            addon.add_directory({'src': 'aplus', 'list': 'genre', 'genre': genre}, {'title': genre})
    
    def aplus_episodes_api(self, seriesid, name):
        episodes = get_json('http://api.animeplus.tv/GetDetails/' + seriesid, 'aplus')
        
        for episode in episodes['episode']:
            addon.add_directory({'src': 'aplus', 'list': 'sources', 'name': episode['name'], 'episodeid': episode['id']}, {'title': episode['name'].encode('UTF-8')})
        addon.end_of_directory()
        
    def aplus_sources_api(self, episodeid, name):
        sources = get_json('http://api.animeplus.tv/GetVideos/' + episodeid + '?direct', 'aplus')
        mctr = 1
        play_url = {}
        
        for vid_group in sources:
            
            for idx in range(len(vid_group)):
                mirror_name = '' # not declared in source, but it still works...?
                
                if vid_group[idx]['source'] == 'storage':
                    mirror_name = vid_group[idx]['link'].split('/')[2]
                    
                else:
                    mirror_name = vid_group[idx]['source']
                add_video_item({'list': 'play', 'name': name, 'url': vid_group[idx]['link']}, {'title': 'Part ' + str(mctr) + ', Mirror ' + str(idx+1) + ' (' + mirror_name + ')'})
                
                if play_url.has_key(idx):
                    play_url[idx] = play_url[idx] + '|' + vid_group[idx]['link']
                    
                else:
                    play_url[idx] = vid_group[idx]['link']
            mctr = mctr + 1
            
        for key in play_url:
            
            if play_url[key].find('|') > -1:
                # TODO: This most likely needs fixing...
                addon.add_video_item({'list': 'mplay', 'urls': play_url[key]}, {'title': "-----Play all mirror " + str(key+1) + " parts ------"})
        addon.end_of_directory()

class couchtuner:
    
    def find_base(self):
        # start with couchtuner.city and find actual list URL from there (slight future proof in case something gets taken down)
        dead = ['eu', 'la']
        live = ['city', 'com', 'ag', 'ch']
        live.sort()
        
        for tld in live:
            url = 'http://www.couchtuner.' + tld
            page = utils().get_page(url)
            #print 'page = ' + str(page)
            
            if 'Couch Tuner TV Videos FREE:' in page.title.string:   # need a better way to validate the page
                return url
    
    def get_series_info(self, url):
        # TODO: change to pull from IMDB instead, and to store the info
        page = get_page(url)
        
        try:
            image = page.find_all('img')[1]['href']
            
        except:
            image = ''
        description = page.find_all('p')[0].string
        episodes = page.find_all('div', class_='entry')[0].find_all('li')
        epi_str = ''
        
        if 'Couchtuner. ' in description:
            description = description.split('Couchtuner.')[1]   # TODO: Strip up to space as well
        
        return {'image': image, 'description': description}
        
    def index(self):
        base_url = self.find_base()
        series_collection = utils().get_page(base_url + '/tv-lists/').find_all('div', class_='entry')[0].find_all('li')
        #print 'series_collection = ' + str(series_collection)
        
        for series in series_collection:
            name = series.a.string.encode('UTF-8')
            url = base_url + series.a['href']
            addon.add_directory({'src': 'ctun', 'list': 'episodes', 'base': base_url, 'name': name, 'url': url}, {'title': name, 'plot': ''}, img='')
    
    def recent(self):
        pass
    
    def sched(self):
        pass
    
    def episodes(self, queries):
        # TODO: Fix to handle bad formatting, unicode stuff (show 19-2 s
        #print 'episodes arg: ' + str(queries)
        page = utils().get_page(queries['url'])
        episodes = page.find_all('div', class_='entry')[0].find_all('li')
        
        for itm in episodes:
            name = ''
            
            try:
                name = itm.a.contents[0]
                
            except:
                continue
            #print 'itm = ' + str(itm)
            
            try:
                if not itm.string:
                    name = name + itm.contents[0].contents[1]
                    
            except:
                #print 'Unhandled error in episodes, name = ' + name.encode('UTF-8') + ', itm = ' + str(itm).encode('UTF-8')
                pass
            url = itm.a['href']
            
            if not '://' in url:
                url = queries['base'] + url
            addon.add_directory({'src': 'ctun', 'list': 'sources', 'base': queries['base'], 'name': name, 'url': url}, {'title': name.encode('UTF-8'), 'plot': ''}, img='')
        
        
class utils:
    
    def get_page(self, url):
        return BeautifulSoup(net.http_GET(url).content, 'html5lib')

class sources:
    supported = ['allmyvideos.net']
    
    def couchtuner(self, url, name):
        page = utils().get_page(url)
        iframes = page.find_all('div', class_='entry')[0].find_all('iframe')
        urls = []
        
        if not iframes:
            # NB: This can be made into a crawler if there are too many variations
            url = page.find_all('div', class_='entry')[0].find_all('a')[0]['href']
            page = utils().get_page(url)
            iframes = page.find_all('div', class_='entry')[0].find_all('iframe')
        
        for iframe in iframes:
            url = iframe['src']
            
            if url.split('/')[2] in self.supported:
                urls.append(url)
            
            else:
                print 'Unsupported source url: ' + url
        self.find_vid_links(urls)
        
    def find_vid_links(self, urls):
        # Takes a list of URLs and finds associated video URLs
        vid_info_coll = []
        
        for url in urls:
            
            if 'allmyvideos.net' in url:
                vid_info_coll = vid_info_coll + self.allmyvideos(url)
        
        for vid_info in vid_info_coll:
            name = 'video'
            
            for itm in vid_info:
                
                if itm == 'url' or itm == 'image':
                    continue
                name = name + ' | ' + vid_info[itm]
            add_video_item({'list': 'play', 'name': name, 'url': vid_info['url']}, {'title': name}, img = vid_info['image'])
        
    def allmyvideos(self, url):
        page = utils().get_page(url)
        scripts = page.find_all('div', id='player_code')[0].find_all('script')
        data = ''
        image = ''
        for script in scripts:
            
            if script.string and 'jwplayer(\'flvplayer\').setup(' in script.string:
                lines = script.string.split('\n')
                flag = False
                
                for line in lines:
                    
                    if '"image"' in line:
                        image = line.split(' : "')[1][:-2]   # get the image URL from the dict key/value
                        
                    if '"sources"' in line:
                        flag = True
                        line = '['
                        
                    if flag:
                        data = data + line

                        
                    if flag and '],' in line:
                        flag = False
                        data = data[:-1]
                        break
        print 'json data = ' + data
        data = json.loads(data)
        
        for idx in range(len(data)):
            # put the image URL in each video info dict, change the key name from file to url for the video link, delete unnecessary key
            data[idx]['image'] = image
            data[idx]['url'] = data[idx]['file']
            del data[idx]['file']
            del data[idx]['default']
        return data
            
    
## ripped from animego
def CreateList(videoLink):
        liz = xbmcgui.ListItem('[B]PLAY VIDEO[/B]', thumbnailImage="")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.add(url=videoLink, listitem=liz)

## end animego rip

## ripped from addon.common
def add_video_item(queries, infolabels, properties=None, contextmenu_items='', context_replace=False, img='', fanart='', resolved=False, total_items=0, playlist=False, item_type='video', is_folder=False):
        '''
        Adds an item to the list of entries to be displayed in XBMC or to a 
        playlist.
        
        Use this method when you want users to be able to select this item to
        start playback of a media file. ``queries`` is a dict that will be sent 
        back to the addon when this item is selected::
        
            add_item({'host': 'youtube.com', 'media_id': 'ABC123XYZ'}, 
                     {'title': 'A youtube vid'})
                     
        will add a link to::
        
            plugin://your.plugin.id/?host=youtube.com&media_id=ABC123XYZ
        
        .. seealso::
        
            :meth:`add_music_item`, :meth:`add_video_item`, 
            :meth:`add_directory`
            
        Args:
            queries (dict): A set of keys/values to be sent to the addon when 
            the user selects this item.
            
            infolabels (dict): A dictionary of information about this media 
            (see the `XBMC Wiki InfoLabels entry 
            <http://wiki.xbmc.org/?title=InfoLabels>`_).
            
        Kwargs:
            
            properties (dict): A dictionary of properties that can be set on a list item
            (see the `XBMC Wiki InfoLabels entry and locate Property() elements
            <http://wiki.xbmc.org/?title=InfoLabels>`_).
            
            contextmenu_items (list): A list of contextmenu items
            
            context_replace (bool): To replace the xbmc default contextmenu items
                    
            img (str): A URL to an image file to be used as an icon for this
            entry.
            
            fanart (str): A URL to a fanart image for this entry.
            
            resolved (str): If not empty, ``queries`` will be ignored and 
            instead the added item will be the exact contentes of ``resolved``.
            
            total_items (int): Total number of items to be added in this list.
            If supplied it enables XBMC to show a progress bar as the list of
            items is being built.
            
            playlist (playlist object): If ``False`` (default), the item will 
            be added to the list of entries to be displayed in this directory. 
            If a playlist object is passed (see :meth:`get_playlist`) then 
            the item will be added to the playlist instead
    
            item_type (str): The type of item to add (eg. 'music', 'video' or
            'pictures')
        '''
        infolabels = addon.unescape_dict(infolabels)
        if not resolved:
            if not is_folder:
                queries['play'] = 'True'
            play = addon.build_plugin_url(queries)
        else: 
            play = resolved
        listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, 
                                    thumbnailImage=img)
        listitem.setInfo(item_type, infolabels)
        #listitem.setProperty('IsPlayable', 'true')   # this line was causing the play problem...
        listitem.setProperty('fanart_image', fanart)
        
        if properties:
            for prop in properties.items():
                listitem.setProperty(prop[0], prop[1])

        if contextmenu_items:
            listitem.addContextMenuItems(contextmenu_items, replaceItems=context_replace)        
        if playlist is not False:
            addon.log_debug('adding item: %s - %s to playlist' % \
                                                    (infolabels['title'], play))
            playlist.add(play, listitem)
        else:
            addon.log_debug('adding item: %s - %s' % (infolabels['title'], play))
            xbmcplugin.addDirectoryItem(addon.handle, play, listitem, 
                                        isFolder=is_folder, 
                                        totalItems=total_items)
    ## end addon.common rip
main()