"""create tables

Revision ID: 3549906ecebb
Revises: 
Create Date: 2024-08-13 00:51:05.354376

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3549906ecebb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "medias",
        sa.Column("media_path_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_medias")),
    )
    op.create_table(
        "users",
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_table(
        "followers",
        sa.Column("follower_id", sa.Integer(), nullable=False),
        sa.Column("followed_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["followed_id"],
            ["users.id"],
            name=op.f("fk_followers_followed_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["follower_id"],
            ["users.id"],
            name=op.f("fk_followers_follower_id_users"),
        ),
        sa.PrimaryKeyConstraint(
            "follower_id", "followed_id", name=op.f("pk_followers")
        ),
    )
    op.create_table(
        "tweets",
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("media_id", sa.Integer(), nullable=True),
        sa.Column("content", sa.String(length=3000), nullable=False),
        sa.Column(
            "tweet_date",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"], ["users.id"], name=op.f("fk_tweets_author_id_users")
        ),
        sa.ForeignKeyConstraint(
            ["media_id"], ["medias.id"], name=op.f("fk_tweets_media_id_medias")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tweets")),
    )
    op.create_table(
        "likes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("tweet_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tweet_id"], ["tweets.id"], name=op.f("fk_likes_tweet_id_tweets")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_likes_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_likes")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("likes")
    op.drop_table("tweets")
    op.drop_table("followers")
    op.drop_table("users")
    op.drop_table("medias")
    # ### end Alembic commands ###
