
from pywikiapi import Site
import re
import pandas as pd
from pywikiapi import ApiError
site = Site('http://wikipast.epfl.ch/wikipast/api.php')


def connect():
    user = 'Zouaoui@Che'
    password = 'c6thfl7oqrpgrlbpp2oa151jt6vl2mck'
    site.no_ssl = True  # remove https
    site.login(user, password)  # to log in


def get_wiki_text(page, section=None):
    result = site('parse', page=page, prop=['wikitext'], section=section)
    return result['parse']['wikitext']


def input_character(data_bottin):
    address = data_bottin['street_clean'][0]
    job = data_bottin['job_lower'][0]
    name = data_bottin['name'][0]
    title = '{} - {} ({})'.format(name, job, address)
    text = []
    years = []

    for index, line in data_bottin.iterrows():
        year = line['year']
        number = line['number']
        url = line['url']
        text.append(
            f'*[[{year}]] / Paris, {number} [[{address}]]. [[{name}]] est mentionné dans la catégorie [[{job}]]. [{url}] <br /> \n')
        years.append(int(year))

    try:
        site('edit', title=title, text="".join(text), token=site.token(), createonly=True)
        desambiguation(name, title)

    except ApiError as err:
        print('I am inside the exception')
        if err.data['code'] == 'articleexists':
            for year, input_text in zip(years, text):
                sort_year(title, year, input_text)
            return

    except Exception as err:
        print('Error :', err)


def sort_year(page_name, year, text):
    old_text = get_wiki_text(page_name)

    # When page is empty, just add content
    if not old_text:
        site('edit', title=page_name, text=text, token=site.token())
        return

    test_string = old_text.split("\n")

    test_string = [x for x in test_string if x.strip().startswith("*")]
    # Page does not contain any valid datafication entries
    if not test_string:
        site('edit', title=page_name, text=text, token=site.token())
        return

    temp = [None] * len(test_string)
    res = [None] * len(test_string)
    foo = False

    for i in range(len(test_string)):
        temp[i] = re.findall(r'\d+', test_string[i])
        res[i] = list(map(int, temp[i]))
    current_year = 0

    for i in range(len(res)):
        if year <= res[i][0]:
            current_year = i
            foo = True
            break
        current_year = i

    previous_line = test_string[current_year]

    if (current_year >= len(res) - 1) and (not foo):  # add after, append
        old_text = old_text.replace(previous_line, previous_line + '\n' + text, 1)
    else:
        old_text = old_text.replace(previous_line, text + '\n' + previous_line, 1)
    site('edit', title=page_name, text=old_text, token=site.token())


def desambiguation(name, page_name):
    title = name + '(homonymie)'
    intro_text = f'{name} est le nom de : <br /> \n'
    input_text = f'\n* [[{page_name}]] <br />'

    homonymie = f' Pour les articles homonymes, voir [[{title}]] \n'
    site('edit', title=page_name, prependtext=homonymie, token=site.token())

    try:
        site('edit', title=title, text=intro_text, token=site.token(), createonly=True)
        site('edit', title=title, appendtext=input_text, token=site.token())

    except ApiError as err:
        if err.data['code'] == 'articleexists':
            site('edit', title=title, appendtext=input_text, token=site.token())
    except Exception as err:
        print('Error :', err)



