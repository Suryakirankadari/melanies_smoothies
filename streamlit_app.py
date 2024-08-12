
import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
import requests

# Function to get the active Snowflake session
def get_active_session():
    connection_parameters = {
        "account": "DFWGPVI-YR76623",
        "user": "Suryakiran",
        "password": "248203@sK",
        "role": "SYSADMIN",
        "warehouse": "COMPUTE_WH",
        "database": "SMOOTHIES",
        "schema": "PUBLIC"
    }
    return Session.builder.configs(connection_parameters).create()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Text input for the name on the smoothie
name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

# Get the active Snowflake session
session = get_active_session()

# Fetch available fruit options from Snowflake
fruit_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
fruit_list = fruit_df['FRUIT_NAME'].tolist()

# Multiselect for choosing ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

if ingredients_list:
    # Join selected ingredients into a single string
    ingredients_string = ', '.join(ingredients_list)

    # Prepare the SQL insert statement
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)
    
    # Button to submit the order
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="👍")
        except Exception as e:
            st.error(f'Something went wrong: {e}')

# API request to Fruityvice
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

if fruityvice_response.status_code == 200:
    fruityvice_data = fruityvice_response.json()
    st.json(fruityvice_data)
else:
    st.error("Failed to fetch data from Fruityvice API.")
