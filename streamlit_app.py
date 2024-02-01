import streamlit

streamlit.stop()

import pandas
import snowflake.connector

streamlit.title('My Parents New Healthy Dines')

streamlit.header('🍞 Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")
streamlit.multiselect("Pick some fruits: ", list(my_fruit_list. index), ["Avocado", "Strawberries"])

streamlit.dataframe(my_fruit_list)

streamlit.header('Fruityvice Fruit Advice!')

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")

# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

with streamlit.form("Add a fruit..."):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    my_data_row = my_cur.fetchall()
    streamlit.text("The fruit load contains:")
    streamlit.dataframe(my_data_row)
    
    newFruit  = streamlit.text_input("New fruit", value = "")
    addButton = streamlit.form_submit_button("Add")

    if addButton and newFruit is not None and newFruit != "":
        my_cur.execute(f"insert into pc_rivery_db.public.fruit_load_list values ('{newFruit}')")
        
