from app.repositories.repository import Repository
from app.extensions import db
from app.models import Activity
from flask import request
from flask_sqlalchemy.query import Query
from werkzeug.exceptions import NotFound

class ActivityRepository(Repository):

    def __init__(self):
        super().__init__()

    def query(self) -> Query:
        joins = request.args.get('join', '').split(',')
        sorts = request.args.get('sort', '').split(',')
        filter = request.args.get('filter', None)
        type = request.args.get('filter[type]', None)
        user_ip_address = request.args.get('filter[user_ip_address]', None)
        user_agent = request.args.get('filter[user_agent]', None)
        subject_type = request.args.get('filter[subject_type]', None)
        description = request.args.get('filter[description]', None)

        query = Activity.query

        if len(joins) > 0:
            if 'user' in joins:
                query = query.options(db.joinedload(Activity.user))
            if 'subject' in joins:
                query = query.options(db.joinedload(Activity.subject_user))
        
        if filter is not None: 
            query = query.filter(db.or_(
                Activity.id == filter,
                Activity.description.contains(filter),
                Activity.user_id == filter,
                Activity.user_ip_address == filter,
                Activity.user_agent.contains(filter),
                Activity.subject_id == filter,
            ))
        else:
            if type is not None: 
                query = query.filter(Activity.type == type)
            if description is not None: 
                query = query.filter(Activity.description.contains(description))
            if user_ip_address is not None: 
                query = query.filter(Activity.user_ip_address == user_ip_address)
            if user_agent is not None: 
                query = query.filter(Activity.user_agent.contains(user_agent))
            if subject_type is not None: 
                query = query.filter(Activity.subject_type == subject_type)
        
        if len(sorts) > 0:
            if '-created_at' in sorts:
                query = query.order_by(Activity.created_at.desc())
            elif 'created_at' in sorts:
                query = query.order_by(Activity.created_at)
        
        return query        

    def paginate(
            self, 
            user_id: str|None = None,
            subject_id: str|None = None, 
        ) -> tuple[list[Activity], dict]:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query()

        if user_id is not None:
            query = query.filter(Activity.user_id == user_id)
        if subject_id is not None:
            query = query.filter(Activity.subject_id == subject_id)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        activities = pagination.items

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (activities, meta)
    
    def show (self, activity_id: str) -> tuple[Activity]:
        activity = self.query()\
            .filter(Activity.id == activity_id)\
            .first()
        
        if activity is None:
            raise NotFound('Activity not found')

        return (activity, )