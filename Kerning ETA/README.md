# Kerning ETA
"I'm almost done with this pairlist," you say? 
Nope! You're probably not. Install this as a [start-up script](https://robofont.com/documentation/how-tos/setting-up-a-startup-script/?highlight=start-up), and you'll get a nice little message on the top-right of your Metrics Machine extension with an estimated time to expect to be done with your pairlist, at your current rate.

**Note:**
This tool will only look at your last 20 pairs to make an estimation. If you took more than 60 seconds on a pair, it will start over with the next 20 pairs. Also, if you have more than 1 MM window open, switching windows will restart the time-estimation clock, because you're probably finding a new groove anyway.

**Also:**
This will display time in 12-hour AM/PM. If you'd like 24-hour time. Set `twenty_four = True` near the beginning of the script.

### Credits
```
Thanks to Tal Leming for pointing me to some MM UI infrastructure.

Ryan Bugden
23.03.22 Support for multiple MM windows / closing & reopening.
22.07.28
```