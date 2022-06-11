import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
from  PIL import Image
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html

global mydb
global data,bootstrap,logo
bootstrap="<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3' crossorigin='anonymous'>"
mydb = mydb = mysql.connector.connect(**st.secrets["mysql"])
st.set_page_config(page_title="MCA Dept Swarnandhra", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.markdown(bootstrap,unsafe_allow_html=True)
hide_streamlit_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.header("Swarnandhra MCA Department Daily Attendance")
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True




#########################################################


def form1():
    global batch
    global branch
    global courses
    global sem
    global attdate
    global period
    st.header("Student Daily Attendance")
    batch = st.selectbox(
        'select batch?',
        ('2020-2022', '2021-2023'))
    #st.write('You selected:', batch)
    branch = st.text_input(
        'select branch?',
        value='MCA',
        disabled=True)
    courses = st.text_input(
            'select courses?',
            value='MCA',
            disabled=True
            )
    
    if branch == 'MCA':
        sem = st.selectbox(
            'select Semester?',
            ('I-II',  'II-II'))
    
    attdate=st.date_input('Select Date:')
    #period=st.number_input('Select Period',value=7,min_value=1,max_value=7)
    period=st.selectbox(
        'select batch?',
        (1, 2,3,4,5,6,7))
    if sem == 'I-II':
        st.selectbox(
        'select batch?',
        ('Computer NetWorks', 'DWDM','OOPS Through Java','OOSE','NoSql'))
    if sem == 'II-II':
        st.selectbox(
        'select batch?',
        ('S/w Testing', 'Bigdata Analysis','Project'))
        

   
    
    


#https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb
    



def display_datagrid():
    global adf,new,data_list
    new=pd.DataFrame(columns=['batch','branch','courses','sem','attdate','period','regdno','attendance'])
    adf={'batch':[],'branch':[],'courses':[],'sem':[],'attdate':[],'period':[],'regdno':[],'attendance':[]}
    global selected_list
    selected_list=[]
    data_list=data.values.tolist()
    rcount=data.shape[0]
    for row in data_list:
        x=st.checkbox(row[1],value=True)
        selected_list.append(x)

    for c in range(0,rcount):
        adf['batch'].append(batch)
        adf['branch'].append(branch)
        adf['courses'].append(courses)
        adf['sem'].append(sem)
        adf['attdate'].append(attdate)
        adf['period'].append(period)
        adf['regdno'].append(data_list[c][1])
        adf['attendance'].append(selected_list[c])
    new = pd.DataFrame.from_dict(adf)
    totaldata=new.values.tolist()
    #st.write(totaldata)
    new.index = np.arange(1, len(new)+1)
    new.query("attendance == False",inplace=True)
    absentees=new["regdno"].to_list()
    st.dataframe(new)
    st.warning("Dear Parent today the following student(s) are absent for period:("+str(period)+")"+str(absentees))
    savedata=st.button("save Data")
    if savedata:
        mycursor = mydb.cursor()
        sql = "INSERT INTO attendance (batch, branch, courses, sem, attdate, period, regdno, attendance) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)"
        checksql="select count(*) from attendance where batch='"+str(batch)+"'and  branch='"+str(branch)+"' and courses='"+str(courses)+"' and sem='"+str(sem)+"' and attdate='"+str(attdate)+"' and period="+str(period)
        #st.write(checksql)
        mycursor.execute(checksql)
        (count,)=mycursor.fetchone()
        #st.write(count)
        if int(count) > 0 :
            st.success("This Attendance is already Saved")
        else:
            for val in totaldata:
                val = (val[0],val[1],val[2],val[3],val[4],val[5],val[6],val[7])
                mycursor.execute(sql, val)
            mydb.commit()
            st.success("Data Saved Succesfully")
    
        
        



def showconsolidated():
        batch = st.selectbox(
            'select batch?',
            ('2020-2022', '2021-2023'))
        #st.write('You selected:', batch)
        branch = st.text_input(
            'select branch?',
            value='MCA',
            disabled=True)
        courses = st.text_input(
                'select courses?',
                value='MCA',
                disabled=True
                )
        
        if branch == 'MCA':
            sem = st.selectbox(
                'select Semester?',
                ('I-II',  'II-II'))
        name=str(batch)+"_"+str(branch)+"_"+str(sem)
        qry="select * from attendance where batch='"+str(batch)+"'and  branch='"+str(branch)+"' and courses='"+str(courses)+"' and sem='"+str(sem)+"' and  period='"+str(7)+"'"
        #st.write(qry)
        sql_query=pd.read_sql(qry,mydb)
        tbl=pd.DataFrame(sql_query,columns=['id','batch','branch','courses','sem','attdate','period','regdno','attendance'])
        restbl=tbl.pivot(index='regdno',columns='attdate',values='attendance')
        #restbl1=tbl.pivot_table(index='regdno',columns='attendance',aggfunc='sum',margins=True,margins_name='Total')
        if not restbl.empty:
            restbl=restbl.astype(int)
            crestbl=restbl.cumsum(axis = 1)
            st.dataframe(crestbl)
            #restbl.index = np.arange(1, len(restbl)+1)
            csv = crestbl.to_csv().encode('utf-8')
            st.download_button("Press to Download", csv, name+"-consolidated.csv", "text/csv",  key='download-csv' )



if check_password():
        with st.sidebar:
            choose = option_menu("Rainfall Predition Project 1", ["Take Attendance", "Consolidated Report",  "Contact","Logout"],
                                icons=['house', 'bell',  'person lines fill','bell'],
                                menu_icon="award", default_index=0,
                                styles={
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#02ab21"},
            }
            )
        if choose == "Take Attendance":
            form1()
            if batch == '2021-2023' and branch == "MCA" and sem == "I-II":
                    data = st.cache(pd.read_csv)('MCA I yr.csv', nrows=100)
                    display_datagrid()
            if batch == '2020-2022' and branch == "MCA" and sem == "II-II":
                    data = st.cache(pd.read_csv)('MCA II yr.csv', nrows=100)
                    display_datagrid()
        if choose == "Consolidated Report":
            showconsolidated()
        if choose == "Contact":
                logo = Image.open(r'swrnlogo.png')
                col1, col2, col3 = st.columns(3)

                with col1:
                        st.write(' ')

                with col2:
                        st.image(logo)

                with col3:
                        st.write(' ')
                st.header("Contact Us:")
                st.success("MCA Department ,SWARNANDHRA College of Engineering and Technology,Seetharampuram, Narsapur, Andhra Pradesh 534280, India")
                st.info("Email : ramabhadrarao.maddu@swarnandhra.ac.in")
                st.success("Developer: Rama Bhadra Rao Maddu,Asst.Professor")
                st.warning("Phone: 9490730454 ")
        if choose == "Logout":
              del st.session_state['password_correct']  
              st.write("You are Logged Out..........")
              st.markdown("<a href='http://localhost:8501/' target='_self'>Click Here to Login Again</a>", unsafe_allow_html=True)  


