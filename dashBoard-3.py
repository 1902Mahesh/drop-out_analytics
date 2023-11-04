# pip install streamlit-option-menu

import streamlit as st
import plotly.express as px
import plotly.graph_objects as px2
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
from streamlit_option_menu import option_menu #menu

st.set_page_config(page_title="Drop-out Analysis!!!", page_icon=":chart_with_upwards_trend:",layout="wide")

selected = option_menu(
    menu_title = None,
    options = [ "State", "Year"],
    icons = ["bank", "calendar"],
    menu_icon = "cast",
    default_index = 0,
    orientation = "horizontal",
    styles={
        "container": {"padding": "3rem 0 1rem 0!important"},
    }
)

cwd = os.getcwd()    

if selected == "Year":
    st.title(" :chart_with_upwards_trend: Drop-out Analysis")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style}', unsafe_allow_html=True)

    fl = st.file_uploader(":file_folder: Upload a file in this column format : (Primary Boy, Primary Girl, Primary Total, Upper Primary Boy, Upper Primary Girl, Upper primary Total, Secondary Boy, Secondary Girl, Secondary Total, Upper Seconday Boys, Upper Secondary Girl, Upper Secondary Total)", type=(["csv", "txt", "xlsx", "xls"]))
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename, encoding= "ISO-8859-1")
    else:
        os.chdir(cwd)
        df = pd.read_csv("Drop_out_data.csv", encoding= "ISO-8859-1")
        
    with st.expander("View Data"):
        # st.dataframe(df)
        st.write(df.style.background_gradient(cmap="Oranges"))
    

        
        
    # create for state
    st.sidebar.header("Choose your filter : ")
    state = st.sidebar.selectbox('Pick The State', df['State'].unique())
    st.write('Selected State', state)

    if not state:
        df2 = df.copy()
    else:
        df2 = df[df.State == state]
        
    # create for year
    year = st.sidebar.multiselect("Choose the year", df2["Year"].unique())
    if not year:
        df3 = df2.copy()
    else:
        df3 = df2[df2["Year"].isin(year)]

    state_wise_df = df3.groupby(by = ["Year"], as_index = False)["Total"].sum()


    st.subheader("Year wise analysis")
    fig = px.bar(state_wise_df, x = "Year", y = "Total", text = ['{:,.2f}'.format(x) for x in state_wise_df["Total"]], template = "seaborn")
    st.plotly_chart(fig, use_container_width=True, height = 200)  


    df3['Boys'] = df3['PB'] + df3['UPB'] + df3['SB'] + df3['USB']
    df3['Girl'] = df3['PG'] + df3['UPG'] + df3['SG'] + df3['USG']



    col1, col2 = st.columns((2))
    with col1:
        st.subheader("Gender Wise Analysis")
        fig = px.pie(df3, values=[df3["Boys"].sum(), df3["Girl"].sum()], names=["Boys", "Girl"], hole=0.5)
        # fig.update_traces(text = df3["Total"], textposition = "outside")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("School Level Wise Analysis")
        fig = px.pie(df3, values=[df3["PT"].sum(), df3["UPT"].sum(), df3["ST"].sum(), df3["UST"].sum()]
                    , names=["Primary", "Upper Primary", "Secondary", "Upper Secondary"], hole=0.5)
        # fig.update_traces(text = df3["Total"], textposition = "outside")
        st.plotly_chart(fig, use_container_width=True)
        
    
       
    fl1 = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]), key="2")
    if fl1 is not None:
        filename = fl1.name
        st.write(filename)
        reason_df = pd.read_csv(filename, encoding= "ISO-8859-1")
    else:
        os.chdir(cwd)
        reason_df = pd.read_csv("reason.csv", encoding= "ISO-8859-1")
        
    st.subheader("Droup-out reason") 
        
        
    colors = {'male' : "#0C3B5D", 'female' : "#3EC1CD"}
    fig2 = px.bar(reason_df, x = "Ratio", y = "reasons", color="Gender", barmode="group", orientation="h", color_discrete_map=colors)
    st.plotly_chart(fig2, use_container_width=True)


if selected == "State":

    st.title(" :chart_with_upwards_trend: Drop-out Analysis")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style}', unsafe_allow_html=True)

    fl = st.file_uploader(":file_folder: Upload a file in this column format : (Primary Boy, Primary Girl, Primary Total, Upper Primary Boy, Upper Primary Girl, Upper primary Total, Secondary Boy, Secondary Girl, Secondary Total, Upper Seconday Boys, Upper Secondary Girl, Upper Secondary Total)", type=(["csv", "txt", "xlsx", "xls"]), key="1")
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename, encoding= "ISO-8859-1")
    else:
        os.chdir(cwd)
        df = pd.read_csv("Drop_out_data.csv", encoding= "ISO-8859-1")
        

    with st.expander("View Data"):
        # st.dataframe(df)
        st.write(df.style.background_gradient(cmap="Oranges"))

        
        
    # create for Year
    st.sidebar.header("Choose your filter : ")
    year = st.sidebar.selectbox('Choose the Year', df['Year'].unique())
    st.write('Selected Year', year)

    if not year:
        df2 = df.copy()
    else:
        df2 = df[df.Year == year]
        
    # create for state
    state = st.sidebar.multiselect("Pick the state", df2["State"].unique())
    if not state:
        df3 = df2.copy()
    else:
        df3 = df2[df2["State"].isin(state)]

    year_wise_df = df3.groupby(by = ["State"], as_index = False)["Total"].sum()


    st.subheader("State wise analysis")
    fig = px.bar(year_wise_df, x = "State", y = "Total", text = ['{:,.2f}'.format(x) for x in year_wise_df["Total"]], template = "seaborn")
    st.plotly_chart(fig, use_container_width=True, height = 200)  


    df3['Boys'] = df3['PB'] + df3['UPB'] + df3['SB'] + df3['USB']
    df3['Girl'] = df3['PG'] + df3['UPG'] + df3['SG'] + df3['USG']



    col1, col2 = st.columns((2))
    with col1:
        st.subheader("Gender Wise analysis")
        fig = px.pie(df3, values=[df3["Boys"].sum(), df3["Girl"].sum()], names=["Boys", "Girl"], hole=0.5)
        # fig.update_traces(text = df3["Total"], textposition = "outside")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("School Level Wise analysis")
        fig = px.pie(df3, values=[df3["PT"].sum(), df3["UPT"].sum(), df3["ST"].sum(), df3["UST"].sum()]
                    , names=["Primary", "Upper Primary", "Secondary", "Upper Secondary"], hole=0.5)
        # fig.update_traces(text = df3["Total"], textposition = "outside")
        st.plotly_chart(fig, use_container_width=True)
    
    fl1 = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]), key="2")
    if fl1 is not None:
        filename = fl1.name
        st.write(filename)
        reason_df = pd.read_csv(filename, encoding= "ISO-88-1")
    else:
        os.chdir(cwd)
        reason_df = pd.read_csv("reason.csv", encoding= "ISO-8859-1")
    
    st.subheader("Droup-out reason")   
    colors = {'male' : "#0C3B5D", 'female' : "#3EC1CD"}
    fig2 = px.bar(reason_df, x = "Ratio", y = "reasons", color="Gender", barmode="group", orientation="h", color_discrete_map=colors)
    st.plotly_chart(fig2, use_container_width=True)

        
    
        
