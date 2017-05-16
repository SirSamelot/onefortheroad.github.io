---
layout: post
title:  "Merging Data"
subtitle:   "when two become one"
date:   2017-05-16 12:02:06
author:     "Sam Wong"
header-img: "img/2017-05-16-merging-data.jpg"
categories: pandas tutorial
comments: true
---
# Introduction
Hello! In this tutorial we will show how to **combine data** from two different sources.  In the real world, you will almost always have to work with data from multiple sources, so it's necessary to know how to combine data into a single source for ease of analysis.

The data we'll be using comes from our tutorials on **web scraping** ([here]({% post_url 2017-04-29-web-scraping-part-1 %}) and [here]({% post_url 2017-05-10-web-scraping-part-2 %})).  The first dataset is a list of the Top 100 Beers from Canada.  The second dataset is a list of all the breweries in Canada.  We'll find and fix some common problems when joining data.  In the next tutorial, we'll take the combined data and do some fun visualizations.  Ready?

## Contents
1. [Read Data](#1-read-data)
2. [Join Data](#2-join-data)
3. [Fixing Join Problems](#3-fixing-join-problems)
4. [Matching Text Strings](#4-matching-text-strings)
5. [Fixing NaN Values](#5-fixing-nan-values)
6. [Cleanup](#6-cleanup)
7. [Conclusion](#conclusion)

# 1. Read Data
Let's get the datasets from the CSV files we saved before.  We'll take a peek at them to refresh ourselves on their contents.


```python
import pandas as pd

pd.set_option('display.width', 1000)  # Display wide dataframes as one

top_100_filename = './data/top_100_canadian_beers.csv'
breweries_filename = './data/breweries_in_canada_clean.csv'

df1 = pd.read_csv(top_100_filename, encoding='ISO-8859-1')
df2 = pd.read_csv(breweries_filename)

print(df1.head(), df2.head(), sep='\n\n')
```

       rank                                      name                  brewery                             style   abv  score  ratings
    0     1                              Péché Mortel  Brasserie Dieu du Ciel!  American Double / Imperial Stout   9.5   4.39     5087
    1     2  Péché Mortel En Fût De Bourbon Américain  Brasserie Dieu du Ciel!  American Double / Imperial Stout   9.5   4.45      488
    2     3                           La Fin Du Monde                 Unibroue                            Tripel   9.0   4.31    10021
    3     4                Unibroue 17 Grande Réserve                 Unibroue           Belgian Strong Dark Ale  10.0   4.24     1140
    4     5                               Fat Tug IPA        Driftwood Brewery                      American IPA   7.0   4.25      601

                                name            city          province
    0          "A" Frame Brewing Co.        Squamish  British Columbia
    1              20 Valley Brewery  St. Catherines           Ontario
    2           33 Acres Brewing Co.       Vancouver  British Columbia
    3          5 Paddles Brewing Co.          Whitby           Ontario
    4  9 Mile Legacy Brewing Company       Saskatoon      Saskatchewan


# 2. Join Data
Now that our datasets are in dataframes, we can join them with `pd.merge()`.  What I'd like to do is add the city and province variables from `df2` to the corresponding brewery in `df1`.  So our end result should be a dataframe of the Top 100 Beers of Canada, with each beer having its original data plus its city and province of origin.


```python
df = pd.merge(df1, df2, how='left', left_on='brewery', right_on='name', suffixes=('_beer', '_brewery'), sort=False)
print("df is length {}".format(len(df)))
print(df.head())
```

    df is length 109
       rank                                 name_beer                  brewery                             style   abv  score  ratings name_brewery     city province
    0     1                              Péché Mortel  Brasserie Dieu du Ciel!  American Double / Imperial Stout   9.5   4.39     5087          NaN      NaN      NaN
    1     2  Péché Mortel En Fût De Bourbon Américain  Brasserie Dieu du Ciel!  American Double / Imperial Stout   9.5   4.45      488          NaN      NaN      NaN
    2     3                           La Fin Du Monde                 Unibroue                            Tripel   9.0   4.31    10021     Unibroue  Sapporo   Quebec
    3     3                           La Fin Du Monde                 Unibroue                            Tripel   9.0   4.31    10021     Unibroue  Chambly   Quebec
    4     4                Unibroue 17 Grande Réserve                 Unibroue           Belgian Strong Dark Ale  10.0   4.24     1140     Unibroue  Sapporo   Quebec


This doesn't look quite right!
- Why is our merged dataframe length 109?  We were expecting length 100
- What's with the NaN values?
- Why is *La Fin Du Monde* repeated?

Without even looking at the rest of the dataframe, we can tell something is wrong.  But if we stop and think about the datasets we just merged, then it becomes apparent what the problems are.

# 3. Fixing Join Problems

### Problem 1: Duplicate values
Remember how we created our dataset of breweries in Canada (`df2`)?  We scraped a Wikipedia page and noticed that some breweries had multiple cities listed as their location.  This could explain why a beer like *La Find Du Monde* was repeated, as the only difference between the two rows in our merged dataframe is the city.  Let's check:


```python
print(df2[df2.name=='Unibroue'])
```

             name     city province
    477  Unibroue  Sapporo   Quebec
    478  Unibroue  Chambly   Quebec


That does match up with the two rows corresponding to *La Fin Du Monde*.  Let's check if there are more of these duplicates, and if so, does the number of duplicates explain the extra 9 rows in the merged data set?


```python
print('Number of duplicate beers: ', df[df.duplicated(['name_beer'])].name_beer.count())
print(df[df.duplicated(['name_beer'], keep=False)])
```

    Number of duplicate beers:  9
        rank                   name_beer   brewery                    style   abv  score  ratings name_brewery     city province
    2      3             La Fin Du Monde  Unibroue                   Tripel   9.0   4.31    10021     Unibroue  Sapporo   Quebec
    3      3             La Fin Du Monde  Unibroue                   Tripel   9.0   4.31    10021     Unibroue  Chambly   Quebec
    4      4  Unibroue 17 Grande Réserve  Unibroue  Belgian Strong Dark Ale  10.0   4.24     1140     Unibroue  Sapporo   Quebec
    5      4  Unibroue 17 Grande Réserve  Unibroue  Belgian Strong Dark Ale  10.0   4.24     1140     Unibroue  Chambly   Quebec
    9      8              Trois Pistoles  Unibroue  Belgian Strong Dark Ale   9.0   4.20     4938     Unibroue  Sapporo   Quebec
    10     8              Trois Pistoles  Unibroue  Belgian Strong Dark Ale   9.0   4.20     4938     Unibroue  Chambly   Quebec
    15    13                     Maudite  Unibroue  Belgian Strong Dark Ale   8.0   4.17     4573     Unibroue  Sapporo   Quebec
    16    13                     Maudite  Unibroue  Belgian Strong Dark Ale   8.0   4.17     4573     Unibroue  Chambly   Quebec
    18    15                 La Terrible  Unibroue  Belgian Strong Dark Ale  10.5   4.16     2216     Unibroue  Sapporo   Quebec
    19    15                 La Terrible  Unibroue  Belgian Strong Dark Ale  10.5   4.16     2216     Unibroue  Chambly   Quebec
    24    20                 Don De Dieu  Unibroue  Belgian Strong Pale Ale   9.0   4.13     2868     Unibroue  Sapporo   Quebec
    25    20                 Don De Dieu  Unibroue  Belgian Strong Pale Ale   9.0   4.13     2868     Unibroue  Chambly   Quebec
    44    39               La Résolution  Unibroue  Belgian Strong Dark Ale  10.0   4.09      270     Unibroue  Sapporo   Quebec
    45    39               La Résolution  Unibroue  Belgian Strong Dark Ale  10.0   4.09      270     Unibroue  Chambly   Quebec
    70    64                  Eau Benite  Unibroue                   Tripel   7.7   3.99      470     Unibroue  Sapporo   Quebec
    71    64                  Eau Benite  Unibroue                   Tripel   7.7   3.99      470     Unibroue  Chambly   Quebec
    78    71                La Fringante  Unibroue                   Tripel  10.0   4.12       81     Unibroue  Sapporo   Quebec
    79    71                La Fringante  Unibroue                   Tripel  10.0   4.12       81     Unibroue  Chambly   Quebec


What do you know, there are 9 duplicated beers, and from the list of duplicated beers, and it sure looks like the two cities listed for Unibroue are to blame.  This is easy enough to fix by removing one of the cities, but which one?  I could run upstairs and take a look in my fridge (I almost always have some version of Éphémère stocked), but a quick trip to Unibroue's [website](https://www.unibroue.com/en) also tells us the same thing: Unibroue is based in **Chambly**, Quebec.  *(If you're wondering where the Sapporo came from, Unibroue is now under the ownership of the beverage giant Sapporo.  Thanks Wikipedia for listing Sapporo as a location.)*


```python
df = df.drop_duplicates(['name_beer'], keep='last').reset_index(drop=True)
print("df is length {}".format(len(df)))
print('Number of duplicate beers: ', df[df.duplicated(['name_beer'])].name_beer.count())
print(df.head())
```

    df is length 100
    Number of duplicate beers:  0
       rank                                 name_beer                  brewery                             style   abv  score  ratings name_brewery     city province
    0     1                              Péché Mortel  Brasserie Dieu du Ciel!  American Double / Imperial Stout   9.5   4.39     5087          NaN      NaN      NaN
    1     2  Péché Mortel En Fût De Bourbon Américain  Brasserie Dieu du Ciel!  American Double / Imperial Stout   9.5   4.45      488          NaN      NaN      NaN
    2     3                           La Fin Du Monde                 Unibroue                            Tripel   9.0   4.31    10021     Unibroue  Chambly   Quebec
    3     4                Unibroue 17 Grande Réserve                 Unibroue           Belgian Strong Dark Ale  10.0   4.24     1140     Unibroue  Chambly   Quebec
    4     5                               Fat Tug IPA        Driftwood Brewery                      American IPA   7.0   4.25      601          NaN      NaN      NaN


That's better!  We have 100 rows without any duplicate beers, just like we expected.

### Problem 2: NaN values

Let's see how many observations have NaN in their `city` variable:


```python
print(df['city'].isnull().sum())
```

    46


Looks like nearly half of our beers don't have an associated city with them.  Why is this?  We know that all the breweries in the brewery dataset have city data, so why don't they show up in this merged dataframe?

The key word in the last sentence was *merged*.  Something happened when we joined the two datasets to cause the data in the second dataset to get left behind. An understanding of what happened when we issued our `merge()` will shed some light.

Recall how we called `merge()`:

```python
pd.merge(df1, df2, how='left', left_on='brewery', right_on='name', suffixes=('_beer', '_brewery'), sort=False)
```

We performed a *left join* using `brewery` from the left dataset `df1` and `name` from the right dataset `df2` as our common key.  In a *left join*, when a match can't be found between the left and right keys, then the variables from the right dataframe are filled with NaN!

So our merged dataset is telling us that **46/100** of the breweries from our beer dataset don't exist in our list of Canadian brewers.  That is a suspiciously high percentage, so something else is going on here.  In fact, the culprit is a very common problem when working with text data.  Since merges using strict equality matching, even a single difference in capitalization or punctuation will cause the merge to fail.  So when working with text data (especially text data from Wikipedia!), be prepared for all sorts of merge failures.

In our case, since we're dealing with names, it's going to be especially difficult to find matches.  But that's not going to stop us.

# 4. Matching Text Strings
Let's make an example of *Driftwood Brewery*, which had no strict match in the list of breweries.  Let's search our list of breweries for any breweries that have *driftwood* in their name.  We'll isolate the name variable and also convert to lowercase.


```python
breweries = df2['name'].str.lower()
breweries[breweries.str.contains('driftwood')]
```




    159    driftwood brewing co.
    Name: name, dtype: object



Look at that!  *Driftwood Brewery* in our beer list is actually *Driftwood Brewing Co.* in our list of breweries!  OK, I admit, I picked an easy one.  And there's no way we can do that manually for all 46 of our mislabeled breweries.  So we're going to use a python library, **difflib**, to help us with this task.

### difflib
We'll jump right into an example showing how to use the **difflib** library.


```python
from difflib import SequenceMatcher, get_close_matches

s1 = 'Brasserie Dieu du Ciel!'
s2 = 'Brasserie Dieu du ciel!'
s3 = 'Dieu du ciel!'
s4 = 'Brasserie Dunham'
s5 = 'Brasserie McAuslan'

print(round(SequenceMatcher(None, s1, s2).ratio(), 3))
print(round(SequenceMatcher(None, s1, s3).ratio(), 3))
print(round(SequenceMatcher(None, s1, s4).ratio(), 3))
print(round(SequenceMatcher(None, s1, s5).ratio(), 3))

print(get_close_matches(s1, [s2, s3, s4, s5]))
```

    0.957
    0.667
    0.615
    0.585
    ['Brasserie Dieu du ciel!', 'Dieu du ciel!', 'Brasserie Dunham']


`SequenceMatcher` can compare two strings and return a measure of the similarity (the `ratio()`) between the two strings.  According to the documentation, the rule of thumb is a ratio of **0.6 or higher** is a close match.  `s1` and `s2` are very similar with a ratio of 0.957.  `s1` and `s5` fall below the rule of thumb threshold.  And `s1` and `s4`, with a ratio of 0.615, would have given us a **false positive** (e.g. it would have considered *Brasserie Dunham* as similar enough to *Brasserie Dieu du Ciel!*).  However, if we compare against the entire list of breweries, and take the highest ratio (if a ratio > 0.6 is found), then we can be reasonably confident a correct match was found.

The method `get_close_matches()` returns a list of matches in order of descending similarity (with a default threshold of 0.6.)

Let's use **difflib** and see how accurate we are in matching our 46 breweries.

First create a list of all the beers where a matching brewery was not found:


```python
nan_breweries = df[df['name_brewery'].isnull()]
print(nan_breweries.head())
```

       rank                                 name_beer                            brewery                             style  abv  score  ratings name_brewery city province
    0     1                              Péché Mortel            Brasserie Dieu du Ciel!  American Double / Imperial Stout  9.5   4.39     5087          NaN  NaN      NaN
    1     2  Péché Mortel En Fût De Bourbon Américain            Brasserie Dieu du Ciel!  American Double / Imperial Stout  9.5   4.45      488          NaN  NaN      NaN
    4     5                               Fat Tug IPA                  Driftwood Brewery                      American IPA  7.0   4.25      601          NaN  NaN      NaN
    5     6            Red Racer IPA (India Pale Ale)  Central City Brewers + Distillers                      American IPA  6.5   4.23     1085          NaN  NaN      NaN
    9    10             Solstice D'été Aux Framboises            Brasserie Dieu du Ciel!                Berliner Weissbier  5.9   4.26      350          NaN  NaN      NaN


Now create a dataframe with the unique breweries to reduce the number of items we're processing.  With that shorter list we'll make a new column with the best matching brewery from `df2`. We'll also add a third column showing the similarity ratio as calculated by **difflib**.


```python
match_df = pd.DataFrame(nan_breweries['brewery'].unique(), columns=['brewery'])
match_df['match from df2'] = match_df['brewery'].apply(lambda x: get_close_matches(x, df2['name'], n=1)[0])
match_df['similarity'] = match_df.apply(lambda x: round(SequenceMatcher(None, x['brewery'], x['match from df2']).ratio(), 3), axis=1)
match_df = match_df.sort_values(by='similarity')
print(match_df)
```

                                  brewery            match from df2  similarity
    2   Central City Brewers + Distillers  Central City Brewing Co.       0.632
    5                   Le Trou Du Diable         La Mare au Diable       0.647
    3                    McAuslan Brewing            Rurban Brewing       0.733
    1                   Driftwood Brewery     Driftwood Brewing Co.       0.737
    6    Howe Sound Inn & Brewing Company    Howe Sound Brewing Co.       0.778
    8         Parallel 49 Brewing Company       Parallel 49 Brewing       0.826
    11          Amsterdam Brewing Company     Amsterdam Brewing Co.       0.870
    10         Lighthouse Brewing Company    Lighthouse Brewing Co.       0.875
    7                  Yellow Dog Brewing    Yellow Dog Brewing Co.       0.900
    9                        Crannóg Ales              Crannog Ales       0.917
    0             Brasserie Dieu du Ciel!   Brasserie Dieu du ciel!       0.957
    4            Microbrasserie Le Castor  Microbrasserie le Castor       0.958


Not bad!  Out of the 12 breweries without a strict match in our Canadian brewery list, **difflib** was able to find a good match for most of them.  There are only two, McAuslan Brewing and Le Trou Du Diable, that don't look quite right.  Looks like we'll have to manually fix those.

McAuslan Brewing corresponds to Brasserie McAuslan in our list of Canadian brewers `df2`.  We can change that in `match_df`.  But Le Trou Du Diable doesn't seem to correspond to anything on our list.  A quick web search show this brewer as based out of Shawinigan, Quebec, so we'll have to manually add this city and province.  For now, we'll set its corrected brewery as NaN so we can find it easily again later.

> Note that we are setting NaN using one of Python's built in methods for the NaN object.  The more orthodox method (for a data scientist, anyways) is to use NumPy's np.NaN.  But I didn't want to get into NumPy here.
{:.blockquote}


```python
match_df['corrected brewery'] = match_df['match from df2']
match_df.loc[match_df['brewery'] == 'McAuslan Brewing', 'corrected brewery'] = 'Brasserie McAuslan'
match_df.loc[match_df['brewery'] == 'Le Trou Du Diable', 'corrected brewery'] = float('NaN')
print(match_df)
```

                                  brewery            match from df2  similarity         corrected brewery
    2   Central City Brewers + Distillers  Central City Brewing Co.       0.632  Central City Brewing Co.
    5                   Le Trou Du Diable         La Mare au Diable       0.647                       NaN
    3                    McAuslan Brewing            Rurban Brewing       0.733        Brasserie McAuslan
    1                   Driftwood Brewery     Driftwood Brewing Co.       0.737     Driftwood Brewing Co.
    6    Howe Sound Inn & Brewing Company    Howe Sound Brewing Co.       0.778    Howe Sound Brewing Co.
    8         Parallel 49 Brewing Company       Parallel 49 Brewing       0.826       Parallel 49 Brewing
    11          Amsterdam Brewing Company     Amsterdam Brewing Co.       0.870     Amsterdam Brewing Co.
    10         Lighthouse Brewing Company    Lighthouse Brewing Co.       0.875    Lighthouse Brewing Co.
    7                  Yellow Dog Brewing    Yellow Dog Brewing Co.       0.900    Yellow Dog Brewing Co.
    9                        Crannóg Ales              Crannog Ales       0.917              Crannog Ales
    0             Brasserie Dieu du Ciel!   Brasserie Dieu du ciel!       0.957   Brasserie Dieu du ciel!
    4            Microbrasserie Le Castor  Microbrasserie le Castor       0.958  Microbrasserie le Castor


# 5. Fixing NaN Values

Now we will finally go back to our merged dataframe `df` and fix the NaN values. We'll use the index of `nan_breweries` to only modify the observations we identified earlier as having an unmatched brewery.

Using `match_df`, we can very quickly replace all the NaN values in `name_brewery` with the corrected brewery.  Then we can go back and replace the city and province of these corrected breweries with the location information in `df2`.  Finally, we manually enter the location (Shawinigan, Quebec) for our brewery that wasn't in the `df2`, Le Trou Du Diable.


```python
# Replace the unmatched breweries with the corrected ones
df.loc[nan_breweries.index, 'name_brewery'] = df['brewery'].replace(match_df.set_index('brewery')['corrected brewery'])

# REWRITE BELOW LINE TO ONLY AFFECT THE CORRECTED BREWERIES

# Update the city and province of the corrected breweries
df.loc[nan_breweries.index, 'city'] = df['name_brewery'].replace(df2.set_index('name')['city'])
df.loc[nan_breweries.index, 'province'] = df['name_brewery'].replace(df2.set_index('name')['province'])

# Manually enter city and province for the brewery Le Trou Du Diable
le_trou_du_diable = ['Le Trou Du Diable', 'Shawinigan', 'Quebec']
df.loc[df['brewery']=="Le Trou Du Diable", ['name_brewery', 'city', 'province']] = le_trou_du_diable
```

# 6. Cleanup
Now that our dataframe is complete, we'll do a bit of cleanup before saving the dataframe as a CSV.


```python
df = df.drop('name_brewery', axis=1)  # remove redundant variable
df = df.rename(columns={'name_beer': 'name'})
print(df.head())

filename = './data/top_100_canadian_beers_with_city.csv'
df.to_csv(filename, index=False, encoding='utf-8')
```

       rank                                      name                  brewery                             style   abv  score  ratings          city          province
    0     1                              Péché Mortel  Brasserie Dieu du Ciel!  American Double / Imperial Stout   9.5   4.39     5087  Saint-Jérôme            Quebec
    1     2  Péché Mortel En Fût De Bourbon Américain  Brasserie Dieu du Ciel!  American Double / Imperial Stout   9.5   4.45      488  Saint-Jérôme            Quebec
    2     3                           La Fin Du Monde                 Unibroue                            Tripel   9.0   4.31    10021       Chambly            Quebec
    3     4                Unibroue 17 Grande Réserve                 Unibroue           Belgian Strong Dark Ale  10.0   4.24     1140       Chambly            Quebec
    4     5                               Fat Tug IPA        Driftwood Brewery                      American IPA   7.0   4.25      601      Victoria  British Columbia


# Conclusion
Well done!  We've added location data for each of the breweries responsible for a beer on BeerAdvocate.com's Top 100 Beers from Canada.  In doing so, we touched on:
- Common problems when joining data from different sources
- Finding and fixing duplicate values
- Dealing with variations in text data
- Python's **difflib** library
- Slicing and dicing with *pandas*

We're now ready to explore this dataset.  Future tutorials will use this dataset to show how **insight** can be derived from **visualization**. Thanks for reading!

> Have a question about this topic, or a suggestion for a future topic?  Please, leave a comment below!
{:.blockquote}

### Resources
- Python's **difflib** [documentation](https://docs.python.org/3.6/library/difflib.html)
- *pandas* [Cookbook](http://pandas.pydata.org/pandas-docs/stable/cookbook.html), useful recipes
