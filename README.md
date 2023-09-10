This was created ostensibly to make collecting criminal evidence, or performing intelligence operations on Twitch criminals, much easier, but I guess you could use it for whatever you want.

This script traverses through the first 10 links on any Google Search with javascript enabled then grabs a full page screenshot of each link. It saves the time-of-results, order-of-results, links, and titles in a CSV file.

You may need to change the chromedriver executable (after installing Chrome separately) to match your OS and Chrome version. https://chromedriver.chromium.org/downloads

---

Usage python3 (or python) search.py term1 term2 term3 etc.

eg python3 search.py twitch sucks 

Will traverse the first 10 links on https://www.google.com/search?q=twitch+sucks

---

Why not let machines download full-records, then do research and summarize for you? You could query the machine with additional questions and it'll be able to answer those using your results, any previously provided information, and also the knowledge contained in the foundational model LLMs themselves. Why not Google Search yourself?

First demo on YouTube: https://youtu.be/mU3wKNKpOSI

This video demos the first stage of roughly ~30 minutes of coding and 1.5 hours of testing, that searches Google automatically for you to grab and download records for any query you desire. Adding the ability for 3rd party pre-existing foundational model LLMs to summarize content, which you could query for additional information, including by adding your existing information, would not be difficult, and I intend to do that soon. 

There are endless ways of leveraging machine and machine learning capabilities to improve your life, whether it's by using 3rd party tools or by programming your own stuff.

---

To traverse websites with deep reinforcement learning you'd probably need machine vision since xpath (or anything else) isn't descriptive enough and could be changed. Having something descriptive to build your value and policy networks is always required.

You may be able to scrape Google faster especially without javascript enabled, but this should be fast enough without turning your IP into a bot. Also manipulating other people's javascript is funny.

---

![Image 6-22-23 at 11 23 AM](https://github.com/bshang165/google-search/assets/118570793/9a23ab2d-ad74-4333-9346-6c0584c9053c)
