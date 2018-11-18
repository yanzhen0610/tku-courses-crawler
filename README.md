# tku-courses-crawler
crawl courses catalogs from http://esquery.tku.edu.tw
## Install required packages
```
pip -r requirements.txt
```
## Start fetching
```
python3 fetch_courses.py
```
and the result will save as `courses.db`(sqlite3)
## Known issue
* can't pair *practice course* and *cheif course*
