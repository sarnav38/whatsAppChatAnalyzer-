import re 
import pandas as pd

def txt2df(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,},\s\d{1,2}:\d{2}.[apAP][mM]\s-\s"
    pattern1 = r"\d{1,2}/\d{1,2}/\d{2,},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    form = '%d/%m/%y, %I:%M %p'
    # print(len(messages))
    if len(messages) == 0:
        messages = re.split(pattern1, data)[1:]
        # print(len(messages))
        pattern = pattern1
        form = '%d/%m/%y, %H:%M'
    dates = re.findall(pattern, data)
    date = []
    for i in dates:
        i = i.replace('-', "")
        date.append(i.strip())
    df = pd.DataFrame({'user_message': messages, 'message_date': date})
    df['message_date'] = pd.to_datetime(df['message_date'], format=form)
    df.rename(columns={'message_date': 'datetime'}, inplace=True)
    pat1 = r'([\w\W]+?):\s'
    user = []
    message = []
    for mess in df['user_message']:
        e = re.split(pat1, mess)
        if e[1:]:
            user.append(e[1])
            message.append(e[2])
        else:
            user.append('Group Notification')
            message.append(e[0])
    df['user'] = user
    df['message'] = message
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['monthname'] = df['datetime'].dt.month_name()
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute
    df['date'] = df['datetime'].dt.date
    df['dayname'] = df['datetime'].dt.day_name()
    period = []
    for hr in df['hour']:
        if hr == 23:
            period.append(str(hr) + "-" + str('00'))
        elif hr == 0:
            period.append(str('00') + "-" + str(hr + 1))
        else:
            period.append(str(hr) + "-" + str(hr + 1))
    df['period'] = period
    df = df.iloc[:, [1, 2, 0, 8, 3, 4, 11, 5, 9, 6, 10, 7]]
    return df
