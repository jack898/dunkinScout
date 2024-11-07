# [DunkinScout](https://nmul1801.github.io/dunkin-ng/)
Find the cheapest Dunkin near you for any particular menu item.. or 
just an Iced Original, as a benchmark.

I was shocked to realize just how much the price of each item varies per location,
even at stores less than a mile apart. Save some money with this tool!

- For drinks, shows the price for a small.
- Price shown is before any taxes/discounts.

# Web app
Thanks to fellow developer [@nmul1801](https://github.com/nmul1801), DunkinScout is now available online at [https://nmul1801.github.io/dunkin-ng/](https://nmul1801.github.io/dunkin-ng/)!


# Easy Usage (if you do not want to install Python)
(Windows only, for now)
1. Download dunkScout.exe from the Releases
2. Simply double click and it should prompt you for your zip code OR latitude/longitude,
item name, and distance.

# Usage
```sh
➜ pip install -r requirements.txt
➜ python dunkScout.py [-zip ZIP] [-lat LAT] [-long LONG] [-item ITEM] [-dist DIST]
```
  * Example: python dunkScout.py -lat 42.161621 -long -71.147720 -item "Original Blend Iced Coffee" -dist 2
    - lat: Latitude for your current location
    - long: Longitude for your current location
    - item: Name of item to price out (must be exact match to menu name--unicode characters should not be encoded)
    - dist: Maximum search radius, in miles
  * Example using zip code: python dunkScout.py -zip 10006 -item "Original Blend Iced Coffee" -dist 2
  
You can also launch it with no arguments, and you will be prompted for each argument before it searches.

# Installation/Dependencies
Download and install [Python](https://www.python.org/downloads/) >=3.6, and add it
to your environment variables as appropriate for your OS. Use pip to install dependencies.


# Acknowledgments
This project was surprisingly much more involved than initially expected...

[BlueStacks 5](https://www.bluestacks.com/): Sniffed the Dunkin API from the Android Dunkin app, which I hosted on a BlueStacks emulator.

[Magisk](https://github.com/topjohnwu/Magisk): Needed to root Android to add a global proxy via adb and remove SSL pinning.

[EdXposed](https://github.com/ElderDrivers/EdXposed): Necessary for TrustMeAlready.

* [TrustMeAlready](https://github.com/ViRb3/TrustMeAlready): Used to disable SSL pinning on the Dunkin' app.

[Charles Proxy](https://www.charlesproxy.com/): Hosted proxy to log API requests.

[PyInstaller](https://pyinstaller.org/en/stable/): Used to make 'no python' executable version.

[Dunkin'](https://www.dunkindonuts.com/en): Last but not least... I'll admit, as a non-New Englander, I didn't understand
the hype. But I've been indoctrinated. Even as a "coffee snob", there is a place for Dunkin when you want a sweeter drink from
a shop that isn't $10.

# Procedure
- Dunkin hosts no menu (with prices) on any website, so I needed to sniff the menu API from their app.

- I first tried to set up a proxy with Charles Proxy and sniff from my iOS device--however, the requests were encrypted as Dunkin
uses SSL pinning on their app. 

- I switched to an Android emulator with Charles Proxy, and rooted it so I could install an Xposed framework module to disable SSL pinning. 

- From here, I played around with the app and searched through the requests.

- I quickly found the API endpoint--yes, the one API endpoint which returns all deals, featured items, and every menu item...
(seriously, there must be a better way to store a menu than a single 42k line JSON object)

- From here I figured out how to parse the menu and store locator JSON response bodies to find specific stores and return the price
of specific items on their menus.

# Debugging
- Ensure you are exactly matching the name of the item as it appears on the menu; any unicode characters e.g. ®, should
appear as symbols rather than any encoding.

- Some locations just may not carry that item! You should just be able to click past these, but if every location is indicating
that it does not have the item, you may have made a typo in the name.

- If you are getting an "API Call failed" error, the Bearer token has probably expired. You will need to retrieve a new one by
disabling SSL pinning and then sniffing the HTTPS traffic to the Dunkin app on an iOS or Android device, and extracting the
token from the "Authorization" header.



# Possible future additions 
* Take argument for city name/state and determine latitude and longitude
* Some kind of fuzzy matching/Levenshtein distance algorithm for item name,
rather than just exact match

# Legal Disclaimer and License
This software tool, **DunkinScout, is not affiliated with, endorsed by, or in any way officially connected with Dunkin' Brands Group, Inc., or any of its subsidiaries or affiliates.** The name "Dunkin'" as well as related names, marks, emblems, and images are registered trademarks of their respective owners.

The DunkinScout program utilizes publicly accessible API endpoints from the Dunkin' mobile application. This tool is provided for educational and personal use only. The author makes no representation or warranty of any kind, express or implied, regarding the accuracy, availability, reliability, or completeness of the data retrieved by this program. Users are advised that use of the DunkinScout program is at their own risk, and the author is not responsible for any damages or issues that may arise from its use.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Changelog

- Version 0.3: Added option to take zip code rather than latitude/longitude, thanks to @logyball, 10/3/24

- Version 0.2: Added prompt for keypress at end of execution, so exe doesn't
exit immediately after completing, 9/1/24

- Version 0.1: Added executable version from PyInstaller for those
without Python, made all CLI arguments optional, 9/1/24

- Version 0.0: First version, 8/31/24
