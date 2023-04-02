import streamlit as st
from email.message import EmailMessage
import ssl
import smtplib
import pandas as pd

st.set_page_config(page_title="Email Sender", layout="wide")

st.markdown("# Email Sender")
st.write(
    """This website will allow you to send emails with ease!"""
)

choice = st.selectbox('Select which sender you would like to use',['Simple Sender','Mass Sender'])
if choice == 'Simple Sender':
    email_sender = st.text_input('On which email is this email being sent by?')
    email_password = st.text_input('What is your app password?')
    email_receiver = st.text_input('Which email is this going to?')
    subject = st.text_input('Insert Subject')
    body = st.text_input('Insert Body')
    send_mail = st.button('Send Email')
    if send_mail:
        em=EmailMessage()
        em['From']=email_sender
        em['To']=email_receiver
        em['subject']=subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())

elif choice == 'Mass Sender':
    email_sender = st.text_input('On which email is this email being sent by?')
    email_password = st.text_input('What is your app password?')
    uploaded_file = st.file_uploader('Insert CSV file of all the users you are sending the email to')
    st.write('Excel sheet **MUST** be formatted like the one shown below')
    df = pd.read_csv('mass-sender-example.csv')
    st.dataframe(df)
    subject = st.text_input('Insert Subject')
    opening = st.text_input('Insert Opening (example: "Dear", "Hello", etc.) ***OPTIONAL***')
    punct_opening = st.text_input('Insert Punctuation at the end of Opening')
    just_body = st.text_area('Insert Body')
    send_mail = st.button('Send Email')
    if send_mail:
        uploaded_csv = pd.read_csv(uploaded_file)
        for i in range(len(uploaded_csv)):
            cell_name = uploaded_csv.loc[i,"name"]
            body = opening + " " + cell_name + punct_opening + "\n" + just_body
            cell_email = uploaded_csv.loc[i, "email"]
            em=EmailMessage()
            em['From']=email_sender
            em['To']=cell_email
            em['subject']=subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(email_sender,email_password)
                smtp.sendmail(email_sender,cell_email,em.as_string())
