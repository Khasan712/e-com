from fastapi import FastAPI
from collections import defaultdict
from sqlalchemy import create_engine, text
from decouple import config

app = FastAPI()


@app.get("/categories/")
def read_root():
    DATABASE_URL = config('DATABASE_URL')
    engine = create_engine(DATABASE_URL)
    engine.connect()
    query = """
        SELECT c1.id, c1.title_ln,
            c2.id AS children_id, c2.title_ln AS children_title_ln,
            c3.id AS sub_children_id, c3.title_ln AS sub_children_title_ln
        FROM product_category c1
        LEFT JOIN product_category c2 ON c1.id = c2.parent_id
        LEFT JOIN product_category c3 ON c2.id = c3.parent_id
        WHERE c1.parent_id IS NULL and c1.is_active = true and c1.is_deleted = false;
    """

    with engine.connect() as conn:
        results = defaultdict(lambda: {
            "id": None,
            "title": None,
            "children": []
        })
        query_obj = text(query)
        fetch_all = conn.execute(query_obj)
    for row in fetch_all:
        parent_id, title, child_id, child_title, sub_child_id, sub_child_title = row[:6]
        parent = results[parent_id]
        parent['id'] = parent_id
        parent['title'] = title
        child = next((c for c in parent['children'] if c['id'] == child_id), None)
        if not child:
            child = {
                "id": child_id,
                "title": child_title,
                "children": []
            }
            parent['children'].append(child)

        sub_child = {
            "id": sub_child_id,
            "title": sub_child_title,
            "children": []
        }
        child['children'].append(sub_child)
    return list(results.values())
