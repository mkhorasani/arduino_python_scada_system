import serial
import time
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

arduino = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS) #Change the COM port to whichever port your arduino is in
gauge_placeholder = st.empty()
chart_placeholder = st.empty()

def temp_gauge(temp,previous_temp,gauge_placeholder):

    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = temp,
        mode = "gauge+number+delta",
        title = {'text': "Temperature (°C)"},
        delta = {'reference': previous_temp},
        gauge = {'axis': {'range': [0, 40]}}))

    gauge_placeholder.write(fig)

def temp_chart(df,chart_placeholder):
    fig = px.line(df, x="Time", y="Temperature (°C)", title='Temperature vs. time')
    chart_placeholder.write(fig)

if arduino.isOpen() == False:
    arduino.open()

i = 0
previous_temp = 0
temp_record = pd.DataFrame(data=[],columns=['Time','Temperature (°C)'])

while i < 500:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    try:
        temp = round(float(arduino.readline().decode().strip('\r\n')),1)
    except:
        pass

    temp_record.loc[i,'Time'] = current_time
    temp_record.loc[i,'Temperature (°C)'] = temp

    temp_gauge(temp,previous_temp,gauge_placeholder)
    temp_chart(temp_record,chart_placeholder)
    time.sleep(1)
    i += 1
    previous_temp = temp

temp_record.to_csv('temperature_record.csv',index=False)

if arduino.isOpen() == True:
    arduino.close()
