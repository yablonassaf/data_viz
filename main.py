import streamlit as st
import pandas as pd
import plotly.express as px


def read_data():
    # url = 'https://drive.google.com/file/d/1NLDQQZdQ2yJo7_2YFL5ivC3Hz_r3MMxQ/view?usp=sharing'
    # url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
    # df_r = pd.read_csv(url)
    df_r = pd.read_csv("HKS_Diversity.csv")  # can also be read locally
    return df_r


def present_dataset():
    st.markdown("<h4 style='text-align: center; color: white;'>"
                "The Following Charts Provide Various Angles to Look at the Dataset  </h4>", unsafe_allow_html=True)

    st.markdown("<h5 style='text-align: center; color: grey;'>"
                "The data used to produce the visuals can be discovered by checking this box:  </h5>", unsafe_allow_html=True)

    global chart_data
    st.markdown('')
    if st.checkbox('Click to Show Data'):
        chart_data = pd.DataFrame(df)
        chart_data
    st.markdown('')


def show_headline():
    st.markdown(
        "<h1 style='text-align: center; color: white;'>DPI 852M: Advanced Data and Information Visualization</h1>",
        unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>Python Track - Final Project </h3>",
                unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: grey;'>Assaf Yablon </h5>", unsafe_allow_html=True)


def student_per_year_df(df_internal, program):
    temp_df = df_internal.groupby(['Year']).sum()
    if program != "All":
        temp_df = temp_df[[program]]
    temp_df["Students"] = temp_df.sum(axis=1)
    temp_df = temp_df.reset_index()
    temp_df["Year"] = ["2018", "2019", "2020", "2021"]
    temp_df = temp_df.set_index('Year')
    temp_df = temp_df["Students"]
    temp_df = pd.DataFrame(temp_df)
    df_internal = temp_df.reset_index()
    return df_internal


def add_line_chart_by_years():
    st.markdown('''---''')
    st.markdown("<h4 style='text-align: center; color: white;'>"
                "Let us examine the changes in programs through the years: </h4>", unsafe_allow_html=True)
    st.markdown('')
    df2 = df.groupby(['Year']).sum()
    df2["Year"] = ["2018", "2019", "2020", "2021"]
    df2 = df2.set_index('Year')
    chart_data = pd.DataFrame(df2)
    st.line_chart(chart_data)
    st.write('')
    st.markdown("<h5 style='text-align: center; color: grey;'>"
                "This visual provides a high-level perspective vis-a-vis the student count"
                " at the Harvard Kennedy School across the different programs. "
                "It can be seen that some programs have been expanded more than others. </h5>", unsafe_allow_html=True)
    st.markdown('''---''')

def show_video():
    st.video('https://www.youtube.com/watch?v=_VnBOY5SRfM&t=1s')
    st.markdown('''---''')


def show_bar_plot(main_df):
    st.markdown("<h4 style='text-align: center; color: white;'>"
                "Number of Students per Year at the Harvard Kennedy School  </h4>", unsafe_allow_html=True)
    st.markdown('')

    program = get_program()

    df_students = student_per_year_df(main_df, program)
    fig = px.bar(
        df_students,
        x="Year",
        y="Students",
        text="Students"
    )
    st.plotly_chart(fig)
    st.write("Number of students at the MPA2 program has nearly "
             "doubled between 2020-2021; see for yourself")
    st.markdown('''---''')


def get_program():
    programs_df = pd.DataFrame({
        'program': ["All", "MPP", "MPAID", "MPA2", "MCMPA"],
    })
    option = st.selectbox(
        'Choose Program to Explore:',
        programs_df['program'])
    'Program selected: ', option
    return option


def get_year_from_slide_bar():
    year_slide = st.slider('Select year:', 2018, 2021, 2018)
    st.write(year_slide, 'was chosen')
    return year_slide


def get_ethnicity_per_year(main_df):
    st.markdown('')
    st.markdown("<h4 style='text-align: center; color: white;'>"
                "Examine Harvard Kennedy School Ethnicity Diversity per Given Year  </h4>", unsafe_allow_html=True)
    year = get_year_from_slide_bar()
    yearly_df = main_df[main_df["Year"] == year]
    yearly_df = yearly_df.drop(columns="Year")
    yearly_df = yearly_df.groupby(['Race/Ethnicity']).sum()
    yearly_df = yearly_df.reset_index()
    yearly_df["Total_Students"] = yearly_df.sum(axis=1)
    yearly_df = yearly_df[["Race/Ethnicity", "Total_Students"]]

    fig = px.pie(yearly_df, values='Total_Students', names='Race/Ethnicity',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig)


def side_bar():
    from PIL import Image
    image = Image.open('hks_logo.png')
    st.sidebar.image(image, caption='Harvard Kennedy School')


def get_years_selection():
    y18 = st.checkbox('2018')
    y19 = st.checkbox('2019')
    y20 = st.checkbox('2020')
    y21 = st.checkbox('2021')

    years_list = []
    if y18: years_list.append(2018)
    if y19: years_list.append(2019)
    if y20: years_list.append(2020)
    if y21: years_list.append(2021)
    return years_list


def get_ethnicities():
    ethnicities = st.multiselect(
        'Select Ethnicities to Explore:',
        ['White', 'American Indian or Alaska Native', 'Asian', 'Black or African American', 'Hispanic/Latinx',
         'Native Hawaiian or Other Pacific Islander', 'Two or More Races', 'Unknown'],
        default=["White", "Black or African American"])
    st.write('You selected:', ethnicities)
    return ethnicities


def get_number_of_students_per_year(df_, race_, year_):
    yearly_df = df_[df_["Year"] == year_]
    yearly_df = yearly_df.drop(columns="Year")
    yearly_df = yearly_df.groupby(['Race/Ethnicity']).sum()
    yearly_df = yearly_df.reset_index()
    yearly_df["Total_Students"] = yearly_df.sum(axis=1)
    yearly_df = yearly_df[["Race/Ethnicity", "Total_Students"]]
    num = int(yearly_df[yearly_df["Race/Ethnicity"] == race_]["Total_Students"])
    return num


def get_race_df(races):
    years_list = [2018, 2019, 2020, 2021]
    dict_race_year = {}
    temp_list = []
    for race in races:
        for year in years_list:
            temp_list.append(get_number_of_students_per_year(df, race, year))
        dict_race_year[race] = temp_list
        temp_list = []
    df_race_year = pd.DataFrame(dict_race_year)
    df_race_year["Year"] = ["2018", "2019", "2020", "2021"]
    df_race_year = df_race_year.set_index('Year')
    return pd.DataFrame(df_race_year)


def present_area_chart():
    st.markdown('''---''')
    st.markdown('''''')
    races_list = get_ethnicities()
    df_race_year = get_race_df(races_list)
    st.area_chart(df_race_year)


# -----------------------------------#

side_bar()

df = read_data()

show_headline()

show_video()

present_dataset()

add_line_chart_by_years()

show_bar_plot(df)

get_ethnicity_per_year(df)

present_area_chart()
