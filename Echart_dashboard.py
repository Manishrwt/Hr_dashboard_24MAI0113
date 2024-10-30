import streamlit as st
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie, Scatter
from streamlit.components.v1 import html

# Load the dataset using st.cache_data to cache the data and fix encoding
@st.cache_data
def load_data():
    try:
        # Fix encoding issue by using 'utf-8-sig'
        df = pd.read_csv('Hr_cleaned_dataset.csv', encoding='utf-8-sig')
        return df
    except FileNotFoundError:
        st.error("Dataset file not found. Please upload the file or check the path.")
        return pd.DataFrame()

df = load_data()

# Add the title for the dashboard
st.title("HR DASHBOARD BY MANISH")

# Sidebar for graph options
st.sidebar.title('Graph Options')

if not df.empty:
    # Select graph type
    graph_type = st.sidebar.selectbox('Select Graph Type', ['Bar', 'Pie', 'Line', 'Scatter', 'Area'])

    # Define relevant columns for the dataset based on graph type
    if graph_type == 'Bar':
        x_axis = st.sidebar.selectbox('Select X-Axis (Categorical)', ['Position', 'Department', 'State'])
        y_axis = st.sidebar.selectbox('Select Y-Axis (Numeric)', ['Salary', 'Absences', 'SpecialProjectsCount'])
    elif graph_type == 'Pie':
        x_axis = st.sidebar.selectbox('Select Category', ['Department', 'EmploymentStatus', 'Position'])
        y_axis = 'Count'
    elif graph_type == 'Line':
        x_axis = st.sidebar.selectbox('Select X-Axis (Categorical)', ['DateofHire', 'DateofTermination'])
        y_axis = st.sidebar.selectbox('Select Y-Axis (Numeric)', ['Salary', 'DaysLateLast30', 'SpecialProjectsCount'])
    elif graph_type == 'Scatter':
        x_axis = st.sidebar.selectbox('Select X-Axis (Numeric)', ['Salary', 'SpecialProjectsCount'])
        y_axis = st.sidebar.selectbox('Select Y-Axis (Numeric)', ['Absences', 'DaysLateLast30'])
    elif graph_type == 'Area':
        x_axis = st.sidebar.selectbox('Select X-Axis (Categorical)', ['DateofHire', 'DateofTermination'])
        y_axis = st.sidebar.selectbox('Select Y-Axis (Numeric)', ['Salary', 'SpecialProjectsCount'])

    # Create chart functions for different graph types
    def create_chart(x, y, chart_type):
        if chart_type == 'Bar':
            chart = (
                Bar()
                .add_xaxis(list(df[x]))
                .add_yaxis(y, list(df[y]))
                .set_global_opts(title_opts=opts.TitleOpts(title=f'{y} by {x}'))
            )
        elif chart_type == 'Pie':
            data = df[x].value_counts().reset_index()
            data.columns = [x, 'count']  # Rename the columns for clarity
            chart = (
                Pie()
                .add('', [list(z) for z in zip(data[x], data['count'])])
                .set_global_opts(title_opts=opts.TitleOpts(title=f'{x} Distribution'))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            )
        elif chart_type == 'Line':
            chart = (
                Line()
                .add_xaxis(list(df[x]))
                .add_yaxis(y, list(df[y]))
                .set_global_opts(title_opts=opts.TitleOpts(title=f'{y} by {x} Over Time'))
            )
        elif chart_type == 'Scatter':
            chart = (
                Scatter()
                .add_xaxis(list(df[x]))
                .add_yaxis(y, list(df[y]))
                .set_global_opts(title_opts=opts.TitleOpts(title=f'{y} vs {x} Scatter Plot'))
            )
        elif chart_type == 'Area':
            chart = (
                Line()
                .add_xaxis(list(df[x]))
                .add_yaxis(y, list(df[y]), areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
                .set_global_opts(title_opts=opts.TitleOpts(title=f'{y} by {x} Area Chart'))
            )
        return chart

    # Function to render pyecharts chart in Streamlit
    def render_chart(chart):
        # Using render_embed to convert the chart to embeddable HTML
        chart_html = chart.render_embed()
        # Displaying the HTML using Streamlit's html component
        html(chart_html, width=700, height=400)

    # Generate the chart and display it
    chart = create_chart(x_axis, y_axis, graph_type)
    render_chart(chart)

    # Optionally show the raw data
    if st.checkbox('Show raw data'):
        st.write(df)

# Add navigation buttons for Home, About, and Contact
st.sidebar.title('Navigation')
if st.sidebar.button('Home'):
    page = "Home"
elif st.sidebar.button('About Me'):
    page = "About"
elif st.sidebar.button('Contact Information'):
    page = "Contact"
else:
    page = "Graphs"  # Default to the graphs page if no button is clicked

if page == "Home":
    st.subheader("Welcome to the HR Dashboard")
    st.write("This dashboard provides insights into HR data through various visualizations.")

elif page == "About":
    st.subheader("About Me")
    st.write("**Name**: Manish Rawat")
    st.write("**Institution**: VIT Vellore")
    st.write("**Program**: M.Tech in AI & ML")
    st.write("**Registration Number**: 24MAI0113")

elif page == "Contact":
    st.subheader("Contact Information")
    st.write("For more information, please reach out via email or phone.")
    st.write("**Email**: manish2018rewa@gmail.com")
    st.write("**Phone**: 6263377546")
    st.markdown("""  
        **Social Media Links**:  
        [![YouTube](https://img.icons8.com/color/48/000000/youtube--v1.png)](https://www.youtube.com/@mnishrwat4314)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        [![Instagram](https://img.icons8.com/color/48/000000/instagram-new.png)](https://www.instagram.com/manish___rwt?igsh=ZjlpZmFqc2p1NmU4)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        [![LinkedIn](https://img.icons8.com/color/48/000000/linkedin.png)](https://linkedin.com)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        [![GitHub](https://img.icons8.com/color/48/000000/github--v1.png)](https://github.com/Manishrwt)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    """, unsafe_allow_html=True)
