from wikibaseintegrator import WikibaseIntegrator
import json
import requests
from wikibaseintegrator import wbi_helpers
from tqdm import tqdm
wbi = WikibaseIntegrator()


def get_class_articles_amount() -> list[tuple]:
    """
    Inputs wikidata id of class entity (e.g. `"Q3314483"` "fruit").
    Outputs `list` of `tuples` (member, article_amount) like `('apple', 123)`.
    """

    output = []

    query = """
        SELECT ?item
        WHERE
        {
        ?item wdt:P279 wd:Q402885 .
        }
    """

    result = wbi_helpers.execute_sparql_query(query)

    fruit_list = [binding['item']["value"].strip(
        "http://www.wikidata.org/entity/") for binding in result['results']['bindings']]

    for i in tqdm(fruit_list):
        # print(f"http://www.wikidata.org/entity/{i}")
        res = requests.get(f"http://www.wikidata.org/entity/{i}")
        d = json.loads(res.text)
        
        output.append((i, len(d["entities"][i]["labels"])))

    return sorted(output, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    with open("Q402885.txt", 'w') as f:
        for i in get_class_articles_amount():
            f.write(str(i)+'\n')
    # print(get_class_articles_amount("Q3314483"))

# find like a threshold to get only cats, dogs and birds when asking an animal