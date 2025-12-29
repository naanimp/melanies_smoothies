# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie!:cup_with_straw")
st.write(
  """Choose the fruit  you want in your custom updates.
  """
)

ctx = st.connection("snowflake");
session = ctx.session()

# session = get_active_session()
df = session.table("smoothies.public.fruit_options").select("fruit_name")
# st.dataframe(data=df, use_container_width=True)

name_on_order = st.text_input("Name on smoothies");

st.write("Name on order Smoothie will be: ", name_on_order);

ingredient_list = st.multiselect(
    'Choose upto 5 ingradients', df, max_selections=5
)

if ingredient_list:
    ingredients_string  = ''
    
    for x in ingredient_list:
        ingredients_string += x + " "
    
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)
    
    time_to_insert = st.button("Submit order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.write("Your smoothies is ordered")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)
