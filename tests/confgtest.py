import pytest
from app.database import Base,engine

@pytest.fixture(autouse=True,scope='function')
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
