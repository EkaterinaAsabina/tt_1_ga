from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.sql import text
from sqlalchemy.orm import declarative_base
import os
import get_spacex_data
from jinja2 import Environment, FileSystemLoader


psg_db = os.environ.get('POSTGRES_DATABASE', 'postgres')
psg_schema = os.environ.get('POSTGRES_SCHEMA', 'postgres')
psg_user = os.environ.get('POSTGRES_USER', 'postgres')
psg_pas = os.environ.get('POSTGRES_PASSWORD', 'postgrespw')
psg_host = os.environ.get('POSTGRES_HOST', 'localhost')
psg_port = os.environ.get('POSTGRES_PORT', '32768')

url = URL.create(
    drivername="postgresql",
    username=psg_user,
    password=psg_pas,
    host=psg_host,
    port=psg_port,
    database=psg_db
)

engine = create_engine(url)

connection = engine.connect()

Base = declarative_base()

class Rockets(Base):
    __tablename__ = "rockets"
    __table_args__ = {"schema": psg_schema}

    rocket_id = Column(String(24), primary_key=True)
    rocket_name = Column(String(100))

class Launches(Base):
    __tablename__ = "launches"
    __table_args__ = {"schema": psg_schema}

    launch_id = Column(String(50), primary_key=True)
    rocket_id = Column(String(50), ForeignKey(Rockets.rocket_id))
    wikipedia = Column(String(150))
    video_link = Column(String(150))
    reddit_recovery = Column(String(150))
    reddit_media = Column(String(150))
    reddit_launch = Column(String(150))
    presskit = Column(String(150))
    reddit_campaign = Column(String(150))
    mission_patch_small = Column(String(150))
    mission_patch = Column(String(150))
    article_link = Column(String(150))

class Missions(Base):
    __tablename__ = "missions"
    __table_args__ = {"schema": psg_schema}

    mission_id = Column(String(26), primary_key=True)
    mission_name = Column(String(50))
    launch_id = Column(String(24), ForeignKey(Launches.launch_id))

class Spacexdatamart(Base):
    __tablename__ = "spacex_datamart"
    __table_args__ = {"schema": psg_schema}

    mission_name = Column(String(50), primary_key=True)
    rocket_name = Column(String(100), primary_key=True)
    links_count = Column(Integer)

def load_datamart():
    environment = Environment(loader=FileSystemLoader(""), trim_blocks=True)
    template = environment.get_template("insert_spacex_datamart.sql")
    statement = template.render(psg_schema=psg_schema)
    t = connection.begin()
    connection.execute(text(statement))
    t.commit()


def main():
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine)

    get_spacex_data.get_rockets().to_sql("rockets", con=engine, if_exists = 'append', index = False)
    get_spacex_data.get_launches().to_sql("launches", con=engine, if_exists = 'append', index = False)
    get_spacex_data.get_missions().to_sql("missions", con=engine, if_exists = 'append', index = False)

    load_datamart()

    connection.close()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise e
    finally:
        connection.close()

