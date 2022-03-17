#!/usr/bin/env python
# coding: utf-8

# In[3]:


pip install looker_sdk


# In[12]:


import looker_sdk #Note that the pip install required a hyphen but the import is an underscore.

import os #We import os here in order to manage environment variables for the tutorial. You don't need to do this on a local system or anywhere you can more conveniently set environment variables.

import json #This is a handy library for doing JSON work.


# In[13]:


# Base URL for API. Do not include /api/* in the url
base_url = "https://trianz.looker.com:19999"
# API 3 client id below
client_id= "" 
# API 3 client secret below
client_secret= "" 
# Set to false if testing locally against self-signed certs. Otherwise leave True
verify_ssl=True


# In[14]:


os.environ["LOOKERSDK_BASE_URL"] = "https://trianz.looker.com:19999" #If your looker URL has .cloud in it (hosted on GCP), do not include :19999 (ie: https://your.cloud.looker.com).
os.environ["LOOKERSDK_API_VERSION"] = "3.1" #3.1 is the default version. You can change this to 4.0 if you want.
os.environ["LOOKERSDK_VERIFY_SSL"] = "true" #Defaults to true if not set. SSL verification should generally be on unless you have a real good reason not to use it. Valid options: true, y, t, yes, 1.
os.environ["LOOKERSDK_TIMEOUT"] = "120" #Seconds till request timeout. Standard default is 120.

#Get the following values from your Users page in the Admin panel of your Looker instance > Users > Your user > Edit API keys. If you know your user id, you can visit https://your.looker.com/admin/users/<your_user_id>/edit.
os.environ["LOOKERSDK_CLIENT_ID"] = "DDgqM4FK5fcrDp39mj7x"  #No defaults.
os.environ["LOOKERSDK_CLIENT_SECRET"] = "GsCngtmtKRrb6DrQBdbnHKxB" #No defaults. This should be protected at all costs. Please do not leave it sitting here, even if you don't share this document.

print("All environment variables set.")


# In[15]:


sdk = looker_sdk.init31()
print('Looker SDK 3.1 initialized successfully.')

#Uncomment out the lines below if you want to instead initialize the 4.0 SDK. It's that easy— Just replace init31 with init40.
#sdk = looker_sdk.init40()
#print('Looker SDK 4.0 initialized successfully.')


# In[16]:


my_user = sdk.me()

#Output is an instance of the User model, but can also be read like a python dict. This applies to all Looker API calls that return Models.
#Example: The following commands return identical output. Feel free to use whichever style is more comfortable for you.

print(my_user.first_name) #Model dot notation
print(my_user["first_name"]) #Dictionary


# In[17]:


#Enter your Look ID. If your URL is https://your.cloud.looker.com/looks/25, your Look ID is 25.
look_id = 256
look = sdk.look(look_id=look_id) 
# This gives us a Look object. We'll print the ID of it to verify everything's working.

print(look.id)

#You actually don't need to do anything further for this case, using a Look. 
#If you wanted to use an Explore instead, you'd have to get the underlying query first, which might look like this:

#explore_id = "Q4pXny1FEtuxMuj9Atf0Gg" 
#If your URL looks like https://your.cloud.looker.com/explore/ecommerce_data/order_items?qid=Q4pXny1FEtuxMuj9Atf0Gg&origin_space=15&toggle=vis, your explore_id/QID is Q4pXny1FEtuxMuj9Atf0Gg.
#explore_query = sdk.query_for_slug(slug=explore_id)

#This would return a Query object that we could then run to get results in step 2 using the run_query endpoints.


# In[18]:


#We'll use a try/except block here, to make debugging easier. 
#In general, this kind of thing isn't really necessary in notebooks as each cell is already isolated from the rest,
#but it's a good practice in larger scripts and certainly in applications where fatal errors can break the entire app.
#You should get into the habit of using them.

try:
  response = sdk.run_look(
    look_id=look.id,
    result_format= "json" # Options here are csv, json, json_detail, txt, html, md, xlsx, sql (returns the raw query), png, jpg. JSON is the easiest to work with in python, so we return it.
  )
  data = json.loads(response) #The response is just a string, so we have to use the json library to load it as a json dict.
  print(data) #If our query was successful we should see an array of rows.
except:
  raise Exception(f'Error running look {look.id}')


# In[19]:


#Before we move on, here's a simple example of that. Let's print the first 10 rows.
#This script is set up to always only look at the first column, assuming our Look returns 1 column.
first_field = list(
    data[0].keys()
    )[0] #This looks at the first row of the data and returns the first field name. keys() returns a set, so we wrap it in list() to return an array.
    
for i in range(0,10):
  print(i,data[i][first_field])

#If we _know_ the name of the first field, why did we go to all this list(data[0].keys()[0]) trouble? Well, we know the name of the first field for ONE look. 
#This little trickery above makes it so that our script will always work for any Look, no matter what the name is, without having to edit the code.


# In[59]:


def get_data_for_look(look_id):
  try:
    look = sdk.look(look_id=look_id)
  except:
    raise Exception(f'Look {look_id} not found.')
  print(f'Successfully got Look {look.id}')

  try:
    response = sdk.run_look(
        look_id=look.id,
        result_format = "csv"
    )
    data = json.loads(response)
    first_field = list(
      data[0].keys()
    )[0]
    list_of_values = []
    for i in data:
      list_of_values.append(i[first_field])
    #Ultimately, we're going to want to pass Looker a filter expression that's a comma-separated-list of values.
    #Here, we use .join on the array of values to generate that filter expression. 
    string_list = ",".join(list_of_values)
    return({"filter_values": string_list, "first_field": first_field}) 
  except:
    raise Exception('Error running Look.')


# In[60]:


test = get_data_for_look(256)
#This should return successful.


# In[20]:


#Start off the same as before, by getting the Look. 

second_look_id = 257
second_look = sdk.look(look_id=second_look_id)
print(second_look.id) #just verifying we obtained the Look properly.

#Now we can extract the underlying query from the second Look, in order to modify it. We'll print it to see what it looks like.
second_query = second_look.query
print(second_query)


# In[62]:


#We want to edit the filters, so let's start by inspecting the query and see how filters are set.
#We can see all the available keys in the query object by running the command below.
#👀 What are keys? Objects are key: value pairs. ex: {"name": "Izzy"}. The key is name, the value for that key is Izzy.

print(second_query.keys())


# In[63]:



#Looks like there's a filters key, so we can run the following to see the filters:
print("Filters: ", second_query.filters)


# In[64]:


response = sdk.run_query(query_id = second_query.id, result_format="csv")
print(response)


# In[65]:


#Let's create a new variable, altered_query, and assign it to be identical to second_query to begin.
altered_query = second_query 

#Then, let's set a new key on the filters dict, which adds a new filter to the query. We'll name it the name of the field we want to filter on.
#This must exactly match the **fully scoped** field name in Looker (ie: view_name.field_name).
#We will then set that key's value equal to our data. In this case, we'll set it equal to that comma-separated string we generated earlier.

filter_data = get_data_for_look(256) # This is that function we built earlier.
field_name = filter_data['first_field']
filter_values = filter_data['filter_values']

altered_query.filters[field_name] = filter_values

#This should now print an object with the filters you've just added. Nice!
print(altered_query.filters)


# In[70]:


#Before we can run this query, we need to do a little bit of pruning to it, since we copied it directly from an existing query.
#If you do not remove the ID and client_id, you'll get an error that this query already exists.
altered_query.client_id = None
altered_query.id = None


# In[71]:


#Option a. Run inline query. This is the simplest option for just getting the data now.
#This should return your newly filtered data from Look #2
response = sdk.run_inline_query(body=altered_query, result_format="json")
print(response)


# In[72]:


#Option b. Creating a brand new query object, then running that query from the ID.
#You might want to do this if you're planning to run the query asynchronously using create_query_task.
new_query = sdk.create_query(body=altered_query)
response = sdk.run_query(query_id=new_query.id, result_format="json")
print(response)


# In[73]:


#@title Look Filterer
#@markdown Enter a look ID (`first_look_id`) that returns one column of values you want to apply as filters to another Look (`second_look_id`).
#@markdown The first Look must return one column only. Once you've entered the look IDs, run this block.

#@markdown _👀  If you get an error, make sure you've run the earlier code blocks that initialize the Looker API and create the get_data_for_look() function._
first_look_id = 256 #@param {type:"integer"}
second_look_id =  257 #@param {type:"integer"}
final_result_format = "csv" #@param ["json", "json_detail", "csv", "png", "jpg", "txt", "html", "md"]


first_look = get_data_for_look(first_look_id)
filter_field = first_look['first_field']
filter_values = first_look['filter_values']
second_look = sdk.look(look_id=second_look_id)
second_query = second_look.query
altered_query = second_query
 
altered_query.filters[filter_field] = filter_values

altered_query.client_id = None
altered_query.id = None

response = sdk.run_inline_query(body=altered_query, result_format=final_result_format)

print(f"Results of look {second_look_id}  filtered with values from {first_look_id}:", response)

