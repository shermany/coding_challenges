"""School Data Stats Challenge"""

__author__ = ('sean.hermany@gmail.com (Sean Hermany)',)

import csv


SCHOOL_DATA_FILENAME = 'school_data.csv'


def print_counts():
    row_count = 0

    # Note, would have used defaultdict here from collections if allowed.
    schools_by_state = dict()
    schools_by_mlocale = dict()
    schools_by_city = dict()

    city_with_most_schools = None
    highest_school_count = 0

    unique_cities = set()

    # Note, character encoding was determined via chardet
    with open(SCHOOL_DATA_FILENAME, encoding='Windows-1252') as csv_file:
        school_data_reader = csv.DictReader(csv_file)
        for row in school_data_reader:
            row_count += 1
            mlocale = row['MLOCALE']
            city = row['LCITY05']
            state = row['LSTATE05']

            city_state = city + ',' + state

            unique_cities.add(city_state)

            schools_by_state.setdefault(state, 0)
            schools_by_state[state] += 1

            schools_by_mlocale.setdefault(mlocale, 0)
            schools_by_mlocale[mlocale] += 1

            schools_by_city.setdefault(city_state, 0)
            schools_by_city[city_state] += 1
            current_city_count = schools_by_city[city_state]
            if current_city_count > highest_school_count:
                highest_school_count = current_city_count
                city_with_most_schools = city

    print("Total Schools: %d" % row_count)

    print("Schools by State:")
    for state, count in schools_by_state.items():
        print("%s: %d" % (state, count))

    print("Schools by Metro-centric locale:")
    for mlocale, count in schools_by_mlocale.items():
        print("%s: %d" % (mlocale, count))

    print("City with most schools: %s (%d schools)" %
          (city_with_most_schools, highest_school_count))
    print("Unique cities with at least one school: %d" % len(unique_cities))


def main():
  print_counts()


if __name__ == '__main__':
    main()
