from app.services import Service
from app.models import Follow, User
from app.forms import QueryForm
from app.extensions import db
from werkzeug.exceptions import NotFound, BadRequest

class FollowService(Service):

    def __init__(self):
        super().__init__()

    def paginate_by_user(
        self,
        query_form: QueryForm,
        user_id: str,
        only_followers: bool = False,
        only_followeds: bool = False
    ) -> tuple[(list[Follow] | list[User]), dict]:
        query = Follow.query

        if only_followers:
            query = query.join(User, Follow.follower_id == User.id).filter(Follow.followed_id == user_id)
        elif only_followeds:
            query = query.join(User, Follow.followed_id == User.id).filter(Follow.follower_id == user_id)

        query = query.order_by(Follow.created_at.desc())

        if query_form.keyword.data is not None:
            query = query.filter(
                db.or_(User.name.like(f'%{query_form.keyword.data}%'), User.email.like(f'%{query_form.keyword.data}%'))
            )

        pagination = query.paginate(
            page=query_form.page.data,
            per_page=query_form.per_page.data,
            error_out=False,
        )

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        follows = pagination.items

        if only_followers:
            users = [follow.follower for follow in follows]
            return users, meta
        elif only_followeds:
            users = [follow.followed for follow in follows]
            return users, meta
        else:
            return follows, meta


    def paginate_followers_by_user(self, form: QueryForm, user_id: str) -> tuple[list[User], dict]:
        return self.paginate_by_user(form, only_followers=True, user_id=user_id)
    
    def paginate_followeds_by_user(self, form: QueryForm, user_id: str) -> tuple[list[User], dict]:
        return self.paginate_by_user(form, only_followeds=True, user_id=user_id)
    
    def toggle_follow(self, follower_id: str, followed_id: str) -> tuple[bool]:
        if follower_id == followed_id:
            raise BadRequest('You cannot follow yourself')

        follow = Follow.query.filter(
            db.and_(Follow.follower_id == follower_id, Follow.followed_id == followed_id)
        ).first()

        if follow is None:
            follow = Follow()
            follow.follower_id = follower_id
            follow.followed_id = followed_id
            db.session.add(follow)
            is_following = True
        else: 
            db.session.delete(follow)
            is_following = False
        
        db.session.commit() 
        return is_following

