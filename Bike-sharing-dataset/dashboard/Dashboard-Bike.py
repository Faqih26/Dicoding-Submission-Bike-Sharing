import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path


def holiday(df):
    holiday_day_data = df.groupby(by="holiday").instant.nunique().reset_index()
    holiday_day_data.rename(columns={ "instant": "sum"}, inplace=True)
    return holiday_day_data

def hrdd(df):
    hrd  = df[df['holiday']=='Holiday']
    return hrd

def seasond(df):
    season_data = df.groupby(by="season").instant.nunique().reset_index()
    season_data.rename(columns={"instant": "sum"}, inplace=True)
    
    return season_data

def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    with st.sidebar:

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )

    return date

# load dataset
day_bike = pd.read_csv("cleandataday.csv")
hour_bike = pd.read_csv("cleanhourdata.csv")

date = sidebar(day_bike)
if len(date) == 2:
    main_df = day_bike[(day_bike["dteday"] >= str(date[0])) & (day_bike["dteday"] <= str(date[1]))]
    h_df = hour_bike[(hour_bike["dteday"] >= str(date[0])) & (hour_bike["dteday"] <= str(date[1]))]
else:
    main_df = day_bike[ (day_bike["dteday"] >= str(st.session_state.date[0])) & (day_bike["dteday"] <= str(st.session_state.date[1]))]
    h_df = hour_bike[ (hour_bike["dteday"] >= str(st.session_state.date[0])) & (hour_bike["dteday"] <= str(st.session_state.date[1]))]

holiday = holiday(main_df)
hrdd = hrdd(h_df)
seasond = seasond(h_df)

# pengaruh hari kerja mempengeruhi pengunaan bike sharing
st.header("Bike Share Monitoring Dashboard :")
st.subheader("Workday")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="sum",
    x="holiday",
    data=holiday.sort_values(by="holiday", ascending=False),
    ax=ax
)
ax.set_title("Number of Bicycles on Workdays", loc="center", fontsize=50)
ax.set_ylabel("Number of Users")
ax.tick_params(axis="x", labelsize=30)
ax.tick_params(axis="y", labelsize=20)
st.pyplot(fig)

#working holiday
st.subheader("Hour Day")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="cnt",
    x="hr",
    data=hrdd.sort_values(by="hr", ascending=False),
)
ax.set_title("Number of Bike Sharing by Hour", loc="center", fontsize=50)
ax.set_ylabel("Number of Users")
ax.tick_params(axis="x", labelsize=30)
ax.tick_params(axis="y", labelsize=20)
st.pyplot(fig)

#time of day
st.subheader("Time Of Day")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="cnt",
    x="time_of_day",
    data=hrdd.sort_values(by="time_of_day", ascending=False),
)
ax.set_title("Number of Bike Sharing by Time Of Day", loc="center", fontsize=50)
ax.set_ylabel("Number of Users")
ax.tick_params(axis="x", labelsize=30)
ax.tick_params(axis="y", labelsize=20)
st.pyplot(fig)

st.subheader("Season")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="sum",
    x="season",
    data=seasond.sort_values(by="season", ascending=False),
)
ax.set_title("Number of Bike Sharing by Season", loc="center", fontsize=50)
ax.set_ylabel("Number of Users")
ax.tick_params(axis="x", labelsize=30)
ax.tick_params(axis="y", labelsize=20)
st.pyplot(fig)

if __name__ == "__main__":
    copyright = "Copyright © " + "2023 | Bike Sharing Dashboard | All Rights Reserved | " + "Made by: [@FaqihSuryana](https://www.linkedin.com/in/faqihsuryana/)"
    st.caption(copyright)
