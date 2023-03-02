import os
import streamlit as st
import plotly.graph_objs as go
import looker_sdk
import json
from PIL import Image
from plotly.subplots import make_subplots
from datetime import datetime

# Load logo image
logo = Image.open("logo.png").resize((100, 100))

# Set page configuration with logo in top left corner
st.set_page_config(page_title='My Little App', page_icon=logo, layout='wide')

# Display logo in left sidebar
st.sidebar.image(logo)

# Set Looker SDK environment variables
os.environ["LOOKERSDK_BASE_URL"] = "https://xxx.eu.looker.com/"
os.environ["LOOKERSDK_API_VERSION"] = "4.0"
os.environ["LOOKERSDK_VERIFY_SSL"] = "true"
os.environ["LOOKERSDK_TIMEOUT"] = "120"
os.environ["LOOKERSDK_CLIENT_ID"] = "xxx"
os.environ["LOOKERSDK_CLIENT_SECRET"] = "xxx"

# Authenticate with Looker API
sdk = looker_sdk.init31()

# Define Looker query function
@st.cache_data(ttl=3600) # cache data for 1 hour
def get_look_data():
    response = sdk.run_query(
        query_id="6219",
        result_format="json"
    )
    data = json.loads(response)
    result = []
    for row in data:
        result.append({
            'date': row['order_items.created_date'],
            'count': row['order_items.count'],
            'total_sale_price': row['order_items.total_sale_price'],
            'avg_sale_price': row['order_items.avg_sale_price'],
        })
    return result

# Get Looker data
result = get_look_data()

# Get the minimum and maximum dates in the data
min_date = datetime.strptime(result[0]['date'], '%Y-%m-%d')
max_date = datetime.strptime(result[-1]['date'], '%Y-%m-%d')

# Set default value for slider to the first and last dates in the result
start_time = st.sidebar.slider(
    "Date picker",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date],
    format="MM/DD/YY"
)

# Filter data based on slider value
filtered_data = [row for row in result if datetime.strptime(row['date'], '%Y-%m-%d') >= start_time[0] and datetime.strptime(row['date'], '%Y-%m-%d') <= start_time[1]]

# Create plotly figure for total sale price and count of order items
fig1 = go.Figure()
fig1.update_layout(height=300, width=400)
fig1.add_trace(go.Scatter(x=[row['date'] for row in filtered_data], y=[row['total_sale_price'] for row in filtered_data], fill='tozeroy', fillcolor='rgba(255, 0, 0, 0.5)', name='Total Sale Price'))
fig1.update_layout(title='Total Sale Price', xaxis_title='Date', yaxis_title="Total Sale Price")

fig2 = go.Figure()
fig2.update_layout(height=300, width=400)
fig2.add_trace(go.Scatter(x=[row['date'] for row in filtered_data], y=[row['count'] for row in filtered_data], fill='tozeroy', fillcolor='rgba(255, 0, 0, 0.5)', name='Count of Order Items'))
fig2.update_layout(title='Count of Order Items', xaxis_title='Date', yaxis_title="Count of Order Items")

# Create plotly figure for sum of sales
sales_sum = sum([row['total_sale_price'] for row in filtered_data])
fig3 = go.Figure()
fig3.update_layout(height=200, width=400)
fig3.add_trace(go.Indicator(
    mode = "number",
    value = sales_sum,
    number={'prefix': "$",},
    title = {"text": "Total Sales"}
))
fig3.update_layout(title='Sales Metrics')

# Create plotly figure for sum of count of orders
orders_sum = sum([row['count'] for row in filtered_data])
fig4 = go.Figure()
fig4.update_layout(height=200, width=400)
fig4.add_trace(go.Indicator(
    mode = "number",
    value = orders_sum,
    title = {"text": "Total Orders"}
))
fig4.update_layout(title='Orders Metrics')

# Define Looker query function for order items by status
def get_order_status_data():
    response = sdk.run_query(
        query_id="6253",
        result_format="json"
    )
    data = json.loads(response)
    result = {}
    for row in data:
        status = row['order_items.status']
        date = datetime.strptime(row['order_items.created_date'], '%Y-%m-%d')
        count = row['order_items.count']
        if date >= start_time[0] and date <= start_time[1]:
            result[status] = result.get(status, 0) + count
    return result

# Get Looker data
order_status_data = get_order_status_data()

# Create plotly figure for order items by status
labels = list(order_status_data.keys())
values = list(order_status_data.values())
fig5 = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig5.update_traces(hole=.4, hoverinfo="label+percent+name")
fig5.update_layout(title='Order Items by Status')

# Display plotly figures side by side in Streamlit app
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(fig3, use_container_width=True)
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig4, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
with col3:
    st.plotly_chart(fig5, use_container_width=True)
