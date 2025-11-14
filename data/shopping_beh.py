#%%
import streamlit as st
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
#%%

DATA_PATH = Path(__file__).parent / "DATA" / "shopping_behaviour.csv"
df = pd.read_csv(DATA_PATH, encoding="utf-8")

#df = pd.read_csv("shopping_behaviour.csv")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True )

st.title("Shopping behaviour analysis")
st.write("Zachowania zakupowe klientów w sklepie internetowym") 
st.text_input("Wpisz coś tutaj:")
@st.cache_data
def load_data():
    #data = pd.read_csv("shopping_behaviour.csv")
    return pd.read_csv(DATA_PATH, encoding="utf-8") #data 
#%%
#%%
st.set_page_config(layout="wide")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Data summary")
    st.write(df.describe()) 
with col2:
    st.subheader("Data types")
    dtypes_df = pd.DataFrame(df.dtypes, columns=["Data Type"])
    st.write(dtypes_df)
    
col3, = st.columns(1)
with col3:
    st.subheader("Missing values")
    missing_df = pd.DataFrame(df.isnull().sum(), columns=["Missing Values"])
    st.write(missing_df)
    
col8, col9 = st.columns(2)
with col8:
    st.subheader("Unique values per column")
    unique_counts = pd.DataFrame(df.nunique(), columns=["Unique Values"])
    st.write(unique_counts)
with col9:
    st.subheader("Columns preview")
    st.write(df.head())
#%%
st.subheader("Filter Data")
columns = df.columns.tolist()
selected_columns = st.selectbox("Select columns to filter", columns)
unique_values = df[selected_columns].unique()
selected_value = st.selectbox("Select value to filter", unique_values)
filtered_df = df[df[selected_columns] == selected_value]
st.write(filtered_df)

#%%
loc_col    = "Location" if "Location" in df.columns else None
season_col = "Season" if "Season" in df.columns else ("Seasons" if "Seasons" in df.columns else None)

view = filtered_df.copy() if 'filtered' in locals() else df.copy()

# dropdown: Lokalizacja
if loc_col:
    sel_loc = st.selectbox("Lokalizacja", ["(Wszystkie)"] + sorted(view[loc_col].dropna().unique()), key="loc_top")
    if sel_loc != "(Wszystkie)":
        view = view[view[loc_col] == sel_loc]

# dropdown: Sezon
if season_col:
    sel_seas = st.selectbox("Sezon", ["(Wszystkie)"] + sorted(view[season_col].dropna().unique()), key="seas_top")
    if sel_seas != "(Wszystkie)":
        view = view[view[season_col] == sel_seas]
    
col4, col5 = st.columns(2)
with col4:
    st.subheader("Age x Gender")
    fig = px.histogram(view, x="Age", color="Gender", barmode= "overlay", nbins=30, labels={"Age":"Wiek", "Gender": "Płeć"}, title="Age by Gender", hover_data=["Age"])
    st.plotly_chart(fig)
with col5:
    st.subheader("Purchase Status")
    purchase_counts = view['Item Purchased'].value_counts()
    fig2 = px.bar(y=purchase_counts.values, x=purchase_counts.index, title="Purchase Status Distribution", labels={"names":"Purchase Status", "values":"Count"})
    fig2.update_layout(xaxis_title="Item Purchased", yaxis_title="Amount of Purchase")

    st.plotly_chart(fig2)


#%%
col6, = st.columns(1)
with col6:
    table_color_gender= view.groupby(["Gender","Color"]).size().reset_index(name="count")
    fig3 = px.bar(table_color_gender, x="Color", y="count", color="Gender", barmode="group", labels={"Gender":"Płeć", "count":"Liczba", "Color":"Color"},title="Gender x Color")
st.plotly_chart(fig3)


# %%
col7, = st.columns(1)
with col7:
    table_subscription= view.groupby(["Subscription Status","Frequency of Purchases"]).size().reset_index(name="count")
    fig4 = px.bar(table_subscription, x="Subscription Status", y="count", color="Frequency of Purchases", barmode="group", labels={"Subscription":"Subskrypcja", "Frequency of Purchases":"Frequency of Purchases"},title="Subscription Status x Frequency of Purchases")
st.plotly_chart(fig4)

#%%
#st.write(list(view.columns))
#print(list(view.columns))
# %%
if "Purchase Amount (USD)" in view.columns:
    view["Purchase Amount (USD)"] = pd.to_numeric(view["Purchase Amount (USD)"], errors="coerce")

# %%
import plotly.express as px

#st.subheader("Top N najczęściej kupowanych produktów")
#n = st.number_input("N (produkty)", min_value=5, max_value=50, value=10, step=1, key="top_items_n")

#if "Item Purchased" in view.columns:
#    items = (view["Item Purchased"].dropna().value_counts().reset_index())
#    items.columns = ["Item Purchased", "Count"]
#    top_items = items.head(int(n))
#
#    st.dataframe(top_items)
#    fig = px.bar(top_items, x="Item Purchased", y="Count", title="Top produkty (liczba sztuk)")
#    fig.update_layout(xaxis=dict(categoryorder="total descending"))
#    fig.update_xaxes(tickangle=-45)
#    st.plotly_chart(fig)
#else:
#    st.info("Brak kolumny 'Item Purchased'.")
#%%
st.subheader("Top 10 najczęściej kupowanych produktów")

N_TOP = 10  # ustaw tu, jeśli chcesz inny
if "Item Purchased" in view.columns:
    items = view["Item Purchased"].dropna().value_counts().reset_index()
    items.columns = ["Item Purchased", "Count"]
    top_items = items.head(N_TOP)

    st.dataframe(top_items, use_container_width=True, hide_index=True)
else:
    st.info("Brak kolumny 'Item Purchased'.")


# %%
#st.subheader("Średnia kwota zakupu wg lokalizacji")

#if {"Location", "Purchase Amount (USD)"} <= set(view.columns):
#    avg_loc = (view.dropna(subset=["Purchase Amount (USD)", "Location"])
#                  .groupby("Location", as_index=False)["Purchase Amount (USD)"].mean()
#                  .rename(columns={"Purchase Amount (USD)": "Avg amount (USD)"})
#                  .sort_values("Avg amount (USD)", ascending=False))
#
#    st.dataframe(avg_loc)
#    fig = px.bar(avg_loc, x="Location", y="Avg amount (USD)", title="Średnia kwota (USD) wg lokalizacji")
#    fig.update_xaxes(tickangle=-45)
#    st.plotly_chart(fig)
#else:
#    st.info("Brak kolumn 'Location' i/lub 'Purchase Amount (USD)'.")

# %%
#st.subheader("Top N lokalizacji po wartości sprzedaży (USD)")
#n_loc = st.number_input("N (lokalizacje)", min_value=5, max_value=50, value=10, step=1, key="top_loc_n")
#
#if {"Location", "Purchase Amount (USD)"} <= set(view.columns):
#    sales_by_loc = (view.dropna(subset=["Purchase Amount (USD)", "Location"])
#                       .groupby("Location", as_index=False)["Purchase Amount (USD)"].sum()
#                       .rename(columns={"Purchase Amount (USD)": "Sales (USD)"})
#                       .sort_values("Sales (USD)", ascending=False))
#
#    top_loc = sales_by_loc.head(int(n_loc))
#
#    st.dataframe(top_loc)
#    fig2 = px.bar(top_loc, x="Location", y="Sales (USD)", title="Top lokalizacje wg wartości sprzedaży")
#    fig2.update_xaxes(tickangle=-45)
#    st.plotly_chart(fig2)
#else:
#    st.info("Brak kolumn 'Location' i/lub 'Purchase Amount (USD)'.")



# %%



