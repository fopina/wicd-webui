wicd-webui
==========
Simple WebUI to manage wireless networks using [wicd](http://wicd.sourceforge.net)

Why
-------
I'm a proud owner of [RPi](http://www.raspberrypi.org)!  
I like it mobile and I don't like having to plug it to a keyboard, screen and ethernet to be able to set it up in a new WiFi location everytime I move it.  

So:

- Installed [hostapd](http://hostap.epitest.fi/hostapd/) and [udhcpd](http://git.busybox.net/busybox/tree/networking/udhcp)
- Configured a self-hosted network on boot
- Installed [wicd](http://wicd.sourceforge.net)
- Configured wicd_webui.py to start as a service

Now, I can simply turn on my RPi, connect to its network on my phone, open http://10.10.10.1:5000/ in the browser and easily re-connect the RPi to the local WiFi.  
No cables, no keyboard, no screen, no fuss! :)


Links
-------
[wicd](http://wicd.sourceforge.net) - open source wired and wireless network manager for Linux  