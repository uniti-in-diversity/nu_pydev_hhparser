from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

engine = create_engine('sqlite:///hhdb_orm.sqlite', echo=True)
Base = declarative_base()

class Region(Base):
    __tablename__ = 'region'
    region_code = Column(Integer, primary_key=True)
    region_name = Column(String)

    def __init__(self, region_code, region_name):
        self.region_code = region_code
        self.region_name = region_name

    def __repr__(self):
        return f'<Region "{self.region_name}", id: {self.region_code}>'


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    vacancy_name = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey('region.region_code'))
    avg_salary = Column(Integer, nullable=False)
    total_vacancies = Column(DateTime, nullable=False)

    def __init__(self, vacancy_name, region_id, avg_salary, total_vacancies):
        self.vacancy_name = vacancy_name
        self.region_id = region_id
        self.avg_salary = avg_salary
        self.total_vacancies = total_vacancies

    def __repr__(self):
        return f'<Vacancy "{self.vacancy_name}", region_id:  {self.region_id}, id: {self.id}>'


Base.metadata.create_all(engine)

