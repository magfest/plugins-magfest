# -*- coding: utf-8 -*-
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from plugins.admin.perms import is_approved
from slackbot.utils import till_white, till_end, to_utf8
import re

woagh = '\\bwo+?a+?g+?h+?\\b'
@listen_to(woagh, re.IGNORECASE)
@respond_to(woagh, re.IGNORECASE)
def woooaaagh(message):
    """wo(repeatable)a(repeatable)g(repeatable)h(repeatable)"""
    if is_approved(message, "any"):
        message.react("colossus")
        message.send("*WOAAAAAAAGGHHHH!*\nhttps://pbs.twimg.com/media/B8JvTeMIIAAbXYA.jpg:large")