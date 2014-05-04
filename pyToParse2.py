#!/usr/bin/env python

import os, sys

#from utils import printTitle, printSubTitle, printExplain, printTab, printError

APPLICATION_ID = "aOmfYWxfdaqrD9aMOtp7a3UinrfOAqNMyVxIjLzm"
REST_API_KEY = "AkHGq6xQCd67e8Tj9xcXY3PirvzZstur7DBaURuX"
MASTER_KEY = "0sbEqmUiRqarMV8zV5WN18pvOaS0N5O2ItUxbS7q"

from parse_rest.connection import register, ParseBatcher
# Alias the Object type to make clear is not a normal python Object
from parse_rest.datatypes import Object as ParseObject

register(APPLICATION_ID, REST_API_KEY)

anyObject = ParseObject()



print "Exist %d objects now " % len(list(ParseObject.Query.all()))

print("Like Django, Querysets can have constraints added by appending the name of the filter operator")
print "The list of constrains is at https://www.parse.com/docs/rest#queries-constraints"
print "Objects with score>=100 ", len(list(ParseObject.Query.filter(score__gte=100)))

