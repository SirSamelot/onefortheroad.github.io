---
layout: post
title:  "Tidying Data"
subtitle:   "a simple example with text data"
date:   2017-05-12 14:41:03
author:     "Sam Wong"
header-img: "img/2017-05-12-tidying-data.jpg"
categories: python pandas tutorial
comments: true
---
# Introduction
Hello!  In this tutorial, we will learn ways to use *pandas* to clean a dataset.  Our ultimate goal is a tidy dataset. We will cover:

- What is tidy data?
- Cleaning text data


At the end of [Part 2]({% post_url 2017-05-10-web-scraping-part-2 %}) we had a dataframe with a list of all the Canadian brewers on [this](https://en.wikipedia.org/wiki/List_of_breweries_in_Canada) Wikipedia page. However, we already know there are some problems with the dataset, and I'm sure we will uncover a few more as we explore it in more detail.  Let's go!

## Contents

1. [What is tidy data](#1-what-is-tidy-data)
2. [Our (messy) data](#2-our-messy-data)
3. [Unpacking a list](#3-unpacking-a-list)
4. [Cleaning text strings](#4-cleaning-text-strings)
5. [Trivia](#5-trivia)
6. [Conclusion](#conclusion)

# 1. What is tidy data?
The term **tidy data** was popularized by Hadley Wickham in a 2014 paper, [Tidy Data](https://www.jstatsoft.org/article/view/v059i10).  This paper is essential reading for anyone working in data science. According to Wickham, a tidy dataset is one in which:
>  each variable is a column, each observation is a row, and each type of observational unit is a table
{:.blockquote}

Further, a tidy dataset is easy for computers to manipulate, model, and visualize.  These are all worthy goals that make a data scientist's life easier, so we should always seek to tidy our data.  Let's take a look at our dataset.

# 2. Our (messy) data


```python
import pandas as pd
from ast import literal_eval

filename = './data/breweries_in_canada_messy.csv'
df = pd.read_csv(filename, index_col=[0], converters={"city": literal_eval}, encoding='ISO-8859-1')

print(df.head(), df.tail(), sep='\n'*2)
```

             city                         name province
    0  [Edmonton]    Alley Kat Brewing Company  Alberta
    1  [Edmonton]      Amber's Brewing Company  Alberta
    2   [Calgary]  Banded Peak Brewing Company  Alberta
    3     [Banff]       Banff Ave. Brewing Co.  Alberta
    4  [Edmonton]       Bent Stick Brewing Co.  Alberta

                                    city                    name province
    501               [Sapporo, Chambly]                Unibroue   Quebec
    502  [Jonquière, Chicoutimi, Québec]          La Voie Maltée   Quebec
    503   [Quebec City, Laval, Brossard]        Les 3 Brasseurs,   Quebec
    504                     [Whitehorse]       Yukon Brewing Co.    Yukon
    505                     [Whitehorse]  Winterlong Brewing Co.    Yukon


There are a few wrinkles we have to contend with when reading our data file.  They are the result of us calling the `to_csv()` function with no arguments when we originally created the CSV file.

- The `index` column was explicitly created as a column in the CSV file.  So to treat it as a proper `index` and not another column of data, we pass in the parameter `index_col=[0]` so *pandas* knows the first column is an index column.
- When we wrote the column `city`, we passed in the list object directly.  Once in CSV form, it is no longer a list object but a string.  So to tell *pandas* that the `city` column is actually full of list objects and not strings, we call in a converter that tell is to "literally evaluate" the contents.  Thus we get our column of list objects back.
- For some reason, the default file encoding used when writing the CSV file can't be used to read the CSV file again.  So we explicitly pass in `encoding='ISO-8859-1'` in order to read the file correctly.

The first problem with our data is that the every value in the `city` variable is a list object.  This is a byproduct of how we scraped the data (see [Web Scraping: Part 2]({% post_url 2017-05-10-web-scraping-part-2 %}).  *pandas* has trouble accessing contents of a list, so we wouldn't be able to use its powerful features for analysis.  Also, some list objects have multiple contents, which means this fails the criteria for tidy data. So the first thing we will do is unpack these list objects and create separate rows for multi-city breweries.

# 3. Unpacking a list
Let's take a look at one of our problem rows, the brewery by the name of *La Voie Maltée*.


```python
print(df[df.name=='La Voie Maltée'])
```

                                    city            name province
    502  [Jonquière, Chicoutimi, Québec]  La Voie Maltée   Quebec


It has three cities listed in its `city` variable.  So ideally, we want to create three new rows, one for each city.  I'll admit this took me a while to figure out, but [cwharland](http://stackoverflow.com/users/1968405/cwharland) came up with a lovely one-liner.  Take a look [here](http://stackoverflow.com/questions/28442358/splitting-a-list-inside-a-pandas-dataframe) to see the full explanation.


```python
df = df.groupby(['name', 'province']).city.apply(lambda x: pd.DataFrame(x.values[0])).reset_index().drop('level_2', axis = 1)
df.columns = ['name', 'province', 'city']  # rename the variables after above operation
print(df[df.name=='La Voie Maltée'])
```

                   name province        city
    257  La Voie Maltée   Quebec   Jonquière
    258  La Voie Maltée   Quebec  Chicoutimi
    259  La Voie Maltée   Quebec      Québec


Much better!

# 4. Cleaning text strings
Again, just from looking at `.tail()`, I can see that the brewery *Les 3 Brasseurs,* has a comma at the end of their name.  Not all punctuation at the end of a name is bad (for example, *Banff Ave. Brewing Co.* or *Dieu du ciel!*) but commas definitely are.  Just curious, how many breweries have undesirable punctuation at the end of their name?


```python
pattern = r'[^\w!.]$'  # pattern to find end of string isn't a letter, comma, nor exclamation mark
print(df[df.name.str.contains(pattern)])
```

                           name          province         city
    54   Big Ridge Brewing Co.]  British Columbia       Surrey
    115             C'est What?           Ontario      Toronto
    275        Les 3 Brasseurs,            Quebec  Quebec City
    276        Les 3 Brasseurs,            Quebec        Laval
    277        Les 3 Brasseurs,            Quebec     Brossard


Only 5 rows, not as bad as I thought.  We even found an unexpected character, `]`, hiding in there.  And *C'est What?* is actually a legitimate name, so really only 4 entries that need to be fixed.  Let's get rid of those unwanted characters:


```python
pattern = r'[^\w!.?]$'  # pattern to find last character is undesired character
df.name = df.name.str.replace(pattern, '')
print(df[df.name.str.contains(pattern)])
```

    Empty DataFrame
    Columns: [name, province, city]
    Index: []


Let's save our dataframe for future use.


```python
filename = './data/breweries_in_canada_clean.csv'
df.to_csv(filename, index=False, columns=['name', 'city', 'province'], encoding='utf-8')
```

# 5. Trivia
Already we can use our data for some simple observations.

### Observation 1


```python
print(df.describe())
```

                      name province     city
    count              509      509      509
    unique             496       12      259
    top     La Voie Maltée  Ontario  Toronto
    freq                 3      211       46


There are 496 breweries in 259 cities.

### Observation 2


```python
print(df.province.value_counts(ascending=False))
```

    Ontario                    211
    British Columbia           103
    Quebec                      90
    Alberta                     39
    Newfoundland & Labrador     19
    Nova Scotia                 15
    Manitoba                    10
    Saskatchewan                 8
    New Brunswick                6
    Prince Edward Island         5
    Yukon                        2
    Northwest Territories        1
    Name: province, dtype: int64


Ontario leads the way with more than twice the number of breweries than the next province on the list.

### Observation 3


```python
print(df.city.value_counts(ascending=False)[:5])
```

    Toronto       46
    Vancouver     24
    Ottawa        22
    Calgary       15
    St. John's    11
    Name: city, dtype: int64


The top 5 cities with the most breweries are Toronto, Vancouver, Ottawa, Calgary, and St. John's.  (Although this one is misleading as many of the breweries listed under St. John's don't exist anymore.)

# Conclusion
We now have a dataframe that is much better than before.  However, there are still some problems. For example:
- some entries are duplicates (e.g. Labatt & Labatt Brewing)
- some entries from the Wikipedia page were removed if their city information was written like so: "CrossRoads Brewing (Prince George - Opening in 2017)
- some entries have incorrect or invalid city information (e.g. *defunct* for Agassiz Brewing)
- some of the breweries don't exist anymore

You can see some of the inherent fallacies in scraping and cleaning textual data from a web page.  It's an inexact science and requires a lot of work to build a robust scraper, not to mention validating the resulting data.  But even with our imperfect dataset, we picked out some interesting trivia.

Note that we didn't cover very common and important topics like dealing with **missing data** and **normalizing data**.  We'll talk about these in a future tutorial when we work with numeric data sets.

I do think we have enough information to use with our Top 100 Beer list (from [Web Scraping: Part 1]({% post_url 2017-04-29-web-scraping-part-1 %}) so we'll leave this dataframe as is.  Our next tutorial will show how to **join dataframes**, and later we'll show an example of **data visualization**.  Until then, cheers!

> Have a question about this topic, or a suggestion for a future topic?  Please, leave a comment below!
{:.blockquote}
