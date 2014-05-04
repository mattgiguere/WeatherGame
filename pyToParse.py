# -*- encoding: utf-8 -*-
# Made by http://www.elmalabarista.com
# This will teach about how use parse.com as your database

# About

# parse.com is a SAAS that provide a ready-to-use NOSQL backend
# and related services, great for quick prototypes. Also, can be used
# from several plataforms and languages

# Official documentation
# https://parse.com/docs/


import os, sys

from utils import printTitle, printSubTitle, printExplain, printTab, printError

printTitle("Parse.com is a NOSQL in the cloud")
printExplain("You need to create a account at parse.com. Is free")
print "https://parse.com/#signup"

printExplain("And create a sample APP")
print "https://parse.com/apps/new"
printExplain("Change the values below to the ones supplied by Parse for your application")
# Are in the 'settings' tab of each app

APPLICATION_ID = "APPLICATION_ID_HERE"
REST_API_KEY = "REST_API_KEY_HERE"

if APPLICATION_ID == "APPLICATION_ID_HERE":
    printTitle("You need to create a parse app and supply the auth values")
    sys.exit(-1)


printExplain("We will use the ParsePy library")
# Install with pip install git+https://github.com/dgrtwo/ParsePy.git

from parse_rest.connection import register, ParseBatcher
# Alias the Object type to make clear is not a normal python Object
from parse_rest.datatypes import Object as ParseObject

printSubTitle("First register the app")

register(APPLICATION_ID, REST_API_KEY)


printSubTitle("Parse is a NOSQL database.")
# https://en.wikipedia.org/wiki/NoSQL
printExplain("So, you not need to pre-create the data schema, and can drop/add data & columns at will")

anyObject = ParseObject()

printExplain("Simple set a value to the object. No need to exist before..")
anyObject.title = 'Hello world'
anyObject.score = 100


def saveToParse(anyObject):
    print "Saving..."

    anyObject.save()

    print "Done!"

saveToParse(anyObject)

printExplain("Parse automatically add the nexts read-only fields on save:")

printSubTitle("objectId")
printExplain("The objectId is the primary-key of the objects. Is the way to identify this object")
print "The objectId is: ", anyObject.objectId

printSubTitle("objectId")
printExplain("The objectId is the primary-key of the objects. Is the way to identify this object")
print "The objectId is: ", anyObject.objectId

printSubTitle("createdAt")
printExplain("The createdAt is the date (UTC) when this object was created")
print "The object was created on: ", anyObject.createdAt

printSubTitle("updatedAt")
printExplain("The updatedAt is the last date (UTC) the object was modified")
print "The object last update on: ", anyObject.updatedAt

print "When the object is created, both dates are the same"

printExplain('You can add new fields anytime')

anyObject.otherField = True
anyObject.score = 200

saveToParse(anyObject)
print "The object last update on: ", anyObject.updatedAt

printExplain("In the parse.com Data Browser, you see that is created a table called 'Object'")
print "To have a better name, you need to subclass"

printExplain("If you run this several times, the object will be duplicated")
print """
In contrast with Sql databases, you need to code the constrains/validations yourself"

And check if a object will duplicate or not the data before to save. Parse.com not
have built-in functionality to constrain the data to avoid duplicated objects or anything
related at all. Only provide the storage, and the default fields
"""

printTitle("Query the data store")

printSubTitle("Query for exact object")
print "You ask for a exact object, you need to query by objectId"

findObject = ParseObject.Query.get(objectId=anyObject.objectId)

print "The object with objectId = ", anyObject.objectId, ' exist? ', not(findObject is None)

printSubTitle("To get all the objects, use all()")

# The queryset return a generator. I need to convert to list to count it
# This is not the best way. Ask only for the data you really need
print "Exist %d objects now " % len(list(ParseObject.Query.all()))

printSubTitle("Like Django, Querysets can have constraints added by appending the name of the filter operator")
print "The list of constrains is at https://www.parse.com/docs/rest#queries-constraints"
print "Objects with score>=100 ", len(list(ParseObject.Query.filter(score__gte=100)))


printTitle("A simple news app")
printExplain("Let's build some classes to store news")


class Source(ParseObject):
    pass


class Article(ParseObject):
    pass

printExplain("Get the news from the yahoo rss feed.")
# Feedparser is the popular option for get RSS/Atom feeds
# http://pythonhosted.org/feedparser/

import feedparser

d = feedparser.parse('http://news.yahoo.com/rss/')

printSubTitle('Downloading news from %s' % d.feed.title)
print d.feed.link

printExplain("To model a one-t-many relation, create a Source object and point it to each article")


printExplain("First get the sources that are already created")

sourcesQry = Source.Query.all()

sources = {source.href: source for source in sourcesQry}


def createSource(title, href):
    if href in sources:
        return sources[href]

    source = Source(**locals())
    saveToParse(source)

    sources[source.href] = source

    return source


def createArticle(title, description, source, date):
    article = Article(**locals())

    return article


articles = []
for entry in d.entries:
    # Is a real new with source? The rrs return images and other stuff
    if 'source' in entry:
        source = createSource(**entry.source)

        articles.append(createArticle(
            title=entry.title,
            description=entry.description,
            source=source,
            date=entry.published
        ))

printExplain("To save several objects, use the batcher")

batcher = ParseBatcher()
batcher.batch_save(articles)

print "Our news sources:"

for source in sources.values():
    printTab(source.title)

print "The news from ", sources.values()[0].title

for new in Article.Query.filter(source=sources.values()[0]):
    printSubTitle(new.title)
    print new.description

printTitle("Conclusion")
print """
Parse.com provide a easy way of store/query data, with not admin skills.

Is not a replacemente for a proper Sql database (like postgresql or sql server)
but provide a flexible data model apropiated for quick development and/or scalable
acces to data, where the data must be denormalized anyway..
"""
