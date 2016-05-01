from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.utils import download_file, create_tmp_file, till_white, till_end
from plugins.admin.perms import is_approved
import urllib
import urllib2
import re
import json, os
from fuzzywuzzy import process, fuzz

domain = "magfe.st"

possible_ubers = {"maglabs":"https://labs.uber.magfest.org/uber/registration/stats", "magstock":"https://magstock6.uber.magfest.org/uber/registration/stats",
                  "prime":"https://prime.uber.magfest.org/uber/registration/stats"}

b = "\\bbadges"
#@respond_to(b, re.IGNORECASE)
#@listen_to(b, re.IGNORECASE)
def badges(message):
    if is_approved(message, "any"):
        the_thing = str(message.body['text']).partition("badges")[2].strip(" ").split(" ")
        if len(the_thing) > 0:

            for x in the_thing:
                extract = process.extractOne(x, possible_ubers.keys(), score_cutoff=80)
                if extract is not None:
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
            try:
                attempt = urllib2.urlopen(possible_ubers["prime"])
                thing = (attempt.read())
                info = json.loads(thing)
                message.send("%s\nBadges Sold: %s\nBadges Remaining: %s" % ("Prime", info['badges_sold'], info['remaining_badges']))
            except KeyError:
                message.send("Bad URL")