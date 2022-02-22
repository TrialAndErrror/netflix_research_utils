from slugify import slugify
import pandas as pd


WIKI_URLS = {
    'Films': {
        '2015-2017': 'https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2015%E2%80%932017)',
        '2018': 'https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2018)',
        '2019': 'https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2019)',
        '2020': 'https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2020)',
        '2021': 'https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2021)',
        '2022': 'https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(since_2022)',
    },
    'Standup': 'https://en.wikipedia.org/wiki/List_of_Netflix_original_stand-up_comedy_specials',
    'Distribution': 'https://en.wikipedia.org/wiki/List_of_Netflix_exclusive_international_distribution_films'
}


class WikiAnalyzer:
    def __init__(self, nf_titles, url_dict):
        self.nf_titles = nf_titles
        self.url_dict = url_dict
        self.leftovers = []

        self.standup_url = url_dict.get('Standup')
        self.distribution_url = url_dict.get('Distribution')
        self.movie_urls = url_dict.get('Films')

        self.results_dict = {}

        self.dataset_split_dict = {}

        self.all_wiki_titles = []
        self.all_dataset_titles = []

    @staticmethod
    def help():
        info = {
            '.run_all()': 'Fetch data from Wikipedia and compare with the netflix dict. Outputs the number of titles '
                          'found and missing titles.\n',

            '.dataset_split_dict': 'Get dictionary of netflix dict tiles split up by Wikipedia page\n',

            '.all_wiki_titles': 'List of titles found across all Wiki pages',

            '.all_dataset_titles': 'List of all titles from netflix dict that were found on Wiki pages',

            '.leftovers': 'List of titles that were not found on Wiki pages.\n',

            '.count_number_identified()': 'Get count of number of titles from the nf_dict that were identified across '
                                          'all Wiki pages.',

            '.count_number_of_leftovers()': 'Get count of number of titles that were not identified across all '
                                            'Wiki pates.',
        }

        for command, description in info.items():
            print(f'{command}: {description}')

    def run_all(self):
        self._fetch_all_categories()
        self._split_titles_into_lists()
        self._make_master_lists()

        print(f'Total count of titles identified: {len(self.all_dataset_titles)}')
        print(f'Total missing films: {len(self.leftovers)}')

    def _split_titles_into_lists(self):
        self.dataset_split_dict['Standup'] = self._split_data(self.nf_titles, self.results_dict['Standup'])
        self.dataset_split_dict['Distribution'] = self._split_data(self.nf_titles, self.results_dict['Distribution'])

        self.dataset_split_dict['Films'] = dict()
        for year, titles in self.results_dict['Films'].items():
            self.dataset_split_dict['Films'][year] = self._split_data(self.nf_titles, titles)

    def _make_master_lists(self):
        total_list = self.results_dict['Standup'] + self.results_dict['Distribution']
        [total_list.extend(item) for item in list(self.results_dict['Films'].values())]
        self.all_wiki_titles = [str(item) for item in total_list]

        all_items = self.dataset_split_dict['Standup'] + self.dataset_split_dict['Distribution']
        [all_items.extend(item) for item in list(self.dataset_split_dict['Films'].values())]
        self.all_dataset_titles = [str(item) for item in all_items]

        self.leftovers = [item for item in self.nf_titles if item not in self.all_dataset_titles]

    def count_number_identified(self):
        return len(self.all_dataset_titles)

    def count_number_of_leftovers(self):
        return len(self.leftovers)

    def print_all_counts(self):
        print('Counts across dataset_split_dict:\n')
        print(f'Standup: {len(self.dataset_split_dict["Standup"])} titles\n')
        print(f'Distribution: {len(self.dataset_split_dict["Distribution"])} titles\n')
        print(f'Films:')

        for key, data in self.dataset_split_dict['Films'].items():
            print(f'\t{key}: {len(data)} Films')

        print(f'\nLeftovers: {len(self.leftovers)}')

    def _fetch_all_categories(self):
        self.results_dict['Standup'] = self._get_titles_from_wiki(self.standup_url)
        self.results_dict['Distribution'] = self._get_titles_from_wiki(self.distribution_url)

        self.results_dict['Films'] = dict()
        for year, url in self.movie_urls.items():
            self.results_dict['Films'][year] = self._get_titles_from_wiki(url)

    @staticmethod
    def _find_missing(dataset_list, wiki_list):
        slug_wiki_list = [slugify(str(item)) for item in wiki_list]
        matches = [item for item in dataset_list if slugify(str(item)) not in slug_wiki_list]
        return matches

    @staticmethod
    def _split_data(dataset_list, wiki_list):
        slug_wiki_list = [slugify(str(item)) for item in wiki_list]
        return [item for item in dataset_list if slugify(str(item)) in slug_wiki_list]

    @staticmethod
    def _get_titles_from_wiki(url):
        return list(pd.concat(pd.read_html(url)).Title.unique())
