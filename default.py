import sys
import xbmcgui
import xbmcplugin
from addon.common.addon import Addon
from addon.common.net import Net

addon = Addon('plugin.video.skeledrew.anime-watcher', argv=sys.argv)
addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')

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

xbmcplugin.endOfDirectory(addon_handle)