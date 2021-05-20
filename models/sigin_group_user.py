from datetime import datetime

from services.db_context import db


class SignGroupUser(db.Model):
    __tablename__ = 'sign_group_users'

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    belonging_group = db.Column(db.BigInteger(), nullable=False)

    checkin_count = db.Column(db.Integer(), nullable=False)
    checkin_time_last = db.Column(db.DateTime(timezone=True), nullable=False)
    impression = db.Column(db.Numeric(scale=3, asdecimal=False), nullable=False)
    add_probability = db.Column(db.Numeric(scale=3, asdecimal=False), nullable=False, default=0)
    specify_probability = db.Column(db.Numeric(scale=3, asdecimal=False), nullable=False, default=0)

    _idx1 = db.Index('sign_group_users_idx1', 'user_qq', 'belonging_group', unique=True)

    @classmethod
    async def ensure(cls, user_qq: int, belonging_group: int, for_update: bool = False) -> 'SignGroupUser':
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        if for_update:
            query = query.with_for_update()
        user = await query.gino.first()
        return user or await cls.create(
            user_qq=user_qq,
            belonging_group=belonging_group,
            checkin_count=0,
            checkin_time_last=datetime.min,  # 从未签到过
            impression=0,
        )

    @classmethod
    async def query_impression_all(cls, belonging_group: int) -> 'list,list':
        impression_list = []
        user_qq_list = []
        query = cls.query.where(
            (cls.belonging_group == belonging_group)
        )
        for user in await query.gino.all():
            impression_list.append(user.impression)
            user_qq_list.append(user.user_qq)
        return user_qq_list, impression_list

    @classmethod
    async def query_glod_all(cls, belonging_group: int) -> 'list,list':
        glod_list = []
        user_qq_list = []
        query = cls.query.where(
            (cls.belonging_group == belonging_group)
        )
        for user in await query.gino.all():
            glod_list.append(user.glod)
            user_qq_list.append(user.user_qq)
        return user_qq_list, glod_list