import praw
import streamlit as st

# Set up your Reddit credentials
def init_reddit_client():
    reddit = praw.Reddit(
        client_id='i6B1PFZj-EM149Oq0czJHg',
        client_secret='fzM0zDFuWWJcerJC5QYiYQJCxrwh1A',
        user_agent='Review fetcher',
    )
    return reddit

# Fetch submissions based on a query
def fetch_reddit_data(subreddit_name, query, limit=5):
    reddit = init_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)
    
    # Search for submissions matching the query
    search_results = subreddit.search(query, limit=limit)

    results = []  # List to hold relevant posts and comments

    for submission in search_results:
        # Check if the submission title or selftext contains the query
        post_matches = []
        if query.lower() in submission.title.lower() or (submission.selftext and query.lower() in submission.selftext.lower()):
            post_matches.append({
                'title': submission.title,
                'score': submission.score,
                'url': submission.url,
                'num_comments': submission.num_comments,
            })
        
        # Fetch comments that mention the query
        submission.comments.replace_more(limit=0)  # Avoid "more comments" placeholders
        for comment in submission.comments.list():
            if query.lower() in comment.body.lower():
                results.append({
                    'type': 'comment',
                    'body': comment.body,
                })
        
        # Append the post if it has matches
        if post_matches:
            results.append({
                'type': 'post',
                'post_info': post_matches[0],  # Only include the first matched post
            })

    return results

# Streamlit App
def main():
    st.title("Reddit Search App")

    # User input for subreddit and query
    subreddit_name = st.text_input("Enter subreddit name", "all")
    query = st.text_input("Enter search query", "datadog")
    
    # Number of posts to fetch
    post_limit = st.slider("Number of posts to fetch", min_value=1, max_value=100, value=5)

    if st.button("Fetch Posts and Comments"):
        st.write(f"Searching for posts in r/{subreddit_name} mentioning: '{query}'...")
        
        # Fetch and display data
        results = fetch_reddit_data(subreddit_name, query, post_limit)
        
        if results:
            for result in results:
                if result['type'] == 'post':
                    post_info = result['post_info']
                    st.write(f"### Post: {post_info['title']}")
                    st.write(f"**Score:** {post_info['score']}")
                    st.write(f"**URL:** [Link]({post_info['url']})")
                    st.write(f"**Number of Comments:** {post_info['num_comments']}\n")
                elif result['type'] == 'comment':
                    st.write("**Comment:**")
                    st.write(result['body'])
        else:
            st.write("No posts or comments found matching the query.")

if __name__ == "__main__":
    main()
