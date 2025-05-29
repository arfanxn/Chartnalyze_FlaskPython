from app.repositories.repository import Repository
from app.extensions import db
from app.models import Save
from flask import request
from flask_sqlalchemy.query import Query
from werkzeug.exceptions import NotFound

class SaveRepository(Repository):

    def __init__(self):
        super().__init__()

    def query(self) -> Query:
        joins = request.args.get('join', '').split(',')
        sorts = request.args.get('sort', '').split(',')
        
        query = Save.query
        
        if len(joins) > 0:
            if 'user' in joins:
                query = query.options(db.joinedload(Save.user))
            if 'saveable' in joins:
                query = query.options(db.joinedload(Save.saveable_post))
        
        if len(sorts) > 0:
            if '-created_at' in sorts:
                query = query.order_by(Save.created_at.desc())
            elif 'created_at' in sorts:
                query = query.order_by(Save.created_at)
        
        return query        

    def paginate(self, user_id: str|None = None, saveable_id: str|None = None, saveable_type: str|None = None) -> tuple[list[Save], dict]:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = self.query()

        if user_id is not None:
            query = query.filter(Save.user_id == user_id)
        if saveable_id is not None:
            query = query.filter(Save.saveable_id == saveable_id)
        if saveable_type is not None:
            query = query.filter(Save.saveable_type == saveable_type)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        saves = []
        for save in pagination.items:
            saves.append(save)

        meta = {
            'page': pagination.page,
            'per_page': pagination.per_page,    
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
        }

        return (saves, meta)
    
    def show (self, save_id: str) -> tuple[Save]:
        save = self.query()\
            .filter(Save.id == save_id)\
            .first()
        if save is None:
            raise NotFound('Save not found')

        return (save, )
    
    def toggle(self, user_id : str, saveable_id: str, saveable_type: str) -> tuple[bool]:
        save = Save.query\
            .filter(
                Save.user_id == user_id,
                Save.saveable_id == saveable_id, 
                Save.saveable_type == saveable_type
            ).first()
        
        if save is None:
            save = Save()
            save.user_id = user_id
            save.saveable_id = saveable_id
            save.saveable_type = saveable_type
            db.session.add(save)
            is_saved = True
        else:
            db.session.delete(save)
            is_saved = False

        return (is_saved, )