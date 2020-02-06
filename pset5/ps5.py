# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Ujjwal Tamhankar
# Collaborators: None
# Time: ~20hrs

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz

# Helper function for problem 2 that "cleans up" the phrase.
def phrase_cleaner(phrase):
    '''Returns a "cleaned up" version of the phrase that is inputed.
       Removes extra spaces and special characters.
    '''
    phrase = phrase.lower()  
    for i in range(0, len(phrase)):
        # If the phrase contains a special character, replace the special character with a space.
        for element in string.punctuation:
            if phrase[i] == element:
                phrase = phrase.replace(element, ' ')
    # Turn the phrase with special characters removed into a list of words.
    phrase_split = phrase.split()

    # Join the phrase list backtogether with a space in between the words.
    return ' '.join(phrase_split)  

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

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
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# Create a NewsStory class.
class NewsStory():
    
    # NewsStory constructor that takes in the NewsStory's guide, title, description, link, and date
    # of publication.
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    # getter() methods that allow one to safely access the attributes fo the NewsStory.
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):

    # Constructor for the phrase trigger. Makes sure that the phrase's case is switched to lower.
    def __init__(self, phrase):
        self.phrase = phrase.lower()
    
    # Function to check if the phrase in 'text' is in the PhraseTrigger object. Utilizes the 
    # phrase_cleaner() helper function.
    def is_phrase_in(self, text):
        text_cleaned = phrase_cleaner(text)
        
        # First, check to see if the phrase itself in string form is in the PhraseTrigger object.
        if self.phrase in text_cleaned:
            
            # If the phrase is, check and see if the individual words that are in the text are also 
            # in the PhraseTrigger object, in the correct order.
            text_cleaned_list = phrase_cleaner(text).split()

            # Check if every element in self.phrase.split is in text_cleaned_list
            if all(item in text_cleaned_list for item in self.phrase.split()):
                for i in range(0, len(self.phrase.split())-1):
                    if text_cleaned_list.index(self.phrase.split()[i-1]) > text_cleaned_list.index(
                        self.phrase.split()[i+1]):
                        return False
                    else: 
                        return True
            else:
                return False
        else:
            return False

# TitleTrigger inherits __init__ from PhraseTrigger.
class TitleTrigger(PhraseTrigger):

    # Evaluate function checks and sees if the the NewsStory title contains the phrase in question.
    def evaluate(self, NewsStory):
        return self.is_phrase_in(NewsStory.get_title())

# Problem 4
# DescriptionTrigger inherits __init__ from PhraseTrigger.
class DescriptionTrigger(PhraseTrigger):

    # Evaluate function checks if the description for NewsStory contains the phrase in question.
    def evaluate(self, NewsStory):
        return self.is_phrase_in(NewsStory.get_description())

# TIME TRIGGERS
# Problem 5
class TimeTrigger(Trigger):
    
# Constructor:
#   Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#   Convert time from string to a datetime before saving it as an attribute.
    def __init__(self, time):
        self.time = datetime.strptime(time, '%d %b %Y %X')

# Problem 6
# BeforeTrigger inherits __init__ from TimeTrigger.
class BeforeTrigger(TimeTrigger):

    # Evaluate checks if the time value inputted is before the publication date of the NewsStory.
    def evaluate(self, NewsStory):
        newsstory_date_cleaned = NewsStory.get_pubdate().replace(tzinfo = None)
        return self.time > newsstory_date_cleaned

# AfterTrigger inherits __init__ from TimeTrigger.
class AfterTrigger(TimeTrigger):

    # Evaluate function checks if the time value inputted is after the publication date of the 
    # NewsStory.
    def evaluate(self, NewsStory):
        newsstory_date_cleaned = NewsStory.get_pubdate().replace(tzinfo = None)
        return self.time < newsstory_date_cleaned

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):

    def __init__(self, Trigger):
        self.Trigger = Trigger

    # Evaluate checks if the phrase in question is NOT in the Trigger.
    def evaluate(self, x):
        T = self.Trigger
        return not T.evaluate(x)

# Problem 8
class AndTrigger(Trigger):
    # Trigger that checks if two Triggers are satisfied.
    
    def __init__(self, Trigger1, Trigger2):
        self.Trigger1 = Trigger1
        self.Trigger2 = Trigger2

    # Evaluate checks if two triggers have fired and fires only if both have.    
    def evaluate(self, x):
        T1 = self.Trigger1
        T2 = self.Trigger2
        return T1.evaluate(x) and T2.evaluate(x)

# Problem 9
class OrTrigger(Trigger):
    # Trigger that checks two triggers and fires if either trigger has fired.

    def __init__(self, Trigger1, Trigger2):
        self.Trigger1 = Trigger1
        self.Trigger2 = Trigger2

    # Evaluate checks if two triggers have fired and fires only if either have fired.
    def evaluate(self, x):
        T1 = self.Trigger1
        T2 = self.Trigger2
        return T1.evaluate(x) or T2.evaluate(x)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    #TODO: Problem 10
    triggered_stories = []
    for i in range(0, len(stories)):
        for t in range(0, len(triggerlist)):
            
            # Checks the evaluate method for each item in triggerlist and returns a nonfalse value 
            # (the way the code is structured, the value returned is not always True if the story 
            # does set off a trigger, hence the !=False instead of True)
            if  triggerlist[t].evaluate(stories[i]) != False:

                # Append to the triggered_stories list, everytime a story sets off a trigger.
                triggered_stories.append(stories[i])
    
    return triggered_stories

#======================
# User-Specified Triggers
#======================
# Problem 11

# Helper funtion to convert lines read in from the triggers.txt file and parses them into 
# an outputted python dictionary with the keys equal to the trigger numbers and the values
# equal to a list of the arguments to form that particular trigger object.
def dict_parser(lines):
    lines_dict = {}
    for i in range(0, len(lines)):
        lines_list = lines[i].split(',')
        lines_dict[lines_list[0]] = lines_list[1:len(lines_list)]
    return lines_dict

def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers.

    # Create dictionary of keywords and types of trigger objects.
    keywords = {'TITLE':TitleTrigger , 'DESCRIPTION':DescriptionTrigger, 'AFTER':AfterTrigger, 
            'BEFORE': BeforeTrigger, 'NOT': NotTrigger, 'AND':AndTrigger, 'OR':OrTrigger}
    
    # With the dict_parses helper function, create a dictionary of the inputted triggers read from 
    # the triggers.txt file.
    lines_dict = dict_parser(lines)
    triggers_list = []

    # Iterate over the helper dictionary created.
    for element in lines_dict.keys():

        # Look for the dict key 'ADD'.
        if element == 'ADD':

            # If the add keyword is found, iterate through the cooresponding value list of the 
            # 'ADD' keyword in lines_dict and create a list of Trigger objects 
            # (located from the keywords dict) with approprately passed in values according to 
            # those of the trigger items' values in lines_dict.
            for i in lines_dict['ADD']:

                # If the corresponding entry is a composite And or Or trigger, iterate through the 
                # values of the AND and OR keyword list and compose the AND/OR trigger objects.
                if lines_dict[i][0] == 'AND' or lines_dict[i][0] == 'OR':
                    triggers_list.append(keywords[lines_dict[i][0]](
                        keywords[lines_dict[lines_dict[i][1]][0]](
                            lines_dict[lines_dict[i][1]][1]),
                        keywords[lines_dict[lines_dict[i][2]][0]](
                            lines_dict[lines_dict[i][2]][1])))
                else:
                    triggers_list.append(keywords[lines_dict[i][0]](lines_dict[i][1]))
                    
        else:
            pass
    return triggers_list

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers_impeachment.txt')
          
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
      print(e)

if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

