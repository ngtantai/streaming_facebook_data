import facebook
import requests
import yaml
import os
import pandas as pd
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key


cred = yaml.load(open(os.path.expanduser('~/GalvanizeU/fb-creds.yml')))


access_token = cred['facebook']['fb_access_token']
user = cred['facebook']['fb_user_id']

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
feeds = graph.get_connections(profile['id'], 'feed')


#print(feeds['data'][0]['message'])
feed_list = []
for i,t in enumerate(feeds['data']):
    try:
        message = feeds['data'][i]['message']
        updated_time = feeds['data'][i]['updated_time']
    except:
        continue
    if message is not None and i < 10:
        feed_list.append((message, updated_time))
        print(message[:50] + "... ",updated_time)

# cast list to a dataframe
df = pd.DataFrame(feed_list)
df.columns = ['message', 'updated_time']
df_sorted = df.sort_values(by = 'updated_time', ascending=False)

#create top 10 feeds into html file
top10_df = df_sorted.reset_index(col_level=0, drop=True).head(10)
top10_df.to_html('top_10_feeds.html')

# # use boto to upload html and image files
# conn = S3Connection()
# mybucket = conn.get_bucket('b-01') # Substitute in your bucket name
#
# # html file from dataframe
# file_key = mybucket.new_key('top_10_feeds.html')
# file_key.content_type = 'text/html'
# file_key.set_contents_from_filename('top_10_feeds.html', policy='public-read')
