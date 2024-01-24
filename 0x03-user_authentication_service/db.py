#!/usr/bin/env python3
'''module for db.py'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import NoResultFound, InvalidRequestError


class DB:
    def __init__(self) -> None:
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No result found for the given query arguments.")
            return user
        except InvalidRequestError as e:
            raise e  # Reraise the InvalidRequestError
        except NoResultFound:
            raise NoResultFound("No result found for the given query arguments.")