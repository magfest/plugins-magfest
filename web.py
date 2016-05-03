from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.utils import download_file, create_tmp_file, till_white, till_end
from plugins.admin.perms import is_approved
from slackbot.globals import attributes
import urllib
import urllib2
import re
import json, os
from fuzzywuzzy import process, fuzz

try:
    db = attributes['db']
except KeyError:
    db = None

domain = "magfe.st"

possible_ubers = {"maglabs":"https://labs.uber.magfest.org/uber/registration/stats", "magstock":"https://magstock6.uber.magfest.org/uber/registration/stats",
                  "prime":"https://prime.uber.magfest.org/uber/registration/stats"}

url_command = "\\burl"
#@respond_to(url_command, re.IGNORECASE)
def url_commands(message):
    if is_approved(message, "web"):
        the_thing = str(message.body['text']).partition("url")[2].strip(" ").split(" ")
        if len(the_thing) > 0:
            for x in the_thing:
                pass

b = "\\bbadges"
@respond_to(b, re.IGNORECASE)
#@listen_to(b, re.IGNORECASE)
def badges(message):
    if is_approved(message, "any"):
        the_thing = str(message.body['text']).partition("badges")[2].strip(" ").split(" ")
        if the_thing[0] != "":

            for x in the_thing:

                extract = process.extractOne(x, possible_ubers.keys())

                if extract is not None:
                    partial_extract = fuzz.partial_ratio(x, extract[0])
                    if partial_extract > 85:
                        try:
                            attempt = urllib2.urlopen(possible_ubers[extract[0]])
                            thing = (attempt.read())
                            info = json.loads(thing)
                            message.send("%s\nBadges Sold: %s\nBadges Remaining: %s" % (extract[0].capitalize(), info['badges_sold'], info['remaining_badges']))
                        except KeyError:
                            message.send("Bad URL")
                    else:
                        message.send("Event Not Found")
                else:
                    message.send("Event Not Found")

        else:
            message.upload_snippet("\n".join(possible_ubers.keys()), "Possible Keys")