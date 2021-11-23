def split_queryset(data):
    sum_all = 0
    dict_section = {}
    dict_category = {}
    dict_name = {}
    for i in data:
        dict_section[i['id_section__section']] = {
            'id_section__id': i['id_section__id']
        }
        dict_category[i['id_category__category']] = {
            'id_category__id': i['id_category__id'],
            'id_category__to_section': i['id_category__to_section']
        }
        dict_name[i['id_name__name_operation']] = {
            'id_name__to_category': i['id_name__to_category'],
            'sum': i['sum']
        }
        sum_all += i['sum']
    return dict_section, dict_category, dict_name, sum_all
