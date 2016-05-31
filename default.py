import sys
import xbmcgui
import xbmcplugin
from addon.common.addon import Addon
from addon.common.net import Net
from bs4 import BeautifulSoup
from urllib import quote_plus, unquote_plus
import json

addon = Addon('plugin.video.skeledrew.anime-watcher', argv=sys.argv)
net = Net()

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

def get_json(url):
    # TODO: should probably do some error checking...
    return json.loads(net.http_GET(url).content)

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
                
            '''if target_list == 'episodes':
                lists().aplus_episodes(addon.queries['url'])
                
            if target_list == 'sources':
                lists().aplus_sources(addon.queries['url'])'''
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
        series_collection = get_json('http://api.animeplus.tv/GetAllShows')
        #addon.show_ok_dialog(str(series_collection))
        
        for series in series_collection:
            addon.add_directory({'src': 'aplus', 'list': 'episodes', 'media': 'shows', 'seriesid': series['id']}, {'title': series['name'].encode('UTF-8'), 'plot': series['description']}, img='http://www.animeplus.tv/images/series/big/'+str(series["id"])+'.jpg')
        addon.end_of_directory()
        
main()