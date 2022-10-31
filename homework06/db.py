from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)
from homework06.scraputils import get_news


def fill_data_base(all_news):
    s = session()
    for atribute in all_news:
        single_news = News(
            title=atribute["title"],
            author=atribute["author"],
            url=atribute["url"],
            comments=atribute["comments"],
            points=atribute["points"],
        )
        s.add(single_news)
        s.commit()


class News(Base):  # type: ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":

    all_collected_news = get_news("https://news.ycombinator.com/", n_pages=27)
    fill_data_base(all_collected_news)
