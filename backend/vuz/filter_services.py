from django.db.models import Min, Max, Case, When, Value, IntegerField
from django.db.models.functions import Cast
from .models import Cities, Subjects, Metros, Programs, Faculties, Specialties, Forms, OrganizationsVuz


def russian_letter_sort_key(item):
    name = item[1] if isinstance(item, tuple) else item
    return name.replace('Ё', 'Е\u0001').replace('ё', 'е\u0001')


def get_filter_data(model, filter_kwargs, limit=20, offset=0, search=None, priority_ids=None):
    queryset = model.objects.filter(**filter_kwargs)
    total_count = queryset.count()

    if search:
        queryset = queryset.filter(name__icontains=search)

    if model.__name__ == 'Cities' and priority_ids:
        ordering = Case(
            *[When(id=id, then=Value(i)) for i, id in enumerate(priority_ids)],
            default=Value(len(priority_ids)),
            output_field=IntegerField()
        )
        queryset = queryset.order_by(ordering, 'name')
    else:
        queryset = queryset.order_by('name')

    queryset = queryset.distinct()
    
    unique_names = list(queryset.values_list('name', flat=True).distinct())
    unique_names.sort(key=russian_letter_sort_key)
    total_search = len(unique_names)
    
    if model.__name__ == 'Cities' and priority_ids:
        priority_items = dict(queryset.filter(id__in=priority_ids).values_list('id', 'name'))
        remaining_queryset = queryset.exclude(id__in=priority_ids)
        remaining_items = dict(remaining_queryset[offset:offset + (limit - len(priority_items))].values_list('id', 'name'))
        items = {**priority_items, **remaining_items}
    else:
        all_items = {}
        for item in queryset.values('id', 'name'):
            if item['name'] not in all_items.values():
                all_items[item['id']] = item['name']
        
        sorted_items = dict(sorted(all_items.items(), key=russian_letter_sort_key))
        items_list = list(sorted_items.items())
        start_idx = min(offset, len(items_list))
        end_idx = min(offset + limit, len(items_list))
        items = dict(items_list[start_idx:end_idx])

    return {
        "items": items,
        "total": total_count,
        "total_search": total_search
    }
 

def get_vuz_filters_data(filtered_vuz, filter_type=None, limit=20, offset=0, search=None, cities=None):
    vuz_ids_list = list(filtered_vuz.values_list('id', flat=True))
    # price_rating_data = filtered_vuz.aggregate(
    #     price_min=Min(Cast("calculation_data__cost_min", output_field=IntegerField())),
    #     price_max=Max(Cast("calculation_data__cost_min", output_field=IntegerField())),
    #     rating_min=Min("rating"),
    #     rating_max=Max("rating")
    # )
    price_rating_data = OrganizationsVuz.objects.aggregate(
        price_min=Min(Cast("calculation_data__cost_min", output_field=IntegerField())),
        price_max=Max(Cast("calculation_data__cost_min", output_field=IntegerField())),
    )

    filters_data = {
        "price": {
            "min": price_rating_data["price_min"] or 0,
            "max": price_rating_data["price_max"] or 0,
        },
        "is_state": {
            "items": {
                "1": "Государственный",
                "2": "Частный"
            },
            "total": 2,
            "total_search": 2
        }
        # "rating": {
        #     "min": price_rating_data["rating_min"] or 0,
        #     "max": price_rating_data["rating_max"] or 0,
        # }
    }

    programs_with_related = Programs.objects.filter(
        organization_vuz_id__in=vuz_ids_list
    ).select_related('faculty', 'specialty', 'form')

    faculty_names = programs_with_related.filter(
        faculty_id__isnull=False
    ).values_list('faculty__name', flat=True).distinct()

    specialty_names = programs_with_related.filter(
        specialty_id__isnull=False
    ).values_list('specialty__name', flat=True).distinct()

    form_names = programs_with_related.filter(
        form_id__isnull=False
    ).values_list('form__name', flat=True).distinct()

    level_codes = programs_with_related.filter(
        specialty__level_code__isnull=False
    ).values_list('specialty__level_code', flat=True).distinct()

    filter_configs = {
        'city': (Cities, {'organizationsvuz__id__in': vuz_ids_list}),
        'subject': (Subjects, {'organizationsvuz__id__in': vuz_ids_list}),
        'metro': (Metros, {'organizationsvuz__id__in': vuz_ids_list}),
        'faculty': (Faculties, {'name__in': faculty_names}),
        'specialty': (Specialties, {'name__in': specialty_names}),
        'form': (Forms, {'name__in': form_names}),
        'level_code': (Specialties, {'level_code__in': level_codes}),
        'organization_type': (OrganizationsVuz, {'id__in': vuz_ids_list})
    }

    if filter_type:
        if filter_type in filter_configs:
            model, kwargs = filter_configs[filter_type]
            priority_ids = [int(city_id) for city_id in cities.split(',')] if filter_type == 'cities' and cities else None
            if filter_type in ['level_code', 'organization_type']:
                if filter_type == 'level_code':
                    items = list(model.objects.filter(**kwargs).values_list('level_code', flat=True).distinct())
                else:
                    items = list(model.objects.filter(**kwargs).values_list('organization_type', flat=True).distinct())
                items = [item for item in items if item]
                items.sort()
                total = len(items)
                items_dict = {str(idx + 1): code for idx, code in enumerate(items[offset:offset + limit])}
                filters_data[filter_type] = {
                    "items": items_dict,
                    "total": total,
                    "total_search": total
                }
            else:
                filters_data[filter_type] = get_filter_data(model, kwargs, limit, offset, search, priority_ids)
    else:
        for filter_name, (model, kwargs) in filter_configs.items():
            priority_ids = [int(city_id) for city_id in cities.split(',')] if filter_name == 'cities' and cities else None
            if filter_name in ['level_code', 'organization_type']:
                if filter_name == 'level_code':
                    items = list(model.objects.filter(**kwargs).values_list('level_code', flat=True).distinct())
                else:
                    items = list(model.objects.filter(**kwargs).values_list('organization_type', flat=True).distinct())
                items = [item for item in items if item]
                items.sort()
                total = len(items)
                items_dict = {str(idx + 1): code for idx, code in enumerate(items[:limit])}
                filters_data[filter_name] = {
                    "items": items_dict,
                    "total": total,
                    "total_search": total
                }
            else:
                filters_data[filter_name] = get_filter_data(model, kwargs, limit, offset, search, priority_ids)

    return filters_data
