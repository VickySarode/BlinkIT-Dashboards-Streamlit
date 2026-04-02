import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Blinkit Sales Dashboard", layout="wide", page_icon="favicon.png")

#Title for dashboard
st.markdown(
    """
    <style>
        .title-blinkit {
        font-size: 42px;
        font-weight: 700;
        font-family: 'Segoe UI';
        color: black;
        margin-bottom: 25px;
        border-bottom: 2px solid #ffd200;
        padding-bottom: 8px;
        display: inline-block;
        }
    </style>
    <div class="title-blinkit">
        Blinkit Dashboard🛒
    </div>
    """,
    unsafe_allow_html=True
)

#Sidebar title
st.sidebar.markdown(
    """
    <style>
        .sb-title {
        font-size: 50px;
        font-weight: 900;
        font-family: 'Segoe UI', sans-serif;
        color: black;
        margin-bottom: 15px;
        text-align: center;
        }
        .sb-subtitle {
        font-size: 18px;
        font-weight: 500;
        color: black;
        margin-top: 1px;
        text-align: center;
        }
    </style>

    <div class="sb-title">
    blink<span style="color: #2A8E45;">it</span>
    </div>

    <div class="sb-subtitle">
    India's Last Minute App
    </div>

    """,
    unsafe_allow_html=True
)

#Sidebar styling
st.sidebar.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        background-color: #ffd200;
        border-radius: 30px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.20);
        }
    section[data-testid="stSidebar"] {
        color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# loading data
df = pd.read_csv("blinkit_data.csv")

# Reading DataFrame
#st.dataframe(df)

# Cleaning Data
df["Item Fat Content"] = df["Item Fat Content"].replace({
    "low fat": "Low Fat",
    "LF" : "Low Fat",
    "reg" : "Regular"
})

# Building KPI's
Total_Sales = df["Sales"].sum()
Average_Sales = df["Sales"].mean()
No_of_Items = df["Item Type"].nunique()
Average_rating = df["Rating"].mean()

st.markdown(
    """
<style>
    .card_grad{
        background: linear-gradient(140deg,#fbe165, #92a87e);
        padding: 20px;
        border-radius: 15px;
        color: Black;
        margin-top: 10px;
        font-weight: 700;
        width: 50%;
        border-left: 6px solid #058c00;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.15);
        }
    .card{
        background-color: #fff;
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        color: Black;
        font-weight: 700;
        width: 50%;
        border-left: 6px solid #058c00;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.15);
        }
    .value{
        font-size: 24px;
        }
    .label{
        font-size: 20px;
        color: black;
        margin-top: 5px;
        }
    .icon_curr{
        font-size: 25px;
        color: black;
        }
    icon{
        font-size: 25px;
        }
</style>
""", unsafe_allow_html=True
)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="card_grad">
    <div class= "value"><span class= "icon_curr">$</span>{Total_Sales/1e6:.2f}M</div>
    <div class= "label">TOTAL SALES</div>
    <img src = "margin.png" width = "20px>
    </div>
        """,unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="card">
    <div class= "value"><span class= "icon_curr">$</span>{Average_Sales:,.2f}</div>
    <div class= "label">AVERAGE SALES</div>
    
    </div>
        """,unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown(f"""
    <div class="card">
    <div class= "value">{No_of_Items}<span class= "icon">📦</span></div>
    <div class= "label">NUMBER OF ITEMS</div>
    
    </div>
        """,unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="card">
    <div class= "value">{Average_rating:.1f} <span class= "icon">⭐</span></div>
    <div class= "label">AVERAGE RATING</div>
    
    </div>
        """,unsafe_allow_html=True)
#Void space
st.markdown("""
<br/>
""", unsafe_allow_html=True)

#Sidebar filter panel
st.sidebar.subheader("🔍Filter panel ", text_alignment="center")

#Filter for data filtering
Outlet_location = st.sidebar.selectbox("Outlet Location Type : ", ["All"] + df["Outlet Location Type"].unique().tolist())
Outlet_Size = st.sidebar.selectbox("Outlet size : ", ["All"] + df["Outlet Size"].unique().tolist())
Item_Type = st.sidebar.selectbox("Item Type : ", ["All"] + df["Item Type"].unique().tolist())

filtered_df = df

if Outlet_location != "All":
    filtered_df = filtered_df[filtered_df["Outlet Location Type"] == Outlet_location]

if Outlet_Size != "All":
    filtered_df = filtered_df[filtered_df["Outlet Size"] == Outlet_Size]

if Item_Type != "All":
    filtered_df = filtered_df[filtered_df["Item Type"] == Item_Type]

col1, col2 = st.columns(2)

# Donut Chart with gca to add center circle and custom autopct to show sales in million dollars instead of percentage. Also added colors and text properties for better visualization.
with col1:
    st.subheader("Fat Content Distribution")

    fat_data = filtered_df.groupby("Item Fat Content")["Sales"].sum()

    plt.figure(figsize=(3, 3))

    plt.pie(
        fat_data, 
        labels=fat_data.index, 
        autopct= lambda p: f"${fat_data.sum() * p / 100 / 1e6:.2f}M", 
        colors=["#2A8E45", "#ffd200"],
        pctdistance=0.50,
        startangle=90,
        wedgeprops={"edgecolor": "black", "linewidth": 1},
        textprops = {"fontsize": 8}
        )
    
    center_circle = plt.Circle((0, 0), 0.70, fc="white")

    plt.gca().add_artist(center_circle)

    st.pyplot(plt)

with col2:
    st.subheader("Sales by Item Type")

    fig, ax1 = plt.subplots(figsize=(20, 30))

    Item_Type = filtered_df.groupby("Item Type")["Sales"].sum().sort_values(ascending=True)

    ax1.barh(Item_Type.index, Item_Type.values/1e6, color="#cda900")

    for i , v in enumerate(Item_Type.values / 1e6):
        ax1.text(v, i, f"{v:.2f}M", va="center", fontsize=20, fontweight="bold", color="black")
    
    for spine in ax1.spines.values():
        spine.set_visible(False)

    ax1.set_xlabel("Total Sales(In Millions)", fontsize=25, fontweight="bold")
    ax1.set_ylabel("Item Type", fontsize=25, fontweight="bold")
    ax1.tick_params(axis="y", labelsize=35)
    ax1.tick_params(axis="x", labelsize=30, rotation=60)
    plt.tight_layout()
    st.pyplot(fig)

oultet_fat = filtered_df.groupby(
    ['Outlet Location Type',
     'Item Fat Content'])['Sales'].sum().unstack()

x = np.arange(len(oultet_fat.index))
width = 0.35

col1, col2 = st.columns(2)
with col1:

    st.subheader("Fat Content Sales by Outlet Type")

    outlet_fat = (
    filtered_df
    .groupby(["Outlet Location Type", "Item Fat Content"])["Sales"]
    .sum()
    .unstack())

    x = np.arange(len(outlet_fat.index))
    width = 0.35

    fig2, ax2 = plt.subplots(figsize=(10, 6))

    
    for spine in ax2.spines.values():
        spine.set_visible(False)

    
    low_fat_color = "#2A8E45"
    regular_color = "#ffd200"

    
    bars1 = ax2.barh(x - width/2, outlet_fat["Low Fat"]/1e6, height=width, 
                color=low_fat_color, label="Low Fat")

    bars2 = ax2.barh(x + width/2, outlet_fat["Regular"]/1e6, height=width, 
                color=regular_color, label="Regular")

    # Labels on bars
    for i, v in enumerate(outlet_fat["Low Fat"]/1e6):
        ax2.text(v + 0.05, i - width/2, f"{v:.2f}M", va='center', fontsize=9)

    for i, v in enumerate(outlet_fat["Regular"]/1e6):
        ax2.text(v + 0.05, i + width/2, f"{v:.2f}M", va='center', fontsize=9)

    # Axis formatting
    ax2.set_yticks(x)
    ax2.set_yticklabels(outlet_fat.index, fontsize=10)
    ax2.set_xlabel("Sales (in Millions)", fontsize=11)

    # Grid (light)
    ax2.xaxis.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)

    # Legend
    ax2.legend(frameon=False)

    plt.tight_layout()
    st.pyplot(fig2)

with col2:
    st.subheader("Sales by Outlet Establishment Year")
    outlet_year = filtered_df.groupby("Outlet Establishment Year")["Sales"].sum().sort_index()

    fig3, ax3 = plt.subplots(figsize=(10, 6))

    ax3.plot(outlet_year.index, outlet_year.values/1e6, marker="o", color="#cda900", linewidth=2, markersize=8)
    for spine in ax3.spines.values():
        spine.set_visible(False)
    ax3.set_xlabel("Outlet Establishment Year", fontsize=11)
    ax3.set_ylabel("Total Sales (in Millions)", fontsize=11)
    ax3.set_title("Sales by Outlet Establishment Year", fontsize=14, weight='bold')
    ax3.xaxis.grid(True, linestyle='--', alpha=0.3)
    ax3.set_axisbelow(True)
    plt.tight_layout()
    st.pyplot(fig3)

st.subheader("Dashboard By Created By Vicky Sarode 👍")
