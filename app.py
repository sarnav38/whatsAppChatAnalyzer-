import matplotlib.pyplot as plt
import streamlit as st
import txt2df, usefulFuns
import seaborn as sns
import plotly.express as px
from PIL import Image

img = Image.open('./favicon/favicon.ico')
st.set_page_config(page_title='WhatApp Analyzer', page_icon=img)

with open('./css/style.css') as f:
    a = f.read()

st.markdown(f'<style>{a}</style>', unsafe_allow_html=True)

with st.sidebar:
    st.title('WhatApp Chat Analyizer')
    uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = txt2df.txt2df(data)
    # st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    with st.sidebar:
        selected_user = st.selectbox('Show Analysis wrt: ', user_list)
        total_message, total_words, total_media, total_urls = usefulFuns.fetch_user(selected_user, df)
        btn1 = st.button('Show Analysis')


    if btn1:

        # TODO 1 Top Statistics
        st.header(':red[Top Statistics]')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader(':violet[Total Messages]')
            st.title(total_message)
        with col2:
            st.subheader(':violet[Total Words]')
            st.title(total_words)
        with col3:
            st.subheader(':violet[Total Media]')
            st.title(total_media)
        with col4:
            st.subheader(':violet[Total Links]')
            st.title(total_urls)

        # TODO 2 Monthly Timeline
        st.header(':red[Monthly Timeline]')
        mnth_tmln = usefulFuns.monthly_timeline(selected_user, df)
        fig_mnth_tmln = px.line(data_frame=mnth_tmln, x='monthname-year', y='message', line_dash='year', color='year',
                                markers=True)
        st.plotly_chart(fig_mnth_tmln)

        # # TODO 3 Daily Timeline
        st.header(':red[Daily Timeline]')
        dail_tml = usefulFuns.daily_timeline(selected_user, df)
        fig_dail_tml = px.line(data_frame=dail_tml, x='date', y='message', markers=True)
        st.plotly_chart(fig_dail_tml)

        # TODO 4 Activity Map
        st.header(':red[Activity Map]')
        colm1, colm2 = st.columns(2)
        with colm1:
            st.subheader(':violet[Most Busy Day]')
            m_b_d = usefulFuns.most_busy_day(selected_user, df)
            fig_m_b_d = px.bar(data_frame=m_b_d, x='index', y='dayname', color='dayname')
            st.plotly_chart(fig_m_b_d)
        with colm2:
            st.subheader(':violet[Most Busy Month]')
            m_b_m = usefulFuns.most_busy_month(selected_user, df)
            fig_m_b_m = px.bar(data_frame=m_b_m, x='index', y='monthname', color='monthname')
            st.plotly_chart(fig_m_b_d)

        # TODO 4 Weekly Activity Map
        try:
            st.header(':red[Weekly Activity Map]')
            pv = usefulFuns.week_Act(selected_user, df)
            fig, ax = plt.subplots()
            # noinspection PyRedeclaration
            ax = sns.heatmap(pv)
            st.pyplot(fig)
        except Exception as e:
            print(e)
            st.title('cannot fetch heatmap')


        # TODO 7 Top Most Busy User
        if selected_user == 'Overall':
            st.subheader(':red[Most Busy User]')
            # fig, ax = plt.subplots()
            x, y = usefulFuns.most_Busy_user(df)
            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(data_frame=x, x='Top 5 User', y='No of Messages', color='No of Messages')
                st.plotly_chart(fig)
                # ax.bar(x.index, x.values, color='#FF56A8')
                # plt.xticks(rotation='vertical')
                # plt.xlabel('Top 5 Busy User')
                # plt.ylabel('Number of Messages')
                # st.pyplot(fig)
            with col2:
                fig2 = px.pie(data_frame=y, names='All User', values='Percentage of messages', hole=0.2)
                st.plotly_chart(fig2)

        # TODO 8 WorldCloud
        st.header(':red[WordCloud]')
        val_wc = usefulFuns.create_wordCloud(selected_user, df)
        fig, ax = plt.subplots()
        # noinspection PyRedeclaration
        ax = plt.imshow(val_wc)
        st.pyplot(fig)

        # TODO 9 Most Common 20 Words
        st.header(':red[Most Common 20 Words]')
        df_mcw20 = usefulFuns.make_MCW(selected_user, df)
        fig_mcw = px.bar(data_frame=df_mcw20, y='MCW20', x='NoOf20MCW', color='NoOf20MCW', orientation='h')
        st.plotly_chart(fig_mcw)

        # TODO 10 Emoji Analysis
        st.header(':red[Emoji Analysis]')
        df_emojiCount = usefulFuns.emoji_analysis(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(df_emojiCount)
        with col2:
            fig_em = px.pie(data_frame=df_emojiCount, names='EMOJI', values='COUNT', hole=0.3)
            st.plotly_chart(fig_em)

    else:
        st.header(':green[Click Show analysis button for Statistics]')

else:
    st.title(':red[Welcome to WhatsApp Chat Analyzier App]')
    st.header(':violet[Upload Whatsapp chat text file by clicking on browse files '
              'button on the left side of window]')
    st.subheader(':blue[To download your WhatsApp chat history do the following steps:]\n '
                 '1. :green[Open WhatsApp on your phone.]\n'
                 '2. :green[Tap the three vertical dots on the top right corner of the screen.]\n'
                 '3. :green[Tap “More” and then “Export Chat”.]\n'
                 '4. :green[Choose whether to export/save with media or without media.]')
