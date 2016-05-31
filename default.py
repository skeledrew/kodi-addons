import sys
import xbmcgui
import xbmcplugin
from addon.common.addon import Addon
from addon.common.net import Net
from bs4 import BeautifulSoup
from urllib import quote_plus, unquote_plus

addon = Addon('plugin.video.skeledrew.anime-watcher', argv=sys.argv)
net = Net()
#addon_handle = int(sys.argv[1])
addon_handle = addon.handle

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
                lists().aplus_index()
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
    
    def aplus_index(self):
        resp = net.http_GET('http://www.animeplus.tv/anime-list')
        soup = BeautifulSoup(resp.content, 'html5lib')
        series_index = soup.find_all('table', class_="series_index")
        #addon.add_directory({'dir': 'cdub'}, {'title': str(resp.content)})
        
        for alnum in series_index:
            # list of series by alphanum
            series_list = alnum.find_all('a')
            
            for series in series_list:
                #individual series in each alphanum list
                name = fix_uni(series.string)
                url = quote_plus(fix_uni(series['href']))
                #addon.show_ok_dialog(url, title=name)
                
                try:
                    addon.add_directory({'series': 'true', 'name': name, 'url': url}, {'title': name})
                    
                except UnicodeEncodeError:
                    addon.add_directory({'series': 'true', 'url': url}, {'title': '<<UnicodeEncodeError encountered in text>>'})
        addon.end_of_directory()
        
main()