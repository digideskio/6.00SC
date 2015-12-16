# Problem Set 5
# Name: Shouvik Roy
# Collaborators: None
# Time: 2 hours
# 6.00 Problem Set 5
# RSS Feed Filter
import thread
import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

# -----------------------------------------------------------------------
#
# Problem Set 5

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================


def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

# ======================
# Part 1
# Data structure design
# ======================

# Problem 1


class NewsStory(object):
    """
    Class for NewsStory. Takes guid, title subject,
    summary and link as arguments.
    """
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link


# ======================
# Part 2
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5


# TODO: WordTrigger
class WordTrigger(Trigger):
    """docstring for WordTrigger"""
    def __init__(self, word):
        self.word = word

    def is_word_in(self, text):
        text = text.lower()
        for char in string.punctuation:
            text = text.replace(char, " ")
        word_list = text.split()
        return self.word .lower() in word_list


# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    """docstring for TitleTrigger"""
    def __init__(self, word):
        super(TitleTrigger, self).__init__(word)

    def evaluate(self, NewsStory):
        return self.is_word_in(NewsStory.get_title())


# TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):
    """docstring for SubjectTrigger"""
    def __init__(self, word):
        super(SubjectTrigger, self).__init__(word)

    def evaluate(self, NewsStory):
        return self.is_word_in(NewsStory.get_subject())


# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    """docstring for SummaryTrigger"""
    def __init__(self, word):
        super(SummaryTrigger, self).__init__(word)

    def evaluate(self, NewsStory):
        return self.is_word_in(NewsStory.get_summary())

# Composite Triggers
# Problems 6-8


# TODO: NotTrigger
class NotTrigger(Trigger):
    """docstring for NotTrigger"""
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, NewsStory):
        return not self.trigger.evaluate(NewsStory)


# TODO: AndTrigger
class AndTrigger(Trigger):
    """docstring for AndTrigger"""
    def __init__(self, triggerA, triggerB):
        self.triggerA = triggerA
        self.triggerB = triggerB

    def evaluate(self, NewsStory):
        return self.triggerA.evaluate(NewsStory) and self.triggerB.evaluate(NewsStory)


# TODO: OrTrigger
class OrTrigger(Trigger):
    """docstring for OrTrigger"""
    def __init__(self, triggerA, triggerB):
        self.triggerA = triggerA
        self.triggerB = triggerB

    def evaluate(self, NewsStory):
        return self.triggerA.evaluate(NewsStory) or self.triggerB.evaluate(NewsStory)

# Phrase Trigger
# Question 9


# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    """docstring for PhraseTrigger"""
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, NewsStory):
        phrase_in_subject = self.phrase in NewsStory.get_subject()
        phrase_in_title = self.phrase in NewsStory.get_title()
        phrase_in_summary = self.phrase in NewsStory.get_summary()
        return phrase_in_subject or phrase_in_summary or phrase_in_title


# ======================
# Part 3
# Filtering
# ======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering) 
    # Feel free to change this line!
    story_list = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                story_list.append(story)
    return story_list

# ======================
# Part 4
# User-Specified Triggers
# ======================


def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [line.rstrip() for line in triggerfile.readlines()]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    trigger_dict = {}
    trigger_list = []
    for line in lines:
        words = line.split()
        if words[0] != "ADD":
            title = words[0]
            type = words[1]
            arg = words[2]
            if type == 'TITLE':
                trigger_dict[title] = TitleTrigger(arg)
            elif type == 'SUBJECT':
                trigger_dict[title] = SubjectTrigger(arg)
            elif type == 'SUMMARY':
                trigger_dict[title] = SummaryTrigger(arg)
            elif type == 'NOT':
                trigger_dict[title] = NotTrigger(trigger_dict[arg])
            elif type == 'AND':
                trigger_dict[title] = AndTrigger(trigger_dict[arg], trigger_dict[words[3]])
            elif type == 'OR':
                trigger_dict[title] = OrTrigger(trigger_dict[arg], trigger_dict[words[3]])
            elif type == 'PHRASE':
                trigger_dict[title] = PhraseTrigger(" ".join(words[2:]))
        else:
            for triggers in words[1:]:
                trigger_list.append(trigger_dict[triggers])
    return trigger_list




def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60  # seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()
