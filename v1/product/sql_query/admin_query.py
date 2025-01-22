from django.db import connection
from collections import defaultdict
from v1.product.models import Category
import time, requests


def get_all_active_category():
    query = """
        SELECT 
            c1.id, c1.title_ln, c2.id, c2.title_ln, c3.id, c3.title_ln
        FROM 
            product_category AS c1
        LEFT JOIN
            product_category AS c2 ON c1.id = c2.parent_id
        LEFT JOIN
            product_category AS c3 ON c2.id = c3.parent_id
        LEFT JOIN
            product_product AS p1 ON c1.id = p1.category_id AND p1.is_active = TRUE AND p1.is_deleted = FALSE
        LEFT JOIN
            product_product AS p2 ON c2.id = p2.category_id AND p2.is_active = TRUE AND p2.is_deleted = FALSE
        INNER JOIN
            product_product AS p3 ON c3.id = p3.category_id AND p3.is_active = TRUE AND p3.is_deleted = FALSE
        WHERE
            c1.parent_id IS NULL 
            AND c1.is_active = TRUE
            AND c1.is_deleted = FALSE
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = defaultdict(lambda: {
            "id": None,
            "title": None,
            "children": []
        })
        for row in cursor.fetchall():
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


# GET UZUM.UZ CATEGORIES
def get_categories():
    url = 'https://api.uzum.uz/api/main/root-categories?eco=false'
    headers = {
        "Authorization": "Basic YjJjLWZyb250OmNsaWVudFNlY3JldA==",
        "Accept-Language": "uz-UZ"
    }
    response = requests.get(url, headers=headers)
    return response.json()['payload']


def save_categories():
    categories = get_categories()
    son = 1
    for category in categories:
        category_obj = Category(
            title_ln=category.get("title")
        )
        category_obj.save()
        time.sleep(10)
        if category.get("children"):
            for category_child in category.get("children"):
                category_child_obj = Category(
                    title_ln=category_child.get("title"),
                    parent_id=category_obj.id
                )
                category_child_obj.save()
                time.sleep(10)
                if category_child.get("children"):
                    category_child_objs = [
                        Category(
                            title_ln=category_child_child.get('title'),
                            parent_id=category_child_obj.id
                        ) for category_child_child in category_child.get("children")
                    ]
                    if category_child_objs:
                        Category.objects.bulk_create(category_child_objs)
                son += 1


def search_ikpu_sql(q, page=1):
    limit = 50
    offset = limit*page-50
    sql_query = f"""
        SELECT 
            id, title_ln, code
        FROM
            product_ikpu
        WHERE 
            is_deleted = false AND is_active = true AND
            title_ln ILIKE %s
            OR "group" ILIKE %s
            OR class_group ILIKE %s
            OR position ILIKE %s
            OR sub_position ILIKE %s
            OR brand ILIKE %s
        ORDER BY
            id
        LIMIT {limit} OFFSET {offset}
    """
    with connection.cursor() as cursor:
        query_param = [f'%{q}%'] * 6
        cursor.execute(sql_query, query_param)
        results = cursor.fetchall()

    return {
        "status": True,
        "data": (
            {"id": result[0], "title_ln": result[1], "code": result[2]}
            for result in results
        )
    }


def get_products(q, page=1):
    offset = (page-1) * 50
    sql_query = f"""
        SELECT
            "product_product"."id",
            "product_product"."title_ln" AS "title",
            "product_category"."title_ln" AS "category_name",
            "user_user"."first_name" AS "seller_name",
            COALESCE(
                (
                    SELECT "sku"
                    FROM (
                        SELECT "product_sku"."sku"
                        FROM "product_sku"
                        WHERE "product_sku"."product_id" = "product_product"."id"
                        LIMIT 1
                    ) AS "inner_sku"
                ),
                NULL
            ) AS "sku",
            "product_product"."created_at"
        FROM
            "product_product"
        LEFT JOIN
            "product_category" ON ("product_product"."category_id" = "product_category"."id")
        LEFT JOIN
            "user_user" ON ("product_product"."seller_id" = "user_user"."id")
    """
    if q:
        sql_query += """
            WHERE "product_product"."is_deleted" = false AND "product_product"."is_active" = true
            AND "product_product"."title_ln" ILIKE %s
            OR "product_product"."title_ru" ILIKE %s
            OR "product_product"."attributes_ln"::text ILIKE %s
            OR "product_product"."attributes_ru"::text ILIKE %s
            OR "product_category"."title_ln" ILIKE %s
            OR "product_category"."title_ru" ILIKE %s
        ORDER BY "product_product"."id" DESC
        """
    if not q:
        sql_query += """
            WHERE "product_product"."is_deleted" = false AND "product_product"."is_active" = true
        """
    sql_query += f"""
        ORDER BY "product_product"."created_at" DESC 
        LIMIT 50 OFFSET {offset};
    """
    with connection.cursor() as cursor:
        if q:
            query_param = [f'%{q}%'] * 6
            cursor.execute(sql_query, query_param)
        else:
            cursor.execute(sql_query)
        results = cursor.fetchall()

    return {
        "status": True,
        "data": (
            {"id": result[0], "title": result[1], "category_name": result[2], "seller_name": result[3], "sku": result[4], "created_at": result[5]}
            for result in results
        )
    }
