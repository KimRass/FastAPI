import requests
import requests
import matplotlib.pyplot as plt
from datetime import datetime

BASE_URL = "http://localhost:8000"


def test_create_post(title, content):
    url = f"{BASE_URL}/posts/"
    data = {"title": title,"content": content}
    response = requests.post(url, json=data) # `timeout`
    print(response.json())


def test_read_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.get(url)
    print(response.json())


def test_update_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    data = {
        "title": "Updated Post Title",
        "content": "Updated content of the post!"
    }
    response = requests.put(url, json=data)
    print(response.json())


def test_delete_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.delete(url)
    if response.status_code == 200:
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
    url = f"{BASE_URL}/posts/"
    response = requests.get(url)
    if response.status_code == 200:
        posts = response.json()
    else:
        print(f"Failed to retrieve posts. Status code: {response.status_code}")
        posts = list()
    if posts:
        visualize_posts(posts)
    else:
        print("No posts retrieved.")


if __name__ == "__main__":
    # Call the function to create a new post
    title = "TITLE3"
    content = "CONTENT1"
    test_create_post(title=title, content=content)

    # Call the function to read a specific post (replace post_id with an existing post ID)
    test_read_post(post_id=21)

    # Call the function to update a specific post (replace post_id with an existing post ID)
    test_update_post(post_id=1)

    # Call the function to delete a specific post (replace post_id with an existing post ID)
    test_delete_post(post_id=1)


    # Retrieve all posts
    show_all_posts()
