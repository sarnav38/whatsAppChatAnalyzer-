from urlextract import URLExtract
import re
import wordcloud
from collections import Counter
import pandas as pd
import emoji

extractor = URLExtract()


def fetch_user(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    total_message = df.shape[0]
    total_words = []
    for message in df['message']:
        total_words.extend(message.split())
    total_media = df['message'][df['message'] == '<Media omitted>\n'].shape[0]
    total_urls = []
    for message in df['message']:
        total_urls.extend(extractor.find_urls(message))
    return total_message, len(total_words), total_media, len(total_urls)


def most_Busy_user(df):
    a = df['user'].value_counts().head().reset_index()
    a.rename(columns={'index': 'Top 5 User', 'user': 'No of Messages'}, inplace=True)
    b = round((df['user'].value_counts() / df.shape[0]) * 100).reset_index()
    b.rename(columns={'index': 'All User', 'user': 'Percentage of messages'}, inplace=True)
    b = b.round({'Percentage of messages': 3})
    return a, b


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df.groupby(['year', 'monthname']).count()['message'].reset_index()
    month_year = []
    for i in range(df.shape[0]):
        month_year.append(df['monthname'][i] + '-' + str(df['year'][i]))
    df['monthname-year'] = month_year
    return df


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df.groupby(['date']).count()['message'].reset_index()
    return df


def most_busy_day(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df['dayname'].value_counts().reset_index()
    return df


def most_busy_month(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df['monthname'].value_counts().reset_index()
    return df


def week_Act(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df.pivot_table(values='message', index='dayname', columns='period', aggfunc='count', fill_value=0)
    return df


with open('stopWords.txt', 'r', encoding='utf-8') as f:
    stopwords = f.read()

# removed stopwords and single emoji as stop_hinglish.txt file contain emoji and stopwords
def remove_stopWords(message):
    words = []
    for word in message.lower().split():
        if word not in stopwords:
            words.append(word)
    return " ".join(words)

# removed multiple and latest emoji
def clean_MulEmoji(msg):
    # other than number and words all removed
    p = r'[a-zA-Z0-9]+'
    return " ".join(re.findall(p, msg))

# clean emoji link stopwords from message
def clear_df2temp(df):
    temp = df[df['user'] != 'Group Notification']
    # Media removed
    temp = temp[temp['message'] != '<Media omitted>\n']
    # Url Removed
    url = []
    for msg in temp['message']:
        url.append(extractor.has_urls(msg.strip()))
    temp['url'] = url
    temp = temp[temp['url'] == False]
    # REMOVE STOP WORDS AND EMOJI
    temp['message'] = temp['message'].apply(remove_stopWords)
    # REMOVE EMPTY MESSAGES
    temp = temp[temp['message'] != ""]
    # remove multi emoji
    temp['message'] = temp['message'].apply(clean_MulEmoji)
    temp = temp[temp['message'] != ""]
    return temp

def create_wordCloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = clear_df2temp(df)
    wc = wordcloud.WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    val_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return val_wc

def make_MCW(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = clear_df2temp(df)
    return pd.DataFrame(Counter(temp['message']).most_common(20), columns=['MCW20', 'NoOf20MCW'])


def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    femoji = []
    for message in df['message']:
        for m in message:
            if m in emoji.EMOJI_DATA.keys():
                femoji.append(m)
    return pd.DataFrame(Counter(femoji).most_common(6), columns=['EMOJI', 'COUNT'])
