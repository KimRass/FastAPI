import requests
import requests
import pandas as pd

pd.options.display.max_columns = 7

BASE_URL = "http://localhost:8000"


def test_create_user(name, email_addr):
    url = f"{BASE_URL}/users"
    data = {"name": name, "email_addr": email_addr}
    resp = requests.post(url, json=data)
    print(resp.json())
test_create_user("USER1", "EMAIL1")


def users_to_df(users):
    users_df = pd.DataFrame(
        users,
        columns=("id", "name", "email_addr", "created_at"),
    )
    for col in ["created_at"]:
        users_df[col] = pd.to_datetime(users_df[col])
        users_df[col] = users_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
    return users_df


def test_read_users(**kwargs):
    url = f"{BASE_URL}/users"
    resp = requests.get(url, json=kwargs)
    users = resp.json()
    users_df = users_to_df(users)
    print(users_df)
test_read_users()


def test_update_user(user_id, **kwargs):
    url = f"{BASE_URL}/users/{user_id}"
    resp = requests.put(url, json={"user_id": user_id, **kwargs})
    print(resp.json())
test_update_user(1, email_addr="sd3da2@gmail.com")


def test_delete_user(user_id):
    url = f"{BASE_URL}/users/{user_id}"
    resp = requests.delete(url)
    print(resp.json())
test_delete_user(user_id=20)


def test_create_post(user_id, title, content):
    url = f"{BASE_URL}/posts"
    data = {"user_id": user_id, "title": title, "content": content}
    resp = requests.post(url, json=data)
    print(resp.json())
test_create_post(user_id=1, title="T1", content="C1")


def posts_to_df(posts):
    posts_df = pd.DataFrame(
        posts,
        columns=("id", "user_id", "title", "content", "created_at", "updated_at"),
    )
    for col in ["created_at", "updated_at"]:
        posts_df[col] = pd.to_datetime(posts_df[col])
        posts_df[col] = posts_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
    return posts_df


def test_read_posts(**kwargs):
    url = f"{BASE_URL}/posts"
    resp = requests.get(url, json=kwargs)
    posts = resp.json()
    posts_df = posts_to_df(posts)
    print(posts_df)
test_read_posts()


def test_update_post(post_id, **kwargs):
    url = f"{BASE_URL}/posts/{post_id}"
    resp = requests.put(url, json={"post_id": post_id, **kwargs})
    print(resp.json())
test_update_post(1, title="T3")


def test_delete_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    resp = requests.delete(url)
    print(resp.json())
test_delete_post(post_id=1)


def test_create_comment(user_id, post_id, content):
    url = f"{BASE_URL}/comments"
    data = {"user_id": user_id, "post_id": post_id, "content": content}
    resp = requests.post(url, json=data)
    print(resp.json())
test_create_comment(user_id=1, post_id=1, content="C2")


def test_update_comment(comment_id, **kwargs):
    url = f"{BASE_URL}/comments/{comment_id}"
    resp = requests.put(url, json={"comment_id": comment_id, **kwargs})
    print(resp.json())
test_update_comment(comment_id=3, content="C3")


def test_delete_comment(comment_id):
    url = f"{BASE_URL}/comments/{comment_id}"
    resp = requests.delete(url)
    print(resp.json())
test_delete_comment(comment_id=2)
