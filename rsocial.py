import json
import streamlit as st

if __name__ == "__main__":
    st.title("Some relevant reviews from reddit on JAMF")
    st.markdown("______________________")
    with open("sentiment_insights.json", "r") as json_file:
        file = json.load(json_file)
        for elem in file:
            if elem['useful'] == '0':  # Display reviews marked as '0'
                if 'title' in elem:
                    st.markdown(elem['title'])
                st.markdown(f"Written by {elem['author']}")
                st.markdown(f"Subreddit : r/{elem['subreddit']}")
                st.markdown(f"Date : {elem['created'].split()[0]}")
                st.markdown(f"Time : {elem['created'].split()[1]}")
                with st.expander(f"{elem['insight']}"):
                    st.markdown(elem['body'])
                st.markdown(f"[Open URL]({elem['url']})")
                st.markdown("______________________")
