import dateutil.parser

def itemize(item):
    # title is always the text in the Text node child of the first child
    try:
        title   = item.getElementsByTagName('title')[0].firstChild.data
        link    = item.getElementsByTagName('link')[0].firstChild.data
        pubdate = item.getElementsByTagName('pubDate')[0].firstChild.data
        desc    = item.getElementsByTagName('description')[0].firstChild.data
        # guid    = item.getElementsByTagName('guid')[0].firstChild.data
        
        item_struct = {'title': title, 'link': link, 'pubdate': pubdate, 'desc': desc}
        return item_struct

    except:
        pass

def sort_items(items):
    """returns a tuple with the standard time format up front and reverse-sorted"""
    items_sorted = []
    for item in items:
        pubdate = item.findtext("pubDate")
        key = datify(pubdate)
        items_sorted.append((key, item))
        items_sorted.sort(reverse=True)
        return items_sorted


def datify(date_string):
    return dateutil.parser.parse(date_string)

# this needs datify too
# have to clean this stuff up with the sorted dates
def sort_itemlist(itemlist):
    itemlist.sort(key=lambda x: x['pubdate'], reverse=True)
    return itemlist

def validate_feed(feed_url):
    # WRITEME
    return True
