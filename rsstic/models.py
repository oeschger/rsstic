from django.db import models
from django import forms

class ItemForm(forms.Form):
    item_name = forms.CharField(max_length=100)
    item_url  = forms.CharField(max_length=100)
    item_desc = forms.CharField(max_length=500,widget=forms.Textarea)
    
class FeedForm(forms.Form):
    feed_name = forms.CharField(max_length=100)
    feed_url  = forms.CharField(max_length=100)
    feed_desc = forms.CharField(max_length=500,widget=forms.Textarea)

class Feed(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300,blank=True)
    url = models.URLField()
    status = models.CharField(max_length=12,blank=True) 
    last_updated = models.DateField(blank=True,null=True)
    mods = models.CharField(max_length=500,blank=True)

# an item you add to your project
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300,blank=True)
    url = models.URLField()
    status = models.CharField(max_length=12,blank=True) 

    
class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300,blank=True)
    feeds = models.ManyToManyField(Feed,blank=True)
    items = models.ManyToManyField(Item,blank=True)
    
    owner_email = models.EmailField(blank=True)
    owner_name = models.CharField(max_length=30)


                                                    
