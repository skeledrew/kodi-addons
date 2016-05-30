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

    #xbmcplugin.endOfDirectory(addon_handle)
    addon.end_of_directory()
    
class main:
    def __init__(self):
        
        if len(addon.queries) == 1 and addon.queries['mode'] == 'main':
            root_dir().get()
           
        else:
            test_area()
            
class root_dir:
    
    def get(self):
        addon.add_directory({'dir': 'lib'}, {'title': 'Library'})
        addon.add_directory({'dir': 'fav'}, {'title': 'Favorites'})
        addon.add_directory({'dir': 'cfg'}, {'title': 'Settings'})
        addon.end_of_directory()
        
main()