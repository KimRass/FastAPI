import sys
sys.path.insert(0, "/Users/jongbeomkim/Desktop/workspace/ML-API")
import requests
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

from app.schemas import PostCreate

BASE_URL = "http://localhost:8000"


def test_create_post(**kwargs):
    url = f"{BASE_URL}/post/create_post"
    resp = requests.post(url, json=kwargs)
    print(resp.json())


def test_read_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    resp = requests.get(url)
    print(resp.json())


def test_update_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    data = {
        "title": "Updated Post Title",
        "content": "Updated content of the post!"
    }
    resp = requests.put(url, json=data)
    print(resp.json())


def test_delete_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    resp = requests.delete(url)
    if resp.status_code == 200:
        print("Post deleted successfully")
    else:
        print("Failed to delete post")


def visualize_posts(posts):
    # Extract creation dates of posts
    creation_dates = [datetime.fromisoformat(post['created_at']) for post in posts]

    # Count posts created per day
    date_counts = {}
    for date in creation_dates:
        day = date.date()
        if day in date_counts:
            date_counts[day] += 1
        else:
            date_counts[day] = 1

    # Sort date_counts by date
    sorted_date_counts = dict(sorted(date_counts.items()))

    # Plotting the data
    dates = list(sorted_date_counts.keys())
    counts = list(sorted_date_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(dates, counts, color='skyblue')
    plt.title('Number of Posts Created Each Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Posts')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def show_all_posts():
    url = f"{BASE_URL}/post/get_all_posts"
    resp = requests.get(url)
    if resp.status_code == 200:
        posts = resp.json()
        print(posts)
    else:
        print(f"Failed to retrieve posts. Status code: {resp.status_code}")
        posts = list()

    if posts:
        posts_df = pd.DataFrame(
            posts, columns=("id", "writer", "title", "content", "created_at"),
        )
        print(posts_df)
show_all_posts()


if __name__ == "__main__":
    writer = "WRITER"
    title = "TITLE3"
    content = "CONTENT1"
    test_create_post(writer=writer, title=title, content=content)

    # Call the function to read a specific post (replace post_id with an existing post ID)
    test_read_post(post_id=21)

    # Call the function to update a specific post (replace post_id with an existing post ID)
    test_update_post(post_id=1)

    # Call the function to delete a specific post (replace post_id with an existing post ID)
    test_delete_post(post_id=1)


    # Retrieve all posts
