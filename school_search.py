"""School Search Challenge"""

__author__ = ('sean.hermany@gmail.com (Sean Hermany)',)

import csv
import time


SCHOOL_DATA_FILENAME = 'school_data.csv'


LONG_STATE_NAMES = {
    'AL': 'ALABAMA',
    'AK': 'ALASKA',
    'AZ': 'ARIZONA',
    'AR': 'ARKANSAS',
    'CA': 'CALIFORNIA',
    'CO': 'COLORADO',
    'CT': 'CONNECTICUT',
    'DE': 'DELAWARE',
    'DC': 'DISTRICT OF COLUMBIA',
    'FL': 'FLORIDA',
    'GA': 'GEORGIA',
    'HI': 'HAWAII',
    'ID': 'IDAHO',
    'IL': 'ILLINOIS',
    'IN': 'INDIANA',
    'IA': 'IOWA',
    'KS': 'KANSAS',
    'KY': 'KENTUCKY',
    'LA': 'LOUISIANA',
    'ME': 'MAINE',
    'MD': 'MARYLAND',
    'MA': 'MASSACHUSETTS',
    'MI': 'MICHIGAN',
    'MN': 'MINNESOTA',
    'MS': 'MISSISSIPPI',
    'MO': 'MISSOURI',
    'MT': 'MONTANA',
    'NE': 'NEBRASKA',
    'NV': 'NEVADA',
    'NH': 'NEW HAMPSHIRE',
    'NJ': 'NEW JERSEY',
    'NM': 'NEW MEXICO',
    'NY': 'NEW YORK',
    'NC': 'NORTH CAROLINA',
    'ND': 'NORTH DAKOTA',
    'OH': 'OHIO',
    'OK': 'OKLAHOMA',
    'OR': 'OREGON',
    'PA': 'PENNSYLVANIA',
    'RI': 'RHODE ISLAND',
    'SC': 'SOUTH CAROLINA',
    'SD': 'SOUTH DAKOTA',
    'TN': 'TENNESSEE',
    'TX': 'TEXAS',
    'UT': 'UTAH',
    'VT': 'VERMONT',
    'VA': 'VIRGINIA',
    'WA': 'WASHINGTON',
    'WV': 'WEST VIRGINIA',
    'WI': 'WISCONSIN',
    'WY': 'WYOMING',
    'BI': 'BUREAU OF INDIAN AFFAIRS',
    'AS': 'AMERICAN SAMOA',
    'GU': 'GUAM',
    'MP': 'NORTHERN MARIANAS',
    'PR': 'PUERTO RICO',
    'VI': 'VIRGIN ISLANDS'
}


class School(object):
    def __init__(self, name, city, state):
        self._name = name
        self._city = city
        self._state = state
        self._long_state = LONG_STATE_NAMES.get(state)

    def calc_score(self, tokens):
        score = 0
        matching_tokens = 0
        for token in tokens:
            token = token.upper()
            if token == 'SCHOOL': # stop word
                continue

            matched = False
            if token in self._name:
                score += 3
                matched = True
            if token in self._city:
                score += 2
                matched = True
            if token == self._long_state:
                score += 1
                matched = True
            if matched:
                matching_tokens += 1
        score = score * (matching_tokens*3)
        return score

    @property
    def name(self):
        return self._name

    @property
    def city(self):
        return self._city

    @property
    def state(self):
        return self._state


class SchoolSearcher(object):
    def __init__(self):
        # A mapping of tokens to School objects (via their index in a list)
        self._index = dict()
        self._schools = list()

        idx = 0
        # Note, character encoding determined via chardet
        with open(SCHOOL_DATA_FILENAME, encoding='Windows-1252') as csv_file:
            school_data_reader = csv.DictReader(csv_file)
            for row in school_data_reader:
                school_name = row['SCHNAM05']
                city = row['LCITY05']
                state = row['LSTATE05']
                long_state = LONG_STATE_NAMES.get(state)

                s = School(school_name, city, state)
                self._schools.append(s)

                # tokenize school name before adding to index
                name_tokens = school_name.split(' ')
                for token in name_tokens:
                    # don't index on these stop words for this dataset
                    if token not in ['SCHOOL', 'ELEMENTARY', 'MIDDLE', 'HIGH']:
                        self._index.setdefault(token, []).append(idx)
                self._index.setdefault(city, []).append(idx)
                self._index.setdefault(long_state, []).append(idx)
                idx += 1

    def search(self, query):
        start_time = time.perf_counter()

        ranked_results = []
        tokens = query.split(' ')

        # get all possible schools using index
        all_possibles = set()
        for token in tokens:
            possibles = self._index.get(token.upper())
            if possibles:
                all_possibles.update(possibles)

        # score and rank all possible schools
        for school_idx in all_possibles:
            school = self._schools[school_idx]
            score = school.calc_score(tokens)
            ranked_results.append((score, school))
        ranked_results.sort(key=lambda score_school: score_school[0], reverse=True)

        # Only interested in top 3 results
        results = ranked_results[:3]
        # Drop the scores before returning results
        results = [score_school[1] for score_school in results]

        end_time = time.perf_counter()
        query_time = end_time - start_time

        return results, query_time


_searcher = None


def search_schools(query):
    global _searcher
    if not _searcher:
        _searcher = SchoolSearcher()

    results, query_time = _searcher.search(query)

    print("Results for \"%s\" (search took: %.3fs)" % (query, query_time))
    for num, school in enumerate(results, start=1):
        print("%d. %s" % (num, school.name))
        print("%s, %s" % (school.city, school.state))


def main():
    search_schools("elementary school highland park")
    print("- - -")
    search_schools("jefferson belleville")
    print("- - -")
    search_schools("riverside school 44")
    print("- - -")
    search_schools("granada charter school")
    print("- - -")
    search_schools("foley high alabama")
    print("- - -")
    search_schools("KUSKOKWIM")


if __name__ == '__main__':
    main()
