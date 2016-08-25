import datetime
from sqlalchemy.orm import sessionmaker
from models import Car, engine


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


def save_car(stats_dict):

    Session = sessionmaker(bind=engine)
    session = Session()

    car = Car.query.filter_by(name=stats_dict['title']).first()

    if car is None:
        car = Car(name=stats_dict['title'],
                  link=stats_dict['link'],
                  milage=stats_dict['milage'],
                  transmission=stats_dict['transmission'],
                  year=datetime.datetime(stats_dict['year'], 1, 1),
                  price=stats_dict['price'],
                  size=stats_dict['size'],
                  last_scraped=datetime.datetime.utcnow())

    session.add(car)
    session.commit()
