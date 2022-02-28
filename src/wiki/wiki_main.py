from src.wiki.wiki_models import WikiAnalyzer, WIKI_URLS
import json


def wiki_main():
    with open('netflix_nametags.json', 'r') as file:
        titles_list = [item['title'] for item in json.load(file)]

    wiki_obj = WikiAnalyzer(titles_list, WIKI_URLS)
    data_output = wiki_obj.run_all()

    with open('wiki_output.json', 'w+') as outfile:
        json.dump(data_output, outfile)

    print('Wiki Data Retrieved.\n')


if __name__ == '__main__':
    wiki_main()
