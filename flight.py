import pandas as pd
import streamlit as st
import pickle
import datetime
import sklearn

data = pd.read_csv("data.csv")
pipe = pickle.load(open("pipe.pkl", "rb"))

st.title("Flight Price Prediction")

r1col1, r1col2 = st.columns(2)
with r1col2:
    company = st.selectbox("Select Airline", [None] + sorted(data["airline"].apply(lambda e : e.replace("_", " ")).unique()))
with r1col1:
    date = st.date_input("Select Date of Departure", min_value = datetime.date.today())

r2col1, r2col2 = st.columns(2)
with r2col1:
    src = st.selectbox("Select Source City", [None] + sorted(data["source_city"].unique()))
with r2col2:
    dest = st.selectbox("Select Destination City", [None] + sorted(data["destination_city"][data["destination_city"] != src].unique()))

r3col1, r3col2 = st.columns(2)
with r3col1:
    dep = st.selectbox("Select Departure Time", [None] + sorted(data["departure_time"].apply(lambda e : e.replace("_", " ")).unique()))
with r3col2:
    arr = st.selectbox("Select Arrival Time", [None] + sorted(data["arrival_time"].apply(lambda e : e.replace("_", " ")).unique()))

r4col1, r4col2 = st.columns(2)
with r4col1:
    stops = st.selectbox("Select Number of Stops", [None] + sorted(data["stops"].apply(lambda e : e.replace("_", " ").capitalize()).unique()))
with r4col2:
    cls = st.selectbox("Select Class", [None] + sorted(data["class"].unique()))

if st.button("Predict Price", use_container_width = True):
    if date is None:
        st.warning("Please Select a Date")
    elif company is None:
        st.warning("Please Select Airline")
    elif src is None:
        st.warning("Please Select Source City")
    elif dest is None:
        st.warning("Please Select Destination City")
    elif dep is None:
        st.warning("Please Select Departure Time")
    elif arr is None:
        st.warning("Please Select Arrival Time")
    elif stops is None:
        st.warning("Please Select Number of Stops")
    elif cls is None:
        st.warning("Please Select Class")
    else:
        company = company.replace(" ", "_")
        date = date.strftime("%d-%m-%Y").replace("/", "-")
        dep = dep.replace(" ", "_")
        arr = arr.replace(" ", "_")
        stops = stops.replace(" ", "_").lower()

        d1 = datetime.date.today().strftime("%d-%m-%Y")

        date1 = datetime.datetime.strptime(d1, "%d-%m-%Y")
        date2 = datetime.datetime.strptime(date, "%d-%m-%Y")

        days = (date2 - date1).days
        prediction = pipe.predict(pd.DataFrame([[company, src, dep, stops, arr, dest, cls, days]],
                                  columns=['airline', 'source_city', 'departure_time', 'stops', 'arrival_time',
                                           'destination_city', 'class', 'days_left']))

        st.write(f"<h2><center><b>{'Predicted Price : ₹ ' + '{:,}'.format(int(prediction[0]))}</b></center></h2>", unsafe_allow_html = True)