from typing import List

from pydantic import BaseModel, ConfigDict, Field


class TweetIn(BaseModel):
    content: str = Field(..., alias="tweet_data")
    tweet_media_ids: list[int] | None = None


class TweetOut(BaseModel):
    result: bool
    tweet_id: int
    model_config = ConfigDict(from_attributes=True)


class AttachmentBase(BaseModel):
    link: str


class UserBase(BaseModel):
    id: int
    name: str


class LikeBase(BaseModel):
    user_id: int
    name: str


class TweetResponse(BaseModel):
    id: int
    content: str
    attachments: List[AttachmentBase]
    author: UserBase
    likes: List[LikeBase]


class TweetsResponse(BaseModel):
    tweets: List[TweetResponse]
