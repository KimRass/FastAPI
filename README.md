# 1. Bulletin Board (FastAPI)

## 1) Cloud
- AWS의 EC2에서 't2.micro` instance type을 사용했습니다.
- (저의 경우에는) `ssh -i <KEY_PAIR.pem> ec2-user@ec2-3-141-143-48.us-east-2.compute.amazonaws.com`으로 Instance에 접속이 가능합니다.
- Inbound rule를 편집해서 8000번 포트를 개방합니다.
    - <img src="https://github.com/KimRass/FastAPI/assets/67457712/15006ab9-184e-4127-b0a9-a3d8c0317366" width="500">
- 정상적으로 작동함을 확인할 수 있습니다.
    - <img src="https://github.com/KimRass/FastAPI/assets/67457712/f931c36d-4e07-4f75-908c-8ae54f099992" width="500">

## 2) FastAPI의 장단점과 사용한 이유
- Pydantic을 통해  데이터 유효성 검사를 할 수 있는데 이점이 편리합니다.
- Swagger UI를 사용하여 자동으로 API 문서가 생성됩니다.
- 비교적 최근에 나온 프레임워크이므로 Django나 Flask와 비교하면 커뮤니티가 작고 자료도 적습니다.
- 사용한 이유는 전에 Scene text image QC server API를 FastAPI를 사용해 만들었던 업무 경험이 있어 개인적으로 익숙하기 때문입니다.

## 3) Table Specifications
- `DBUser` (`"users"` table), `DBPost` (`"posts"` table), `DBComment` (`"comments"` table)는 각각 게시판의 사용자, 게시글, 댓글을 의미합니다.
- `DBUser`와 `DBPost`는 one-to-many 관계입니다.
- `DBUser`와 `DBComment`는 one-to-many 관계입니다.
- `DBPost`와 `DBComment`는 one-to-many 관계입니다.
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

| `create_user` | `read_users` | `update_user` | `delete_user` |
|:-:|:-:|:-:|:-:|
| <img src="https://github.com/KimRass/FastAPI/assets/67457712/2e2f2b65-7996-4fd7-a02d-0b6fac6afe0f" width="400"> | <img src="https://github.com/KimRass/FastAPI/assets/67457712/5d0d82e5-2255-434a-9f16-fb920272e352" width="400"> | <img src="https://github.com/KimRass/FastAPI/assets/67457712/ffa7bbd0-fb43-444e-9b0c-c87e86f82be7" width="400"> | <img src="https://github.com/KimRass/FastAPI/assets/67457712/6fca2cf3-4e08-4cd1-b903-61feb76b70bb" width="400"> |

| `create_post` | `read_posts` | `update_post` | `delete_post` |
|:-:|:-:|:-:|:-:|
| <img src="https://github.com/KimRass/FastAPI/assets/67457712/77f43aae-1202-4d4d-b6d4-fb1c3027733f" width="400"> | <img src="https://github.com/KimRass/FastAPI/assets/67457712/10d8238d-ff2a-4d8d-9e04-70943dc52279" width="400"> | <img src="https://github.com/KimRass/FastAPI/assets/67457712/f3ff4860-5e78-4498-ad27-e98797b0518f" width="400"> | <img src="https://github.com/KimRass/FastAPI/assets/67457712/83a12770-a42f-40f9-807d-643eb77740f2" width="400"> |

| `create_comment` | `update_comment` | `delete_comment` |
|:-:|:-:|:-:|
| <img src="https://github.com/KimRass/FastAPI/assets/67457712/4439cdb4-714c-4602-8bc6-bf2d37262db0" width="400"> | <img src="https://github.com/KimRass/FastAPI/assets/67457712/06e9d772-5eb5-438e-9a21-cb42e7d18d17" width="400"> | <img src="https://github.com/KimRass/FastAPI/assets/67457712/8ef6e19a-752b-4b35-9d7d-e738d2dd68e8" width="400"> |

## 5) How to Start Server
```sh
bash run.sh bulletin_board
```

## 6) Logging
- 로그를 'logs.txt'에 자동으로 기록합니다.
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

# 2. Semantic Segmentation (FastAPI)

## 1) Training
- [DeepLabv3](https://github.com/KimRass/DeepLabv3)에서 DeepLabv3 ('Rethinking Atrous Convolution for Semantic Image Segmentation')를 직접 구현하고 VOC2012 (10,582 images of 'trainaug')에 대해서 학습시켰습니다.
- ImageNet-1k에 대해 학습시킨 ResNet-101 backbone을 Torchvision에서 가져와 사용했습니다.
- Loss function은 픽셀별 Cross-entropy의 합입니다.
- 학습 과정에서 최적의 모델을 선별하기 위해 Validation set에 대해 Pixel IoU를 사용했으며 21개 클래스들에 대해 평균을 구했습니다.
- CPU 환경에서도 추론이 가능하긴 하지만 느리므로 TorchScript로 변환하는 등의 방법으로 추론 속도를 향상시킬 수 있습니다.

## 2) How to Start Server
1. [deeplabv3-voc2012.pt](https://drive.google.com/file/d/1hop_eH6MD-ng7bfg8iS9VW2EGT7_Fm19/view?usp=sharing)를 'instance_segmentation/resources' directory에 위치시킵니다.
2. `bash run.sh instance_segmentation`

## 3) Samples
- 구글에서 VOC2012의 클래스를 검색하로 하여 적당한 이미지를 가져와 추론시켜보겠습니다.

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
