import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# Load data
data_bottin = pd.read_csv('./bottin_data_groupe_1.csv')
'''
sample = data_bottin.head(10)
# print(sample.to_string())
'''
'''
entries_number = data_bottin.shape[0]
entries_per_year = data_bottin.groupby('year').size()
unique_names_number = data_bottin['name'].unique().size
unique_jobs_number = data_bottin['job'].unique().size
unique_streets_number = data_bottin['street'].unique().size

print()
print(f"Il y {entries_number} entrées, dont {unique_names_number} noms uniques, {unique_jobs_number} métiers uniques, {unique_streets_number} rue uniques")
print("\nLa distribution d'entrées par année est la suivante:")
print("\n".join([f"\t{year}: {count}" for year, count in entries_per_year.reset_index().values]))


data_bottin.groupby('year').size().plot(kind='bar',
                                        title='Entries per year',
                                        figsize=(8, 5)).set_ylabel('Number of entries')
plt.savefig('Entries_per_year.png')
plt.show()

data_bottin['name'].value_counts().plot(kind='hist',
                                        loglog=True,
                                        bins=1000,
                                        title='Distribution of duplicate names',
                                        figsize=(8, 5)).set_xlabel('Number of duplicates')
plt.savefig('Duplicates.png')
plt.show()


data_bottin['job'].value_counts().plot(kind='hist',
                                       loglog=True,
                                       bins=1000,
                                       title='Distribution of duplicate jobs',
                                       figsize=(8, 5)).set_xlabel('Number of duplicates')
plt.show()

'''
# Filter only words with

filter = '^\s*\w+(?:\s?\(.*\)\s*)?\s*$'
predicate = data_bottin['name'].str.match(filter)
data_bottin_one_word = data_bottin.loc[predicate].copy()

one = data_bottin_one_word.groupby(['name', 'job', 'street_clean', 'number']).size().sort_values(ascending=False).value_counts().to_frame('Count').rename_axis('Number of duplicates')

print(one.head(10).to_string())
exit()

regex_one_word = '^\s*\w+(?:\s?\(.*\)\s*)?\s*$'

predicate_one_word = data_bottin['name'].str.match(regex_one_word)

data_bottin_one_word = data_bottin.loc[predicate_one_word].copy()
nb_one_word = data_bottin_one_word['name'].size
nb_word = data_bottin['name'].size
percent_one_word = nb_one_word / nb_word * 100
print('One word + parenthesis : {}/{} ({:2f}%)'.format(nb_one_word, nb_word, percent_one_word))

# print(', '.join([e for e in data_bottin.loc[~predicate_one_word]['name']]))

regex_parens = '^.*?\((.*)\).*?$'

name_parens = data_bottin['name'].str.extract(regex_parens).dropna()[0]



name_parens_split = name_parens.str.split('\W')
name_parens_split = name_parens_split.apply(lambda words: [word for word in words if len(word) > 0])

word_counts = Counter()

for words in name_parens_split.values:
    word_counts.update(words)

word_counts.most_common(10)

name_one_word_split = data_bottin.loc[~predicate_one_word]['name'].str.split('\W')
name_one_word_split = name_one_word_split.apply(lambda words: [word for word in words if len(word) > 0])

word_counts = Counter()

for words in name_one_word_split.values:
    word_counts.update(words)

data_bottin.groupby(['name', 'job', 'street', 'number']).size().sort_values(ascending=False).value_counts().to_frame('Count').rename_axis('Number of duplicates')

data_bottin['number_clean'] = data_bottin['number'].str.extract('(^\d+(?: ?bis)?).*')
data_bottin.groupby(['name', 'job', 'street_only', 'number_clean']).size().sort_values(ascending=False).value_counts().to_frame('Count').rename_axis('Number of duplicates')
