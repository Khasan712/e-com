from django.db import connection
import math


def get_product_detail(product_id: int):
    # query =
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT get_product_detail({product_id});")
        result = cursor.fetchone()
    return result[0]


def get_top_products():
    query = """
        SELECT
            product.id, product.title_ln, product.title_ru,
            COALESCE(
                (
                    SELECT
                        price
                    FROM
                        product_productitemsellprice
                    WHERE
                        is_deleted = false AND
                        is_active = true AND
                        product_item_id = product_item.id
                    ORDER BY id DESC
                    LIMIT 1
                ),
                0
            ),
            COALESCE(
                (product_item.images->-1->>'url')::text,
                (product.images->-1->>'url')::text,
                NULL
            ),
            product_item.id
        FROM
            product_topproductitem AS top_product
        INNER JOIN
            product_productitem AS product_item 
            ON product_item.id = top_product.product_item_id
        INNER JOIN
            product_product AS product
            ON product.id = product_item.product_id
        WHERE
            top_product.is_deleted = FALSE
            AND top_product.is_active = TRUE
        ORDER BY
            top_product.id DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return [
        {
            "id": data[0],
            "title_ln": data[1],
            "title_ru": data[2],
            "price": data[3],
            "image": data[4],
            "item_id": data[5],
        } for data in result
    ]


def get_ads_products():
    query = """
        SELECT
            product.id, product.title_ln, product.title_ru,
            COALESCE(
                (
                    SELECT
                        price
                    FROM
                        product_productitemsellprice
                    WHERE
                        is_deleted = false AND
                        is_active = true AND
                        product_item_id = product_item.id
                    ORDER BY id DESC
                    LIMIT 1
                ),
                0
            ),
            COALESCE(
                (product_item.images->-1->>'url')::text,
                (product.images->-1->>'url')::text,
                NULL
            ),
            product_item.id
        FROM
            product_adsproductitem AS ads_product
        INNER JOIN
            product_productitem AS product_item 
            ON product_item.id = ads_product.product_item_id
        INNER JOIN
            product_product AS product
            ON product.id = product_item.product_id
        WHERE
            ads_product.is_deleted = FALSE
            AND ads_product.is_active = TRUE
        ORDER BY
            ads_product.id DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return [
        {
            "id": data[0],
            "title_ln": data[1],
            "title_ru": data[2],
            "price": data[3],
            "image": data[4],
            "item_id": data[5],
        } for data in result
    ]


def get_new_products():
    query = """
        SELECT
            product.id, product.title_ln, product.title_ru,
            COALESCE(
                (
                    SELECT
                        price
                    FROM
                        product_productitemsellprice
                    WHERE
                        is_deleted = false AND
                        is_active = true AND
                        product_item_id = product_item.id
                    ORDER BY id DESC
                    LIMIT 1
                ),
                0
            ),
            COALESCE(
                (product_item.images->-1->>'url')::text,
                (product.images->-1->>'url')::text,
                NULL
            ), 
            product_item.id
        FROM
            product_productitem AS product_item
        INNER JOIN
            product_product AS product
            ON product.id = product_item.product_id
        WHERE
            product_item.is_deleted = FALSE
            AND product_item.is_active = TRUE
        ORDER BY
            product_item.id DESC
        LIMIT 5
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return [
        {
            "id": data[0],
            "title_ln": data[1],
            "title_ru": data[2],
            "price": data[3],
            "image": data[4],
            "item_id": data[5],
        } for data in result
    ]


def get_category_ids(category_id):
    query = f"""
        SELECT 
            category.id, child.id, sub_child.id
        FROM
            product_category AS category
        LEFT JOIN
            product_category AS child ON child.parent_id = category.id
        LEFT JOIN
            product_category AS sub_child ON sub_child.parent_id = child.id
        WHERE category.id = {category_id}
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return list({
        category
        for category_list in result
        for category in category_list if category
    })


def get_item_filters(filters):
    item_filters = """
        WHERE
            product_item.is_deleted = FALSE
            AND product_item.is_active = TRUE
    """
    if filters:
        q = filters.get("q")
        category_id = filters.get("category_id")
        brand_ids = filters.get("brand_ids")
        model_ids = filters.get("model_ids")
        character_ids = filters.get("character_ids")

        if q and isinstance(q, str):
            item_filters += f"""
                OR product.title_ln ILIKE '%{q}%'
                OR product.title_ru ILIKE '%{q}%'
                OR product.description_ln ILIKE '%{q}%'
                OR product.description_ru ILIKE '%{q}%'
                OR product.attributes_ln::text ILIKE '%{q}%'
                OR product.attributes_ru::text ILIKE '%{q}%'
                OR category.title_ln ILIKE '%{q}%'
                OR category.title_ru ILIKE '%{q}%'
                OR category.description_ln ILIKE '%{q}%'
                OR category.description_ru ILIKE '%{q}%'
                OR brand.title_ln ILIKE '%{q}%'
                OR brand.title_ru ILIKE '%{q}%'
                OR model.title_ln ILIKE '%{q}%'
                OR model.title_ru ILIKE '%{q}%'
                OR country.title_ln ILIKE '%{q}%'
                OR country.title_ru ILIKE '%{q}%'
                OR character_item.title_ln ILIKE '%{q}%'
                OR character_item.title_ru ILIKE '%{q}%'
                OR character_item.value ILIKE '%{q}%'
            """

        if category_id and str(category_id).isdigit():
            category_ids = str(get_category_ids(
                int(category_id))
            ).replace('[', "(").replace(']', ')')
            item_filters += f"""
            AND product.category_id IN {category_ids}
            """
        
        if brand_ids and isinstance(brand_ids, list):
            brand_ids = str(brand_ids).replace('[', "(").replace(']', ')')
            item_filters += f"""
            AND product.brand_id IN {brand_ids}
            """

        if model_ids and isinstance(brand_ids, list):
            model_ids = str(model_ids).replace('[', "(").replace(']', ')')
            item_filters += f"""
            AND product.model_id IN {model_ids}
            """

        if character_ids and isinstance(character_ids, list):
            character_ids = str(character_ids).replace('[', "(").replace(']', ')')
            item_filters += f"""
            AND character_item.id IN {character_ids}
            """

    return item_filters


def get_products(filters=None):
    item_filters = get_item_filters(filters)
    if not filters:
        page = 1
    else:
        page = int(filters.get("page", 1))
    limit = 48
    offset = limit*page-limit

    product_item_query = """
        SELECT 
            product.id, product.title_ln, product.title_ru,
            COALESCE(
                (
                    SELECT
                        price
                    FROM
                        product_productitemsellprice
                    WHERE
                        is_deleted = false AND
                        is_active = true AND
                        product_item_id = product_item.id
                    ORDER BY id DESC
                    LIMIT 1
                ),
                0
            ),
            COALESCE(
                (product_item.images->-1->>'url')::text,
                (product.images->-1->>'url')::text,
                NULL
            ),
            product_item.id
        FROM 
            product_productitem AS product_item
        INNER JOIN
            product_product AS product ON product.id = product_item.product_id
            AND product.is_deleted = FALSE AND product.is_active = TRUE
        INNER JOIN
            product_category AS category ON category.id = product.category_id
        LEFT JOIN
            product_brand AS brand ON brand.id = product.brand_id
        LEFT JOIN
            product_model AS model ON model.id = product.model_id
        LEFT JOIN
            product_country AS country ON country.id = product.country_id
        LEFT JOIN
            product_characteristic AS characteristic ON characteristic.product_id = product.id
        LEFT JOIN
            product_characteritem AS character_item ON character_item.id = characteristic.title_id
        %s
        GROUP BY
            product_item.id, product.id
        ORDER BY
            product_item.id DESC, product.id
        LIMIT %s OFFSET %s
    """%(item_filters, limit, offset)

    count_item_query = """
        SELECT 
            COUNT(product_item.id)
        FROM 
            product_productitem AS product_item
        INNER JOIN
            product_product AS product ON product.id = product_item.product_id
            AND product.is_deleted = FALSE AND product.is_active = TRUE
        INNER JOIN
            product_category AS category ON category.id = product.category_id
        LEFT JOIN
            product_brand AS brand ON brand.id = product.brand_id
        LEFT JOIN
            product_model AS model ON model.id = product.model_id
        LEFT JOIN
            product_country AS country ON country.id = product.country_id
        LEFT JOIN
            product_characteristic AS characteristic ON characteristic.product_id = product.id
        LEFT JOIN
            product_characteritem AS character_item ON character_item.id = characteristic.title_id
        %s
        GROUP BY
            product_item.id, product.id
    """%item_filters

    with connection.cursor() as cursor:
        cursor.execute(product_item_query)
        result = cursor.fetchall()

        cursor.execute(count_item_query)
        item_qty = cursor.fetchone()

    item_qty = item_qty[0] if item_qty else 0
    return {
        "count": item_qty,
        "prev": page - 1 if page > 1 else None,
        "next": page + 1 if math.ceil(item_qty / limit) > page else None,
        "results": [
            {
                "id": data[0],
                "title_ln": data[1],
                "title_ru": data[2],
                "price": data[3],
                "image": data[4],
                "item_id": data[5],
            } for data in result
        ]
    }


def get_carts(user_id):
    query = f"""
        SELECT
            cart.id, product_item.id, product.title_ln, product.title_ru, cart.quantity,
            COALESCE(
                (
                    SELECT
                        product_price.price
                    FROM
                        product_productitemsellprice AS product_price
                    WHERE
                        product_price.is_deleted = FALSE AND
                        product_price.is_active = TRUE AND
                        product_price.product_item_id = product_item.id
                    ORDER BY
                        product_price.id DESC
                    LIMIT 1
                ),
                0
            ),
            COALESCE(
                (product_item.images->-1->>'url')::text,
                (product.images->-1->>'url')::text,
                NULL
            )
        FROM 
            product_cart AS cart
        INNER JOIN
            product_productitem AS product_item ON product_item.id = cart.product_id
        INNER JOIN
            product_product AS product ON product.id = product_item.product_id
        WHERE
            cart.user_id = {user_id}
            AND cart.is_deleted = FALSE
            AND cart.is_active = TRUE
        ORDER BY 
            cart.id DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return [
        {
            "cart_id": data[0],
            "id": data[1],
            "title_ln": data[2],
            "title_ru": data[3],
            "quantity": data[4],
            "price": data[5],
            "image": data[6],
            'totalPrice': data[4] * data[5]
        } for data in result
    ]

