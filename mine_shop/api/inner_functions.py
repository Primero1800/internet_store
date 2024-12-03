def filters(queryset, count, sort_by, x_filters_mapping, other, dict_mapping=None):
    data = None
    for case, value in x_filters_mapping.items():
        if sort_by == case:
            data = sorted(queryset, key=lambda x: x[value], reverse=True) if value else queryset
            break
    else:
        if dict_mapping:
            for case, value in dict_mapping.items():
                if sort_by == case:
                    def func(x):
                        return x[case][value] if value else sum(len(v) for v in x[case].values())
                    data = sorted(queryset, key=func, reverse=True)
                    break
    if not data:
        data = sorted(queryset, key=lambda x: x[other], reverse=True) if other else queryset

    if count:
        try:
            count = int(count)
            if count != 0:
                data = data[:count] if count > 0 else reversed(data[count:])
        except:
            pass
    elif sort_by:
        try:
            sort_by = int(sort_by)
            if sort_by != 0:
                data = data[:sort_by] if sort_by > 0 else reversed(data[sort_by:])
        except:
            pass

    return data