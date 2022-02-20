from src.wiki.wiki_models import WikiAnalyzer, WIKI_URLS
import json


if __name__ == '__main__':
    with open('final_nf_dict.json', 'r') as file:
        titles_list = json.load(file).keys()
    wiki_obj = WikiAnalyzer(titles_list, WIKI_URLS)
    wiki_obj.run_all()