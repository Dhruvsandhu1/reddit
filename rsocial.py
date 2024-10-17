import json
import streamlit as st

if __name__ == "__main__":
    st.title("Some relevant reviews from reddit on JAMF")
    st.markdown("______________________")
    with open("sentiment_insights.json", "r") as json_file:
        file=json.load(json_file)
        for elem in file:
            if elem['insight']=='0':
                if 'title' in elem:
                    st.markdown(elem['title'])
                st.markdown(f"Written by {elem['author']}")
                st.markdown(f"Subreddit : r/{elem['subreddit']}")
                st.markdown(elem['body'])
                st.markdown(f"[Open URL]({elem['url']})")
                st.markdown("______________________")
