
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from editdistance import distance
from urllib.parse import quote
from collections import Counter
import argparse
import frontend
import pickle

doc2start = {"bpt6k63243601": 123, "bpt6k62931221": 151, "bpt6k6286466w": 189, "bpt6k6393838j": 219, "bpt6k6331310g": 216, "bpt6k6292987t": 353, "bpt6k62906378": 288, "bpt6k6391515w": 319, "bpt6k6315927h": 349, "bpt6k6319106t": 324, "bpt6k6315985z": 82, "bpt6k63959929": 82, "bpt6k63197984": 56, "bpt6k6389871r": 77, "bpt6k6319811j": 79, "bpt6k6282019m": 72, "bpt6k6314752k": 190, "bpt6k6305463c": 113, "bpt6k6318531z": 108, "bpt6k6324389h": 72, "bpt6k63243920": 80, "bpt6k6309075f": 96, "bpt6k6333200c": 132, "bpt6k63243905": 134, "bpt6k6333170p": 137, "bpt6k96727875": 135, "bpt6k9764746t": 99, "bpt6k97645375": 123, "bpt6k9672117f": 125, "bpt6k9763554c": 123, "bpt6k9763553z": 105, "bpt6k9677392n": 110, "bpt6k9692809v": 113, "bpt6k9762929c": 129, "bpt6k9672776c": 119, "bpt6k9764647w": 121, "bpt6k9669143t": 145, "bpt6k9677737t": 139, "bpt6k9668037f": 167, "bpt6k96839542": 171, "bpt6k96762564": 185, "bpt6k9685861g": 189, "bpt6k9763471j": 153, "bpt6k9762899p": 157, "bpt6k97630871": 11, "bpt6k9684454n": 235, "bpt6k9732740w": 239, "bpt6k9684013b": 189, "bpt6k9692626p": 305, "bpt6k9685098r": 281, "bpt6k9764402m": 329, "bpt6k97631451": 322, "bpt6k9776121t": 49, "bpt6k9775724t": 33, "bpt6k97774838": 327, "bpt6k9780089g": 339}

def entry2url(row):
    """
    Takes a row of an Annuaire csv and
    transforms it to the corresponding Gallica url
    """
    url = "https://gallica.bnf.fr/ark:/12148/"

    directory = row['directory']
    page = row['page'] - doc2start[directory]
    url += f"{row['directory']}/f{row['page'] - doc2start[row['directory']]}"

    r_strings = []
    if 'name' in row and pd.notna(row['name']):
        r_strings.append(quote(row['name'].replace('.', ' ')))
    if 'job' in row and pd.notna(row['job']):
        r_strings.append(quote(row['job'].replace('.', ' ')))
    if 'street' in row and pd.notna(row['street']):
        r_strings.append(quote(row['street'].replace('.', ' ')))
    if 'number' in row and pd.notna(row['number']):
        r_strings.append(quote(row['number'].replace('.', ' ')))

    if len(r_strings) > 0:
        url += f".item.r={'%20'.join(r_strings)}.zoom"

    return url


def add_clickable_url(bottin_dataframe):
    bottin_dataframe = bottin_dataframe.copy()
    bottin_dataframe['url'] = bottin_dataframe.apply(entry2url, axis=1)

    def make_clickable(val):
        return '<a href="{}">gallica url</a>'.format(val, val)

    return bottin_dataframe.style.format(make_clickable, subset=['url'])


def clean_up(df, threshold, field):
    '''
        Homogenises a field of the data frame by replacing similar entries with a canonical form.
        That's defined to be the most repeated form withing that similar group

        Parameters:
            df              The bottin pandas dataframe to be cleaned.
            threshold       A float (0-1] representing the maximum relative distance for 2 strings to be considered similar
            field           A string containing the name of the field to be cleaned up. The field must be string-valued

        returns:
            clean_df        The cleaned up dataframe
    '''

    clean_df = df.copy()
    series = pd.Series(df[field].unique())
    counts = series.value_counts(sort=True)
    for i,str1 in enumerate(series):
        for str2 in series[i+1:]:
            dist = distance(str1,str2)/2*(len(str1) + len(str2))
            if (dist > 0) and (dist <= threshold):
                if counts[str2] < counts[str1]:
                    canon = str1
                    abr = str2
                else:
                    canon = str2
                    abr = str1
                clean_df.replace(to_replace=abr,value=canon,inplace=True)

    return clean_df


def split_frame(df, split_criteria,output_list):
    if not split_criteria:
        output_list.append(df)
        return output_list
    else:
        gb = df.groupby(split_criteria[0])
        for val in df[split_criteria[0]].unique():
            df_split = gb.get_group(val)
            output_list = split_frame(df_split,split_criteria[1:],output_list)
        return output_list





# Load data
data_bottin = pd.read_csv('./bottin_data_groupe_1.csv').dropna()

'''data_bottin['job_lower'] = data_bottin['job'].copy()
data_bottin['job_lower'].str.lower()
filter = '^\s*\w+(?:\s?\(.*\)\s*)?\s*$'
treated = data_bottin['name'].str.match(filter)
print('Avant le nettoyage{}'.format(len(data_bottin['street_clean'].unique())))
data_bottin = clean_up(data_bottin,0.2,'street_clean')
print('Après le nettoyage{}'.format(len(data_bottin['street_clean'].unique())))
data_bottin.to_csv('Clean_group_1')
exit(0)
df_one_word = data_bottin.loc[treated].copy()
data_bottin = data_bottin.loc[~treated]

'''
clean = pd.read_csv('./Clean_group_1')

#gb_name = df_one_word.groupby('name')
lst_lil_frames = split_frame(clean,['name', 'job_lower'],[])

for lil_frame in lst_lil_frames:

    print(lil_frame.to_string(header=False))
    print('-'*20)


'''np.random.seed(0)
lst = np.random.choice(split_frame(clean,['name', 'street_clean', 'job', 'number'],[]),20)
for series in lst:
    print(series.to_string())'''
#lil_frame['url'] = lil_frame.apply(entry2url, axis=1)