import sys
sys.path.insert(0, "/Users/jongbeomkim/Desktop/workspace/ML-API")
import requests
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

BASE_URL = "http://localhost:8000"


def test_create_post(writer, title, content):
    url = f"{BASE_URL}/post/create_post"
    data = {"writer": writer, "title": title, "content": content}
    resp = requests.post(url, json=data)
    print(resp.json())


def to_df(posts):
    posts_df = pd.DataFrame(
        posts,
        columns=("id", "writer", "title", "content", "created_at", "updated_at"),
    )
    for col in ["created_at", "updated_at"]:
        posts_df[col] = pd.to_datetime(posts_df[col])
        posts_df[col] = posts_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
    return posts_df


def test_read_posts(**kwargs):
    """
    Call the function to read a specific post (replace post_id with an existing post ID)
    """
    url = f"{BASE_URL}/post/read_posts"
    resp = requests.get(url, params=kwargs)
    posts = resp.json()
    posts_df = to_df(posts)
    print(posts_df)


def test_update_post(post_id, title, content):
    """
    Call the function to update a specific post (replace post_id with an existing post ID).
    """
    url = f"{BASE_URL}/post/{post_id}"
    data = {"id": post_id, "title": title, "content": content}
    resp = requests.put(url, json=data)
    print(resp.json())


def test_delete_post(post_id):
    """
    Call the function to delete a specific post (replace post_id with an existing post ID)
    """
    url = f"{BASE_URL}/post/{post_id}"
    resp = requests.delete(url)
    print(resp.json())


if __name__ == "__main__":
    test_create_post(writer="WRITER", title="TITLE2", content="CONTENT")

    test_read_posts()

    test_update_post(post_id=2, title="NEW TITLE", content="NEW CONTENT")

    test_delete_post(post_id=4)
