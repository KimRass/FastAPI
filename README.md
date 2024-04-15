# 1. Bulletin Board (FastAPI)

## 1) Cloud

## 2) FasiAPI의 장단점과 사용한 이유
- Pydantic을 통해  데이터 유효성 검사를 할 수 있는데 이점이 편리합니다.
- Swagger UI를 사용하여 자동으로 API 문서가 생성됩니다.
- 비교적 최근에 나온 프레임워크이므로 Django나 Flask와 비교하면 커뮤니티가 작고 자료도 적습니다.
- 사용한 이유는 전에 Scene text image QC server API를 FastAPI를 사용해 만들었던 업무 경험이 있어 개인적으로 익숙하기 때문입니다.

## 3) Table Specifications
```python
# 'bulletin_board/app/schemas.py'
class DBUser(BASE):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email_addr = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)

    posts = relationship("DBPost", back_populates="writer")
    comments = relationship("DBComment", back_populates="writer")


class DBPost(BASE):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=datetime.now,
        nullable=True,
    )

    writer = relationship("DBUser", back_populates="posts")
    comments = relationship("DBComment", back_populates="post")


class DBComment(BASE):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    content = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=datetime.now,
        nullable=True,
    )

    writer = relationship("DBUser", back_populates="comments")
    post = relationship("DBPost", back_populates="comments")
```

## 4) Headers and Bodies
- 게시판 서버 API의 각 HTTP method별 Header와 Body는 다음과 같습니다.
- `create_user`:
    - Header: application/json
    - Body:
    ```json
    {
        "name": "string",
        "email_addr": "string"
    }
    ```
- `read_users`:
    - Header: application/json
    - Body:
    ```json
    {
        "user_id": 0,
        "name": "string",
        "email_addr": "string"
    }
    ```
- `update_user`:
    ```json
    {
        "name": "string",
        "email_addr": "string"
    }
    ```
- `delete_user`:

## 5) How to Start Server
```sh
bash run.sh bulletin_board
```

## 6) Logging
- 게시판 API 서버의 경우 예를 들어 다음과 같은 로그를 'logs.txt'에 기록합니다.
```
| 2024-04-15 20:11:39 | WARNING | Post not found; `post_id=1` | main.py | create_comment() |
| 2024-04-15 20:11:53 | INFO | Post created; user_id=1 title='T1' content='C1' | main.py | create_post() |
| 2024-04-15 20:17:31 | INFO | Comment created; user_id=1 post_id=1 content='C1' | main.py | create_comment() |
| 2024-04-15 20:17:40 | INFO | Comment created; user_id=1 post_id=1 content='C2' | main.py | create_comment() |
| 2024-04-15 20:19:16 | WARNING | User not found; `name=None email_addr='sd3da2@gmail.com'` | main.py | update_user() |
| 2024-04-15 20:19:28 | WARNING | User not found; `name=None email_addr='sd3da2@gmail.com'` | main.py | update_user() |
| 2024-04-15 20:26:21 | WARNING | User not found; `name=None email_addr='sd3da2@gmail.com'` | main.py | update_user() |
| 2024-04-15 20:26:27 | INFO | User updated; `name=None email_addr='sd3da2@gmail.com'` | main.py | update_user() |
| 2024-04-15 20:32:04 | INFO | Comment updated; content='C3' | main.py | update_comment() |
| 2024-04-15 20:34:16 | WARNING | Comment not found; `content='C3'` | main.py | update_comment() |
| 2024-04-15 20:34:41 | WARNING | Comment not found; `comment_id=3` | main.py | update_comment() |
| 2024-04-15 20:35:24 | WARNING | Comment not found; `comment_id=3` | main.py | update_comment() |
| 2024-04-15 20:35:32 | WARNING | Comment not found; `comment_id=20` | main.py | delete_comment() |
| 2024-04-15 20:35:41 | INFO | Comment deleted; `comment_id=2` | main.py | delete_comment() |

```

# 2. Instance Segmentation (FastAPI)

## 1) Training
- [DeepLabv3](https://github.com/KimRass/DeepLabv3)에서 DeepLabv3 ('Rethinking Atrous Convolution for Semantic Image Segmentation')를 직접 구현하고 VOC2012 (10,582 images of 'trainaug')에 대해서 학습시켰습니다.
- ImageNet-1k에 대해 학습시킨 ResNet-101 backbone을 Torchvision에서 가져와 사용했습니다.
- Loss function은 픽셀별 Cross-entropy의 합입니다.
- 학습 과정에서 최적의 모델을 선별하기 위해 Validation set에 대해 Pixel IoU를 사용했으며 21개 클래스들에 대해 평균을 구했습니다.

## 2) How to Start Server
1. [deeplabv3-voc2012.pt](https://drive.google.com/file/d/1hop_eH6MD-ng7bfg8iS9VW2EGT7_Fm19/view?usp=sharing)를 'instance_segmentation/resources' directory에 위치시킵니다.
2. `bash run.sh instance_segmentation`

## 3) Samples
| 'cat', 'chair' |
|:-:|
| <img src="https://github.com/KimRass/DeepLabv3/assets/67457712/21ec8f7b-8d46-4253-929d-eb5e8820469d" width="400"> |
| <p style="text-align:right">[Source](https://www.reddit.com/r/funny/comments/jtadyg/thanks_to_a_mini_armchair_for_my_daughter_my_cat/)</p> |

| 'person' |
|:-:|
| <img src="https://github.com/KimRass/DeepLabv3/assets/67457712/0c610ba0-adee-48ac-b386-410103ecda22" width="400"> |

| 'airplane' |
|:-:|
| <img src="https://github.com/KimRass/DeepLabv3/assets/67457712/ff07df30-a5d0-44d2-9534-5ce838a2c56f" width="400"> |

| 'dog', 'horse', 'person' |
|:-:|
| <img src="https://github.com/KimRass/DeepLabv3/assets/67457712/b536860e-6f4d-4977-b50e-56bc9c236d5b" width="400"> |
| <p style="text-align:right">[Source](https://metro.co.uk/2021/01/05/horse-dog-and-pony-are-best-friends-and-look-like-siblings-13849616/)</p> |
