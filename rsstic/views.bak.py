from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Template, Context

import urllib2
from xml.dom import minidom

# from xml.etree import ElementTree as et
from djangito.rsstic.models import Feed

t = Template("<li><input type='checkbox'/> {{ the_item }}</li>\n")

def about(request):
	return render_to_response('about.html', {})


def home(request):
	feeds = Feed.objects.all()
	return render_to_response('feeds.html', {'feeds': feeds})

def index(request):

	# retrieve the bfeed object from the database using get()
	bluemix_feed = Feed.objects.get(name="bfeed")
	bluemix_xml = urllib2.urlopen(bluemix_feed.url)

	# parse the xml/rss from the stored url
	xmldoc = minidom.parse(bluemix_xml)
	itemlist = xmldoc.getElementsByTagName('item')

	for item in itemlist:
		# title is always the text in the Text node child of the first child
		try:
			title = item.childNodes[1].firstChild.data
			print('adding ' + title)
			c = Context({"the_item": title})
			newlist += t.render(c)
		except: pass

	newlist += '</ul>'

	return render_to_response('feed.html', {'itemlist': itemlist })
	# return render_to_response('feed.html', {'the_list': newlist})

    
