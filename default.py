import sys
import xbmcgui
import xbmcplugin
from addon.common.addon import Addon
from addon.common.net import Net

addon = Addon('plugin.video.skeledrew.anime-watcher', argv=sys.argv)
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
    
class main:
    def __init__(self):
        
        if len(addon.queries) == 1 and addon.queries['mode'] == 'main':
            # default query
            dirs().root()
        
        try:
            target_dir = addon.queries['dir']
            
            if target_dir == 'lib':
                dirs().lib()
                
            if target_dir == 'aplus':
                dirs().aplus()
        
        except:
            pass
        
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
        addon.add_directory({'list': 'index'}, {'title': 'Index'})
        addon.add_directory({'list': 'pop'}, {'title': 'Popular'})
        addon.add_directory({'list': 'new'}, {'title': 'New'})
        addon.add_directory({'list': 'recent'}, {'title': 'Recent'})
        addon.add_directory({'list': 'ongoing'}, {'title': 'Ongoing'})
        addon.add_directory({'list': 'complete'}, {'title': 'Completed'})
        addon.add_directory({'list': 'genres'}, {'title': 'Genres'})
        addon.add_directory({'list': 'recrel'}, {'title': 'Recent Releases'})
        addon.add_directory({'list': 'recadd'}, {'title': 'Recently Added Series'})
        addon.end_of_directory()
        
main()