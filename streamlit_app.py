# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f"Customize Your Smoothie!:cup_with_straw")
st.write(
  """Choose the fruit  you want in your custom updates.
  """
)

ctx = st.connection("snowflake");
session = ctx.session()

# session = get_active_session()
df = session.table("smoothies.public.fruit_options").select("fruit_name", "search_on")
# st.dataframe(data=df, use_container_width=True)
pd_df = df.to_pandas();
#st.dataframe(pd_df)
#st.stop()


name_on_order = st.text_input("Name on smoothies");

st.write("Name on order Smoothie will be: ", name_on_order);

ingredient_list = st.multiselect(
    'Choose upto 5 ingradients', df, max_selections=5
)

if ingredient_list:
    ingredients_string  = ''
    
    for x in ingredient_list:
        ingredients_string += x + " "
        st.subheader(x + " Nutrician information")
        search_on = pd_df.loc[pd_df["FRUIT_NAME"] == x, 'SEARCH_ON'].iloc[0]
        st.write('Search value fruit chosen',  x ,  ' Search on ' , search_on)
      
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)
      
    
    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)
    
    time_to_insert = st.button("Submit order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.write("Your smoothies is ordered")



