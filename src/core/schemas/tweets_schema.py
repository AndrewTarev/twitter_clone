from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseTweet(BaseModel):
    author_id: int
    title: str
    media_path: Optional[str]


class TweetIn(BaseTweet):
    pass


class TweetOut(BaseTweet):
    model_config = ConfigDict(from_attributes=True)
    id: int
