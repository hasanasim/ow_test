import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app import models, schemas
from app.db_interaction import get_titles, get_title_by_id, create_title


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    models.Base.metadata.create_all(bind=engine)

    # Create a session and return it as the fixture
    session = Session()
    yield session

    # Clean up the database after all tests have finished
    session.close()
    models.Base.metadata.drop_all(bind=engine)


@pytest.mark.parametrize(
    'sort, order, expected_first',
    [
        ('title_number', 'asc', '123'),
        ('title_number', 'desc', '789'),
        ('id', 'asc', '123'),
        ('id', 'desc', '789'),
    ]
)
def test_get_titles_sorting_and_ordering(db, sort, order, expected_first):
    title1 = models.Title(id=0, title_number='123', title_class='Leasehold', content='test content 0')
    title2 = models.Title(id=1, title_number='456', title_class='Freehold', content='test content 1')
    title3 = models.Title(id=2, title_number='789', title_class='Freehold', content='test content 2')
    db.add(title1)
    db.add(title2)
    db.add(title3)
    db.commit()

    result = get_titles(db, _sort=sort, _order=order)
    assert result[0].title_number == expected_first
    assert len(result) == 3


def test_get_titles_limit(db):
    for i in range(20):
        db.add(
            models.Title(id=i, title_number=f'title_number{i}', title_class='Leasehold', content=f'test content {i}')
        )
    db.commit()
    result = get_titles(db, limit=10)
    assert len(result) == 10


def test_get_titles_skip_and_limit(db):
    for i in range(30):
        db.add(
            models.Title(id=i, title_number=f'title_number{i}', title_class='Leasehold', content=f'test content {i}')
        )
    db.commit()
    result = get_titles(db, skip=10, limit=10)
    assert result[0].id == 10
    assert result[-1].id == 19
    assert len(result) == 10


def test_get_title_by_id(db):
    title = models.Title(id=1, title_number='123', title_class='Leasehold', content='test_content')
    db.add(title)
    db.commit()

    result = get_title_by_id(db, title_id=1)
    assert result is not None
    assert result.title_number == '123'

    result = get_title_by_id(db, title_id=2)
    assert result is None


def test_create_title(db):
    title_create = schemas.TitleCreate(
        id=1,
        title_number='123',
        title_class='leasehold',
        content='test_content',
    )
    result = create_title(db, title_create)
    assert result is not None
    assert result.title_number == '123'
