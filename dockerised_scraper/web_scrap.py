import requests
from bs4 import BeautifulSoup
import traceback 
import pandas as pd
import datetime


#### db #######

#from db.create_db import schema_table_creation
#from db.import_data_into_db import import_data_to_db

def find_day_date_time_location(event_item):
    
    date_time = event_item.find('div', class_='cell xlarge-6 body-small')


    # Get the text content and strip leading/trailing whitespace
    text_content = date_time.get_text().strip()

    # Get the current year
    current_year = datetime.datetime.now().year

    # Split the text by '|' and take the first part to get the date and time
    date = text_content.split('|')[0].split(' ')

    # =======================================================
    # Find Day : Task = 0 achieved 
    day = date[-3]

    # =======================================================

    date_str = date[-2]


    # =======================================================

    # Find Date : Task = 1 achieved 
    new_date_str = f"{date_str.strip('.')}.{current_year}"

    # =======================================================

    # Find Time : Task = 2 achieved 
    time = text_content.split('|')[1].strip()

    # =======================================================

    # Find Location : Task = 3 achieved 
    location = text_content.split('|')[-1].strip()

    return(day, new_date_str, time, location)




def find_event_title_artist(event_item):

    # Goal is to find the Artists ==========================
    event_title_tag = event_item.find('p', class_='event-title h3')
    
    event_title_artist = event_title_tag.get_text().strip().split('|')
    #print(event_title_artist)


    # some titles do not have artist naem, so check if the length of the list is == 1, then only title is present, no artist's name is present
    # Go only if the length of the splitted list is > 1

    if len(event_title_artist) > 1 :
        artists = event_title_artist[1:]


        final_artist = []

        for artist in artists:
            final_artist.append(artist)


        # Find Artist : Task = 4 achieved 
        artist = "_".join(final_artist)
    
    # for some programs Artist's name is not mentioned
    else:
        artist = str(0)

    
     # Find Event Title : Task - 7 Achieved
    event_title = event_title_artist[0].strip()

    #print(artist)

    return(event_title,artist)




def find_image_link(event_item):

    # Find Image link : Task - 5 Achieved
    img_tag = event_item.find('source', media="(min-width: 1280px)")
    img_link = None
    if img_tag:
        srcset = img_tag.get('srcset')
        if srcset:
            img_link = srcset.split()[0]
        else:
            img_link = img_tag.get('src')
    
    return(img_link)





def find_works(event_item):
     # Goal is to find the works to be presented in the show,
    # on the current webpage there are total 27 shows, where "works" is not mentioned explicitly

    try:
        program_tag = event_item.find_all('div', class_='cell xlarge-6 body-small')[1]
        works = []

        content = program_tag.get_text().split('|')
        #print("content is ...",content[0])

        for i in range(len(content)):
            if i == 0:

                content_0 = content[0].split('\n')
                #print("content_0 is ...", content_0)
                
                if len(content_0) > 2:
                    content[i] = content_0[2]
                    works.append(content[i].strip())
                else:
                    works = str(0)
                    
                continue

            content[i] = content[i].strip()
            works.append(content[i])

        # Find works : Task - 6 Achieved
        works = "_".join(works)


    except Exception as e:
        
        tb = traceback.format_exc()  # returns the full stack trace as a string


        # Get the most recent traceback
        exc_type, exc_value, exc_tb = traceback.extract_tb(e.__traceback__)[-1]

        # Extract the  line number from the traceback, to see at which line, the error is generated from
        line_number = exc_tb.lineno
        
        print(f"the exception is ....{e}, at line number {line_number}")
        
        works = str(0)
    
    return(works)




def scarper_extract(url):
    
    # Send HTTP GET request
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all events
    event_items = soup.find_all('li', class_='event-item')

    return(transform(event_items))
    




def load_event_data(df):

    #  create database and schema if not already created
    #schema_table_creation()

    # finally load the data
    return(df)






def transform(event_items):


    # Extract information for each event (as a dictionary) and store into the Events list
    events = []



    for event_item in event_items:


        day, date, time, location = find_day_date_time_location(event_item)
        event_title,artist = find_event_title_artist(event_item)
        img_link = find_image_link(event_item)
        works = find_works(event_item)
       

        
        # make a dictionary and store all the info into it
        event_info = {
            'event_title': event_title,
            'artist': artist,
            'day': day,
            'date_string' : date,
            'time': time,
            'location' : location,
            'works': works,
            'image_link': img_link
        }
        

        # at every iteration, store the dictionary into the events list, which in future going to be converted to a DataFrame
        events.append(event_info)
    
    df = pd.DataFrame(events)



    # call the LOAD function

    return(load_event_data(df))