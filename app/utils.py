
def stats_list_to_dict(car_stats):

    stats_dict = dict()
    stats_dict['year'] = car_stats[0]
    stats_dict['style'] = car_stats[1]
    stats_dict['milage'] = car_stats[2]
    stats_dict['transmission'] = car_stats[3]
    stats_dict['size'] = car_stats[4]
    stats_dict['fuel'] = car_stats[6] if len(car_stats) > 6 else car_stats[5]

    return stats_dict


def format_stats(stats_dict):

    stats_dict['year'] = int(stats_dict['year'][:4])
    stats_dict['milage'] = int(stats_dict['milage'].replace('miles', '').replace(',', '').strip())
    stats_dict['size'] = float(stats_dict['size'].replace('L', ''))

    return stats_dict


def increase_url_page_number(url, page):

    url_list = url.split('/')
    page_number_index = url_list.index('page') + 1
    next_page_number = page + 1
    url_list[page_number_index] = str(next_page_number)
    next_page_url = '/'.join(url_list)

    return next_page_url
