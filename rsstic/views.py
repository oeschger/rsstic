from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.template import Template, Context
from django import forms
from django.contrib import auth

import urllib2
from xml.dom import minidom
# from xml.etree import ElementTree as et

from djangito.rsstic.models import Feed, Project, Item, ItemForm, FeedForm
import djangito.rsstic.utils

def about(request):
	return render_to_response('about.html', {}, context_instance=RequestContext(request))

def project(request, project_id):
	current_project = Project.objects.get(id=project_id)
	return render_to_response('project.html', {'project': current_project,
						   'feeds': current_project.feeds.all(),
						   'items': current_project.items.all()},
				  context_instance=RequestContext(request))

def projects(request):
	projects = Project.objects.all()
	return render_to_response('projects.html' ,{'projects': projects}, context_instance=RequestContext(request))

def index(request):
	return render_to_response('welcome.html' ,{}, context_instance=RequestContext(request))


def home(request):
	feeds = Feed.objects.all()
	return render_to_response('feeds.html', {'feeds': feeds}, context_instance=RequestContext(request))


def view(request, project_id):
	# get the generated (or stored) view for a project's feeds
	current_project = Project.objects.get(id=project_id)

	itemlist = []
	for feed in current_project.feeds.all():
		current_xml = urllib2.urlopen(feed.url)

		# TODO: Rewite all this to use ElementTree
		# parse the xml/rss from the stored url
		xmldoc = minidom.parse(current_xml)
		items = xmldoc.getElementsByTagName('item')
	
		for item in items:
 			itemlist.append(djangito.rsstic.utils.itemize(item))
	itemlist = djangito.rsstic.utils.sort_itemlist(itemlist)
	return render_to_response('project_view.html', {'itemlist': itemlist }, context_instance=RequestContext(request))
	
def projectfeed(request, project_id):
	current_project = Project.objects.get(id=project_id)

	itemlist = []
	for feed in current_project.feeds.all():
		current_xml = urllib2.urlopen(feed.url)

		# TODO: Rewite all this to use ElementTree
		# parse the xml/rss from the stored url
		xmldoc = minidom.parse(current_xml)
		items = xmldoc.getElementsByTagName('item')
	
		for item in items:
			# TODO Get the mods as a JSON object and compare each item
			# If the url is in the mods list, do not put it in the output
 			itemlist.append(djangito.rsstic.utils.itemize(item))
	itemlist = djangito.rsstic.utils.sort_itemlist(itemlist)
	return render_to_response('project_feed.html', {'itemlist': itemlist }, context_instance=RequestContext(request))

	
def feed(request, feed_id):

	# retrieve the feed object from the database using get()
	current_feed = Feed.objects.get(id=feed_id)
	current_xml = urllib2.urlopen(current_feed.url)

	# parse the xml/rss from the stored url
	xmldoc = minidom.parse(current_xml)
	items = xmldoc.getElementsByTagName('item')
	itemlist = []
	
	for item in items:
		# title is always the text in the Text node child of the first child
		try:
			title = item.getElementsByTagName('title')[0].firstChild.data
			link  = item.getElementsByTagName('link')[0].firstChild.data
			desc  = item.getElementsByTagName('description')[0].firstChild.data
			itemlist.append({'title': title, 'link': link, 'desc': desc})
		except: pass

	return render_to_response('feed.html', {'itemlist': itemlist, 'feedname': current_feed.name },
				  context_instance=RequestContext(request))
	# return render_to_response('feed.html', {'the_list': newlist})

def removefeed(request, project_id, feed_id):
	if not request.user.is_authenticated():
		return redirect('%s?next=%s' % ( '/login', request.path ))

	current_project = Project.objects.get(id=project_id)
	feed = current_project.feeds.get(id=feed_id)
	feed.delete()
	return HttpResponseRedirect('/rsstic/project/'+project_id) # Redirect after POST

def removeitem(request, project_id, item_id):
	if not request.user.is_authenticated():
		return redirect('%s?next=%s' % ( '/login', request.path ))

	current_project = Project.objects.get(id=project_id)
	item = current_project.items.get(id=item_id)
	item.delete()
	return HttpResponseRedirect('/rsstic/project/'+project_id) # Redirect after POST

def additem(request, project_id):

	if not request.user.is_authenticated():
		return redirect('%s?next=%s' % ( '/login', request.path ))
	current_project = Project.objects.get(id=project_id)
	if request.method == 'POST': # If the form has been submitted...
		form = ItemForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			item_name = form.cleaned_data['item_name']
			item_url  = form.cleaned_data['item_url']
			item_desc = form.cleaned_data['item_desc']

			new_item = Item.objects.create(name=item_name,
						       url=item_url,
						       description=item_desc)

			current_project.items.add(new_item)
			return HttpResponseRedirect('/rsstic/project/'+project_id) # Redirect after POST
	else:
		form = ItemForm()

	c = {}
        c.update(csrf(request))
	c['form'] = form
	c['project'] = current_project
	return render_to_response('additem.html', c)


def addfeed(request, project_id):
	if not request.user.is_authenticated():
		return redirect('%s?next=%s' % ( '/login', request.path ))

	current_project = Project.objects.get(id=project_id)
	if request.method == 'POST': # If the form has been submitted...
		form = FeedForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			feed_name = form.cleaned_data['feed_name']
			feed_url  = form.cleaned_data['feed_url']
			feed_desc = form.cleaned_data['feed_desc']

			new_feed = Feed.objects.create(name=feed_name,
							url=feed_url,
							description=feed_desc)

			current_project.feeds.add(new_feed)
			return HttpResponseRedirect('/rsstic/project/'+project_id) # Redirect after POST
	else:
		form = FeedForm()

	c = {}
        c.update(csrf(request))
	c['form'] = form
	c['project'] = current_project
	return render_to_response('addfeed.html', c, context_instance=RequestContext(request))
