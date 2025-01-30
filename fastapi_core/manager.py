from app.db.database import _DB


class DBManager:
    _model: object
    _db: _DB

    def __init__(self, model, db):
        self._model = model
        self._db = db

    def all(self):
        return self._db.query(self._model).all()

    def queryset(self):
        return self._db.query(self._model)

    def get(self, id: int):
        return self._db.query(self._model).filter(self._model.id == id).first()

    def create(self, **kwargs):
        model = self._model(**kwargs)
        self._db.add(model)
        self._db.commit()
        return model

    def update(self, id: int, **kwargs):
        model = self._db.query(self._model).filter(self._model.id == id).first()
        for key, value in kwargs.items():
            setattr(model, key, value)
        self._db.commit()
        return model

    def delete(self, id: int):
        model = self._db.query(self._model).filter(self._model.id == id).first()
        self._db.delete(model)
        self._db.commit()
        return model
