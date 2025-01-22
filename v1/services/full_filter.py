from django.db.models import Q


def get_product_items_full_filter(q, queryset):
    return queryset.filter(
        Q(artikul_ln__icontains=q) | Q(artikul_ru__icontains=q) | Q(product__title_ln__icontains=q) |
        Q(product__title_ru__icontains=q) | Q(product__description_ln__icontains=q) |
        Q(product__description_ru__icontains=q) | Q(product__category__title_ln__icontains=q) |
        Q(product__category__title_ru__icontains=q) | Q(product__brand__title_ln__icontains=q) |
        Q(product__brand__title_ru__icontains=q) | Q(product__title_ru__icontains=q)
    )


def get_category_parents(category):
    result = {
        "id": category.id,
        "title_ln": category.title_ln,
        "title_ru": category.title_ru,
        "parent": None if not category.parent else get_category_parents(category.parent),
    }
    return result


def get_categories_id(categories):
    r = []
    for category in categories:
        if category.children.exists():
            r += get_categories_id(category.children.all())
        else:
            r.append(category.id)
    return r


def get_category_and_children_id(category):
    r = []
    if not category.children.all():
        r.append(category.id)
    else:
        r += get_categories_id(category.children.all())
    return r


def get_category_parent_id_title(category):
    result = [{
        "id": category.id,
        "title_ln": category.title_ln,
        "title_ru": category.title_ru
    }]
    if category.parent:
        result += get_category_parent_id_title(category.parent)
    return result


def category_children_tree(category):
    return get_category_parent_id_title(category)[::-1]
