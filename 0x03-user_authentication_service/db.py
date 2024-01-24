#!/usr/bin/env python3
'''module for db.py'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    '''DB class'''
    def __init__(self) -> None:
        '''constructor'''
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        '''creates a session if not created'''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''takes mandatory email and hashed_password
        fields and returns a User'''
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        '''takes in arbitrary keyword arguments and returns the first row'''
        user = self._session.query(User)
        for key, value in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            for usr in user:
                if getattr(usr, key) == value:
                    return usr
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes based on the provided arguments.

        Args:
            user_id (int): The ID of the user to update.
            kwargs: Arbitrary keyword arguments representing user attributes.

        Raises:
            ValueError: If an argument that does not
            correspond to a user attribute is passed.
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if key not in User.__dict__:
                    raise ValueError(f"Invalid user attribute: {key}")
                setattr(user, key, value)
            self._session.commit()
        except NoResultFound:
            raise ValueError(f"No user found with ID: {user_id}")
