from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.db import Base, engine, Session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String)
    user_name = Column(String)
    free_slots = Column(Integer)

    def __repr__(self):
        return str(self.user_name)


class Resource(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return str(self.name)


class Market(Base):
    __tablename__ = 'markets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship("User", backref="markets")
    resource_id = Column(Integer, ForeignKey('resources.id'))
    resource = relationship("Resource", backref="markets")
    count = Column(Integer)
    last_update = Column(Integer)

    def __repr__(self):
        return f'Market res {self.resource.name} of user {self.user.name}'


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def add_test_data():
    Base.metadata.create_all(bind=engine)
    session = Session()

    res_pelt = Resource(name='Pelt')
    res_coal = Resource(name='Coal')
    res_stick = Resource(name='Stick')

    user_artem = User(name='Artem', user_name='artofey')
    user_maga = User(name='Maga', user_name='godzilla4')

    market_artem_pelt = Market(resource=res_pelt, user=user_artem, count=1000)
    market_artem_coal = Market(resource=res_coal, user=user_artem, count=2000)
    market_maga_stick = Market(resource=res_stick, user=user_maga, count=3000)

    session.add_all(
        [
            market_artem_coal,
            market_artem_pelt,
            market_maga_stick,
        ]
    )
    session.commit()


if __name__ == '__main__':
    add_test_data()
