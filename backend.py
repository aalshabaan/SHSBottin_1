
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
    series = df[field]
    counts = df[field].value_counts(sort=True)
    unique = series.unique()

    for i, str1 in enumerate(unique):
        for str2 in unique[i+1:]:
            dist = 2*distance(str1, str2)/(len(str1) + len(str2))
            if (dist > 0) and (dist <= threshold):
                if counts[str2] < counts[str1]:
                    canon = str1
                    abr = str2
                else:
                    canon = str2
                    abr = str1
                series.replace(to_replace=abr, value=canon, inplace=True)

    clean_df[field] = series
    return clean_df


def split_frame(df, split_criteria, output_list):
    if not split_criteria:
        df.sort_values('year', inplace=True)
        output_list.append(df)
        return output_list
    else:
        gb = df.groupby(split_criteria[0])
        for val in df[split_criteria[0]].unique():
            df_split = gb.get_group(val)
            output_list = split_frame(df_split, split_criteria[1:], output_list)
        return output_list

def clean_number(df):
    df['number'] = df['number'].str.strip('.')
    # print(df)
    return df


def clean_chars(df):
    target_chars = '*#¥<>~/\\'
    for char in target_chars:
        df['name'] = df['name'].str.replace(char, '')
    return df


def main_process(pargs):
    # Load data
    filename = pargs.file_name
    preprocess = pargs.pre_process

    if preprocess:
        data_bottin = pd.read_csv(filename).dropna()
        print('Initial count :', data_bottin.shape[0])
        data_bottin['job_lower'] = data_bottin['job'].copy()
        data_bottin['job_lower'].str.lower()
        data_bottin['url'] = data_bottin.apply(entry2url, axis=1)
        names = []
        clean_streets = clean_up(data_bottin, 0.2, 'street_clean')
        clean_streets = clean_number(clean_streets)
        lil_frames = split_frame(clean_streets, ['street_clean'], [])
        for frame in lil_frames:
            frame = clean_up(frame, 0.2, 'job_lower')
            very_lil_frames = split_frame(frame, ['job_lower'], [])
            for street_job in very_lil_frames:
                street_job = clean_up(street_job, 0.1, 'name')
                street_job = clean_chars(street_job)
                names = split_frame(street_job, ['name'], names)
            # frame = very_lil_frames[0].append(very_lil_frames[1:])
        # clean_frame = lil_frames[0].append(lil_frames[1:])
    # for name in names[:100]:
    #     print(name.to_string(header=False))
    #     print('-'*50)


        with open('save.pkl', 'wb+') as file:
            pickle.dump(names, file)
    else:
        # retieve from pickle
        with open(filename, 'rb') as file:
            names = pickle.load(file)

    frontend.connect()

    for i,person in enumerate(names):
        try:
            frontend.input_character(person)
        except KeyError as err:
            print(i,person,err)
            exit(1)
    print('Pages created :', len(names))
    print('Export finished')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--file_name',
                        required=True,
                        type=str,
                        help='Location to the file containing entries to be uploaded to wikipast\n'
                             'Either a CSV if preprocessing is required or a pre-processd pickle'
                        )

    parser.add_argument('--pre_process',
                        required=True,
                        type=int,
                        help='Indicate if pre-processing (clean-up) needs to be done, 0 if already pre-processed'
                        )

    args = parser.parse_args()

    main_process(args)
