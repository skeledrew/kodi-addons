import sys
import xbmcgui
import xbmcplugin
from addon.common.addon import Addon
from addon.common.net import Net
from bs4 import BeautifulSoup
from urllib import quote_plus, unquote_plus
import json
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
            return
        
        if 'list' in addon.queries:
            # navigate dynamic site lists
            target_list = addon.queries['list']
            
            if target_list == 'index':
                lists().aplus_index_api()
                
            if target_list == 'episodes':
                lists().aplus_episodes_api(addon.queries['seriesid'], addon.queries['name'])
                
            if target_list == 'sources':
                lists().aplus_sources_api(addon.queries['episodeid'], addon.queries['name'])
                
            if target_list == 'play':
                kodi_player.play(addon.queries['url'])
            return
        
        else:
            addon.add_directory({'list': 'index'}, {'title': "Didn't get it..."})
            #addon.add_directory({'list': 'index'}, {'title': target_list})
        
        test_area()
            
class dirs:
    
    def root(self):
        addon.add_directory({'dir': 'lib'}, {'title': 'Library'})
        addon.add_directory({'dir': 'fav'}, {'title': 'My List'})
        addon.add_directory({'dir': 'cfg'}, {'title': 'Settings'})
        addon.end_of_directory()
        
    def lib(self):
        addon.add_directory({'dir': 'aplus'}, {'title': 'Anime Plus'})
        addon.add_directory({'dir': 'adub'}, {'title': 'Anime Dub'})
        addon.add_directory({'dir': 'acrazy'}, {'title': 'Anime Crazy'})
        addon.add_directory({'dir': 'ablog'}, {'title': 'Anime Blog'})
        addon.add_directory({'dir': 'afreak'}, {'title': 'Anime Freak'})
        addon.add_directory({'dir': 'afav'}, {'title': 'Anime Fav'})
        addon.add_directory({'dir': 'cdub'}, {'title': 'Cartoon Dub'})
        addon.end_of_directory()
        
    def aplus(self):
        addon.add_directory({'src': 'aplus', 'list': 'index'}, {'title': 'Index'})
        addon.add_directory({'src': 'aplus', 'list': 'pop'}, {'title': 'Popular'})
        addon.add_directory({'src': 'aplus', 'list': 'new'}, {'title': 'New'})
        addon.add_directory({'src': 'aplus', 'list': 'recent'}, {'title': 'Recent'})
        addon.add_directory({'src': 'aplus', 'list': 'ongoing'}, {'title': 'Ongoing'})
        addon.add_directory({'src': 'aplus', 'list': 'complete'}, {'title': 'Completed'})
        addon.add_directory({'src': 'aplus', 'list': 'genres'}, {'title': 'Genres'})
        addon.add_directory({'src': 'aplus', 'list': 'recrel'}, {'title': 'Recent Releases'})
        addon.add_directory({'src': 'aplus', 'list': 'recadd'}, {'title': 'Recently Added Series'})
        addon.end_of_directory()
      
class lists:
    '''
    def aplus_index(self):
        resp = net.http_GET('http://www.animeplus.tv/anime-list')
        soup = BeautifulSoup(resp.content, 'html5lib')
        series_index = soup.find_all('table', class_="series_index")
        
        for alnum in series_index:
            # list of series by alphanum
            series_list = alnum.find_all('a')
            
            for series in series_list:
                #individual series in each alphanum list
                name = fix_uni(series.string)
                url = quote_plus(series['href'])
                #addon.show_ok_dialog(url, title=name)
                
                try:
                    addon.add_directory({'list': 'episodes', 'name': name, 'url': url}, {'title': name})
                    
                except UnicodeEncodeError:
                    addon.add_directory({'list': 'episodes', 'name': url, 'url': url}, {'title': '<< ' + unquote_plus(url).split('tv/')[1] + ' >>'})
        addon.end_of_directory()
        
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
    def aplus_index_api(self):
        series_collection = get_json('http://api.animeplus.tv/GetAllShows', 'aplus')
        
        for series in series_collection:
            addon.add_directory({'src': 'aplus', 'list': 'episodes', 'name': series['name'], 'seriesid': series['id']}, {'title': series['name'].encode('UTF-8'), 'plot': series['description']}, img='http://www.animeplus.tv/images/series/big/'+str(series["id"])+'.jpg')
        addon.end_of_directory()
        
    def aplus_episodes_api(self, seriesid, name):
        episodes = get_json('http://api.animeplus.tv/GetDetails/' + seriesid, 'aplus')
        
        for episode in episodes['episode']:
            addon.add_directory({'src': 'aplus', 'list': 'sources', 'name': episode['name'], 'episodeid': episode['id']}, {'title': episode['name']})
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
                addon.add_video_item({'list': 'play', 'url': vid_group[idx]['link']}, {'title': 'Part ' + str(mctr) + ', Mirror ' + str(idx+1) + ' (' + mirror_name + ')'})
                #addon.show_ok_dialog(str(mirror_name))
                
                if play_url.has_key(idx):
                    play_url[idx] = play_url[idx] + '|' + vid_group[idx]['link']
                    
                else:
                    play_url[idx] = vid_group[idx]['link']
            mctr = mctr + 1
            
        for key in play_url:
            
            if play_url[key].find('|') > -1:
                addon.add_video_item({}, {'title': "-----Play all mirror " + str(key+1) + " parts ------"})
        addon.end_of_directory()
        
# ripped from animego
def PLAYLIST_VIDEOLINKS(vidlist,name):
        ok=True
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        #time.sleep(2)
        links = vidlist.split('|')
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        totalLinks = len(links)-1
        loadedLinks = 0
        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
        pDialog.update(0,'Please wait for the process to retrieve video link.',remaining_display)
        
        for videoLink in links:
                #CreateList(ParseVideoLink(videoLink,name,name+str(loadedLinks + 1)))
                CreateList(videoLink)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                #print percent
                remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
                pDialog.update(percent,'Please wait for the process to retrieve video link.',remaining_display)
                if (pDialog.iscanceled()):
                        return False   
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                d = xbmcgui.Dialog()
                d.ok('videourl: ' + str(playList), 'One or more of the playlist items','Check links individually.')
        return ok

def playVideo(url,name,movieinfo):
        #vidurl=ParseVideoLink(url,name,movieinfo);
        vidurl=url;
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(vidurl)
# end rip

main()