from sqlalchemy import create_engine, update, delete
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, Link, Mid

engine = create_engine('sqlite:///app.db')


session = sessionmaker(bind=engine)
s = session()


def add_links(links: list) -> bool:
    try:
        for link in links:
            new = Link(link=link)
            s.add(new)
            s.commit()

        return True

    except Exception as e:
        print(e)
        return False


def get_link(link_id: int) -> str | bool:
    try:
        response = s.query(Link.link).where(Link.id == link_id)[0][0]
        return response

    except Exception as e:
        print(e)
        return False