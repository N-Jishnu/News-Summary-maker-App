import streamlit as st
import base64
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk

nltk.download('punkt')
st.set_page_config(page_title='NEWS APP')

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
#put the file url saved on ur comp below for img background
set_background(r'C:\Users\kumar\OneDrive\Desktop\NewsApp\bg\R.png')#Remove line if shows error

def fetch_news_search_topic(topic):
    site = 'https://news.google.com/rss/search?q={}'.format(topic)
    op = urlopen(site)
    rd = op.read()   
    op.close() 
    sp_page = soup(rd, 'xml')  
    news_list = sp_page.find_all('item') 
    return news_list


def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site) 
    rd = op.read() 
    op.close() 
    sp_page = soup(rd, 'xml')  
    news_list = sp_page.find_all('item')  
    return news_list


def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    op = urlopen(site) 
    rd = op.read()  
    op.close()  
    sp_page = soup(rd, 'xml') 
    news_list = sp_page.find_all('item') 
    return news_list


def display_news(list_of_news):
    for news in list_of_news:
        st.write('=> {}'.format(news.title.text))
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            st.error(e)
        with st.expander(news.title.text):
            st.markdown('''<h6 style='text-align: justify;'>{}"</h6>'''.format(news_data.summary),unsafe_allow_html=True)
            st.markdown("[Read more at {}...]({})".format(news.source.text, news.link.text))
        st.success("Published Date: " + news.pubDate.text)

def main():
    st.header(":red[📰 News App ]:",divider='red')
    col1, col3 = st.columns([3, 3])

    with col1:
        st.write("")


    with col3:
        st.write("")
    category = ['Trending News', 'Favourite Topics', 'Search ']
    cat = st.selectbox('Select your Category', category)
    if cat == category[0]:
        st.subheader("Trending news :")
        news_list = fetch_top_news()
        display_news(news_list)
    elif cat == category[1]:
        top = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE','HEALTH']
        st.subheader("Choose your favourite Topic")
        chosen_topic = st.selectbox("Choose your favourite Topic", top)
        if chosen_topic == top[0]:
            st.warning("Please Choose the Topic")
        else:
            news_list = fetch_category_news(chosen_topic)
            if news_list:
                st.subheader(" {} New : ".format(chosen_topic))
                display_news(news_list)
            else:
                st.error("No News found for {}".format(chosen_topic))

    elif cat == category[2]:
        user_topic = st.text_input("Enter your Topic🔍")

        if st.button("Search") and user_topic != '':
            user_topic_pr = user_topic.replace(' ', '')
            news_list = fetch_news_search_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("{} News :".format(user_topic.capitalize()))
                display_news(news_list)
            else:
                st.error("No News found for {}".format(user_topic))
        else:
            st.warning("Please write Topic Name to Search🔍")


main()
