from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.utils import download_file, create_tmp_file, till_white, till_end
import re
from slackbot.globals import attributes
from plugins.admin.perms import is_approved
from jira import JIRAError

issue = "(\\S[^\\-\\s]*-[*\\d])"
j_key = "(\\S[^\\-\\s]*)"

try:
    db = attributes['db']
except KeyError:
    db = None

try:
    snakeman = attributes['snakeman']
except KeyError:
    snakeman = None

def keys():
    temp = []
    for x in snakeman.projects():
        temp.append(x.key)
    return temp

c_issue = "\\bcreate issue\\b %s %s" % (j_key, till_end)
c_issue_help = "create issue (KEY) (issue) - creates a jira issue under the specified key"
#@listen_to(c_issue, re.IGNORECASE, c_issue_help)
@respond_to(c_issue, re.IGNORECASE)
def jira_create_issue(message, key, summary):
    if is_approved(message, "admin"):
        key = key.upper()
        if key in keys():
            issue_dict = {
                'project':{'key':key},
                'summary': summary,
                'issuetype':{'name':'Story'}
            }
            new = snakeman.create_issue(fields=issue_dict)
            #message.send(str(new.fields))
            message.send("Issue Created %s" % (new.key))

a_comment = "\\badd comment\\b %s (.*$)" % issue
a_comment_help = "add comment (KEY)-(#) (comment) - adds a comment to the associated jira issue"
#@listen_to(a_comment, re.IGNORECASE, a_comment_help)
@respond_to(a_comment, re.IGNORECASE)
def jira_comment(message, issue, com):
    if is_approved(message, 'jira'):
        key = issue.partition("-")[0]
        num = issue.partition("-")[2]
        key = key.strip(" []<>$|.!@#$%^&*()").upper()
        num = num.strip(" []<>")
        if key in keys():
            try:
                resp = snakeman.add_comment('%s-%s' % (key, num), message.sent_by() +  " says " + com)
                message.send("Comment Added")
            except JIRAError:
                message.send("Issue does not exist.")
                return
        else:
            message.send("Key Not Found")

j_issue = "(\\S[^\\-\\s]*-[*\\d])"
j_issue_help = "(KEY)-(#) - Example: $WEST-3 brings up the details for the associated jira issue"
#@listen_to(j_issue, re.IGNORECASE, j_issue_help)
@respond_to(j_issue, re.IGNORECASE)
def jira_issue(message, issue):
    if is_approved(message, 'jira'):
        key = issue.partition("-")[0]
        num = issue.partition("-")[2]
        key = key.strip(" []<>$|.!@#$%^&*()").upper()
        num = num.strip(" []<>")
        if message.body['text'].strip("$ .").upper() == "%s-%s" % (key, num):
            temp = ""
            if key in keys():
                try:
                    issue = snakeman.issue('%s-%s' % (key, num))
                    temp += "Summary: %s\n" % issue.fields.summary
                    temp += "Priority: %s\n" % issue.fields.priority
                    temp += "Status: %s\n" % issue.fields.status
                    if issue.fields.comment.total > 0:
                        count = 1
                        for comment in issue.fields.comment.comments:
                            temp += "Comment #%d: %s - %s\n" % (count, comment.author, comment.body)
                            count += 1
                except JIRAError:
                    message.send("Issue does not exist.")
                    return

            message.upload_snippet(temp, "%s-%s\n" % (key.upper(), num))

j_projects = '\\bjira projects\\b'
j_projects_help = "jira projects - brings up a list of all available jira projects"
#@respond_to(j_projects, re.IGNORECASE, j_projects_help)
@listen_to(j_projects, re.IGNORECASE)
def jira_projects(message):
    if is_approved(message, 'jira'):
        proj = snakeman.projects()
        temp = ""
        for x in proj:
            temp += "%s -- %s\n" % (x.key, x.name)
        message.upload_snippet(temp.strip("\n"), "Jira Projects")
