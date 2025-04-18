# MinecraftWikiExtractor
A Python script for extracting Minecraft wiki pages

### How to Use
1. Use **fetch_titles.py** to get the titles. The title may change continuously with version updates or Wiki modifications, so it is necessary to obtain the latest value. However, you can also use the one that comes with this repository (taken from April 16, 2025).
2. **(Optional)** Use **divide.py** to divide those titles into groups. You can customize the number of items in each group and the save location of the grouping files by modifying the source code.
3. Use **spider.py** to fetch and save the information. There is a random delay of several seconds between two requests, which can be adjusted by modifying the source code.
4. Use **validate.py** to validate and pick out those missing files. During the crawling process, there is a 1-2% probability of failure, which may result in some pages being missed. Run this code to identify those missing pages and save them into a separate group for re-crawling.
