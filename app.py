import streamlit as st
import numpy as np
import pandas as pd
from utils import hdi

st.header('First name popularity by birth year, Ontario')

st.markdown("""
Using open data from the Ontario government [1-2], we can plot the popularity of first names given to
newborns over time. Since a name's popularity grows and fades over generations, we can ask: *given just a first name*, can we estimate the age
of the person? Often we can, and with high accuracy.
""")


@st.cache
def load_gendered_data():
    return pd.read_csv('data/by_gender.csv', index_col=0)

@st.cache(show_spinner=False)
def load_nongendered_data():
    df = pd.read_csv("data/total.csv", index_col=0)
    return df

@st.cache(show_spinner=False)
def load_survival():
    series = pd.read_csv("data/canadian_survival.csv").set_index('age')['survival']
    return series


#by_gender_df = load_gendered_data()
total_df = load_nongendered_data()
survival = load_survival()

name1 = st.sidebar.text_input("Enter first name:", value="Cameron", key="1").upper()
name2 = st.sidebar.text_input("Enter first name:", value="Barbara", key="2").upper()
name3 = st.sidebar.text_input("Enter first name:", value="Brittany", key="3").upper()
name4 = st.sidebar.text_input("Enter first name:", value="...", key="4").upper()
name5 = st.sidebar.text_input("Enter first name:", value="", key="5").upper()


names = [name for name in [name1, name2, name3, name4, name5] if name in total_df.columns]

st.line_chart(total_df[names], width=800, height=700)

st.subheader("Guessing ages using first names")

st.markdown("""
The popularity of some names spike very quickly, and the age range of people with that name may be very small. Below are
confidence intervals of the age of someone, given their first name¹.
""")

YEAR = 2019
PERCENT = st.slider("", min_value=20, max_value=95, value=50, step=5, format="%d%%")
for name in names:
    series = total_df[name].copy()
    series.index = pd.RangeIndex(106, 2, -1) # gross TODO.
    series = series.mul(survival)
    cdf = (series / series.sum()).cumsum()
    lower_bound, upper_bound = hdi(cdf, PERCENT/100.)
    st.markdown(f'⚬ There is a `{PERCENT}%` chance that someone named `{name.title()}` is between `{lower_bound}` and `{upper_bound}` years old.')


st.subheader("References")

st.markdown("""
1. Government and Consumer Services. (2012). Ontario top baby names (male) May 24, 2019.\nRetrieved from https://www.ontario.ca/data/ontario-top-baby-names-male
1. Government and Consumer Services. (2012). Ontario top baby names (female) May 24, 2019.\nRetrieved from https://www.ontario.ca/data/ontario-top-baby-names-female
2. Statistics Canada. Life tables, Canada, provinces and territories, catalogue no. 84-537-X.\nRetrieved from https://www150.statcan.gc.ca/n1/pub/91-209-x/2018001/article/54957-eng.htm
""")

st.subheader("Contact")

st.markdown("Cameron Davidson-Pilon, `cam.davidson.pilon@gmail.com`")




st.text("¹These statistics have been weighed by Canadian population survival rates[2]")