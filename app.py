import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="StartUp Analysis")

df = pd.read_csv("startup_cleaned.csv")


def load_investor_details(investor):
    st.title(investor)
    #loading details about recent 5 investments
    last5_df = df[df["investors"].str.contains(investor)].head()[["date","startup","vertical","city","round","amount"]]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        #Displaying biggest investments
        big_series = df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        st.subheader("Biggest Investments")
        #st.dataframe(big_series)
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()
        st.subheader("Sector invested")
        #st.dataframe(big_series)
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        city_series = df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum()
        st.subheader("City invested")
        #st.dataframe(big_series)
        fig2, ax2 = plt.subplots()
        ax2.pie(city_series, labels=city_series.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    with col4:
        round_series = df[df["investors"].str.contains(investor)].groupby("round")["amount"].sum()
        st.subheader("Round in which invested")
        #st.dataframe(big_series)
        fig3, ax3 = plt.subplots()
        ax3.pie(round_series, labels=round_series.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    yoy = df[df["investors"].str.contains(investor)].groupby("date")["amount"].sum()
    st.subheader("Year on Year Investments")
    #st.dataframe(big_series)
    fig4, ax4 = plt.subplots()
    ax4.plot(yoy.index, yoy.values)
    plt.xticks(rotation=45)  #
    st.pyplot(fig4)


def general_analysis():
    st.title("Overall Analysis")
    total_amount = str(round(df["amount"].sum()))
    max_funding = str(round(df["amount"].max()))
    average_funding = str(round(df["amount"].mean()))
    total_startup = str(df["startup"].nunique())

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total investments", value= f"{total_amount} Cr")

    with col2:
        st.metric(label="Max Funding", value= f"{max_funding} Cr")

    with col3:
        st.metric(label="Average Funding", value= f"{average_funding} Cr")

    with col4:
        st.metric(label="Funded Startps", value= f"{total_startup}")    

    
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("Top Investors")
        top_series = df.groupby("investors")["amount"].max().sort_values(ascending=False)[0:5]
        figsize = (5, 5)
        fig5, ax5 = plt.subplots(figsize = figsize)
        ax5.pie(top_series, labels=top_series.index, autopct="%0.01f%%")
        st.pyplot(fig5)
    with col6:
       st.subheader("Top Cities")
       top_cities = df.groupby("city")["amount"].max().sort_values(ascending=False)[0:5]
       figsize = (5, 5)
       fig6, ax6 = plt.subplots(figsize = figsize)
       ax6.pie(top_cities, labels=top_cities.index, autopct="%0.01f%%")
       st.pyplot(fig6)

def startup_analysis(startup):
    startup_df = df[df["startup"].str.contains(startup)]
    amount = startup_df["amount"].values[0]
    if amount == 0:
        amount = "Undisclosed"
    else:
        amount = round(amount)
    st.markdown(
        f"""
## Startup Details 
#### City: {startup_df["city"].values[0]}
#### Investors: {startup_df["investors"].values[0]}
#### Round: {startup_df["round"].values[0]}
#### Amount Invested: {amount} Cr
"""
    )

st.sidebar.title("StartUp Funding Analysis")

option = st.sidebar.selectbox("Select One", ["Overall Analysis", "StartUp", "Investor"])

if option == "Overall Analysis":
    general_analysis()

elif option == "StartUp":
    st.title("StartUp")
    startup = st.sidebar.selectbox("Select Startup", df["startup"].unique().tolist())
    btn3 = st.sidebar.button("Find Startup Details")
    if btn3:
        startup_analysis(startup)
else:
    #st.title("Investor")
    selected_investor = st.sidebar.selectbox("Select Startup", sorted(set(df["investors"].str.split(",").sum())) )
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)
