import streamlit as st
import pickle
import plotly.graph_objects as go

st.title('Mumbai Air Quality Index Predictor')
# load the model
model = pickle.load(open('aqi_model.pkl','rb'))

def aqi_cat(aqi):
    if aqi < 50:
        return """
                Good
                Minimal Impact
                """
    elif aqi > 50:
        return """
                Satisfactory
                Minor breathing discomfort to sensitive people
                """
    elif aqi > 100:
        return """
                Moderate
                Breathing discomfort to the people with lungs, asthama and hear disease
                """
    elif aqi > 200:
        return """
                Poor
                Breathing discomfort to most people on prolonged exposure
                """
    elif aqi > 300:
        return """
                Very Poor
                Respiratory illness on prolonged exposure
                """
    else:
        return """
                Severe
                Affects healthy people and seriously impacts those with existing diseases
                """



st.subheader('Environmental factors')
PM25 = st.number_input("PM2.5",0,500)
PM10 = st.number_input("PM10",0,500,200)
NO2 = st.number_input("NO2",0,500,40)
SO2 = st.number_input("SO2",0,500,20)
CO = st.number_input("CO",0,100,1)
O3 = st.number_input("O3",0,500,50)

if st.button("Predict"):
    aqi = model.predict([[PM25,PM10,NO2,SO2,CO,O3]])
    st.metric("Predicted AQI",int(aqi))
    cat = aqi_cat(aqi)
    st.subheader("Impact")
    st.subheader(cat)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=int(aqi),
        title={'text':"AQI Gauge"},
        gauge={
            'axis':{'range':[0,500]},
            'bar': {'color':'#2F3E46'},
            'steps': [
                {'range':[0,50],'color':'#2ECC71'},
                {'range':[51,100],'color':'#F1C40F'},
                {'range':[101,200],'color':'#E67E22'},
                {'range':[201,300],'color':'#E74C3C'},
                {'range':[301,500],'color':'#8E44AD'}
            ]
        }
    ))
    st.plotly_chart(fig,use_container_width=True)