---
layout: post
title:  "Web Scraping: Part&nbsp2"
subtitle:   "Adventures with Wikipedia"
date:   2017-05-10 20:18:03
author:     "Sam Wong"
header-img: "img/2017-05-10-web-scraping-part-2.jpg"
categories: tutorial python
comments: true
---
# Introduction
Hello!  In this tutorial we will scrape a more complicated page from Wikipedia.  This is a continuation of [Part 1]({% post_url 2017-04-29-web-scraping-part-1 %}) where we learned the basics of web scraping.

When we left off Part 1, we had a *pandas* dataframe containing the Top 100 Canadian Beers. I'd like to add some **geospatial** information to our beer list so I can plan a pilgrimage to these fantastic breweries.  (Actually, we'll use this geospatial information in a future tutorial on visualization.)  Wikipedia's [List of Breweries in Canada](https://en.wikipedia.org/wiki/List_of_breweries_in_Canada) is a fine place to start.  Let's go!

## Contents
1. [Import Libraries](#1-import-libraries)
2. [Download the web page](#2-download-the-web-page)
3. [Examine the HTML](#3-examine-the-html)
4. [Parse the HTML](#4-parse-the-html)
5. [Extract Data](#5-extract-data)
6. [Putting it all together](#6-putting-it-all-together)
7. [Create pandas dataframe](#7-create-pandas-dataframe)
8. [Conclusion](#conclusion)

# 1. Import Libraries


```python
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
```

# 2. Download the web page


```python
url = 'https://en.wikipedia.org/wiki/List_of_breweries_in_Canada'
page = requests.get(url)
```

# 3. Examine the HTML
Looking at the [wiki](https://en.wikipedia.org/wiki/List_of_breweries_in_Canada), the breweries are listed by province.  The HTML for the breweries in Alberta looks like this:

```html
<h3><span class="mw-headline" id="Alberta">Alberta</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=List_of_breweries_in_Canada&amp;action=edit&amp;section=2" title="Edit section: Alberta">edit</a><span class="mw-editsection-bracket">]</span></span></h3>
<ul>
<li>Alley Kat Brewing Company (<a href="/wiki/Edmonton" title="Edmonton">Edmonton</a>)</li>
...
</ul>
```

We can start thinking of the structure, and hence our parse logic, as follows:
- Heading `<h3>` followed by a `<span>` with class `mw-headline` gives the province
- Each province is followed by an unordered list `<ul>` of breweries
- Each list item `<li>` represents an individual brewery
- Repeat for each province

# 4. Parse the HTML
We'll first turn our `page` object into a Beautiful Soup object, then start looking for the headings denoting provinces:


```python
soup = BeautifulSoup(page.content, 'lxml')

provinces = soup.find_all(lambda tag: tag.name == 'h3' and tag.find(class_='mw-headline'))
# Print the list of provinces
for i, province in enumerate(provinces, start=1):
    print(i, province.contents[0].string)
```

    1 Alberta
    2 British Columbia
    3 Manitoba
    4 Newfoundland & Labrador
    5 Northwest Territories
    6 Nova Scotia
    7 New Brunswick
    8 Ontario
    9 Prince Edward Island
    10 Saskatchewan
    11 Quebec
    12 Yukon


Nice! We use a lambda function in `find_all()` because we want to find only tags with particular children, and Beautiful Soup doesn't have any methods to do this directly.  Our lambda function does this quite elegantly in a single line.

>Why didn't we just search for all `<h3>` tags, or `mw_headline` classes?  These searches would have turned up other elements as well, leading to additional steps to get only the ones we want.  Try it out as an exercise!
{:.blockquote}

Next, using the first province in the list (Alberta), let's get the list of breweries which are in the `<li>` tags:


```python
brewers_by_province = provinces[0].find_next_sibling('ul').find_all('li')
# Truncate the printed list to first 5 brewers
for i, brewery in enumerate(brewers_by_province[:5], start=1):
    print(i, brewery.text)
```

    1 Alley Kat Brewing Company (Edmonton)
    2 Amber's Brewing Company (Edmonton)
    3 Banded Peak Brewing Company (Calgary)
    4 Banff Ave. Brewing Co. (Banff)
    5 Bent Stick Brewing Co. (Edmonton)


Let's explain this line.  Working with the first province `provinces[0]`, we went sideways in the tree using `find_next_sibling()` to the unordered list `<ul>`.  Inside the `<ul>` we then gathered all the `<li>` tags using `find_all()`.

# 5. Extract Data
The data we want is the brewery's name and city. Scanning through the list of brewers, we see that the text can be in any of the following formats.
- Alley Kat Brewing Company (Edmonton)
- Brewsters Brewing Company (Calgary), (Edmonton)
- Andina Brewing Co. (Vancouver - Opening in 2017)
- Agassiz Brewing (Winnipeg, defunct)
- 1827–1962: The Bennett Brewing Company (St. John's)
- 1997–present: Garrison Brewing Company\[2\](Halifax)
- 2013–present: Boxing Rock Brewing Company [3] (Shelburne)
- 1786–present: Molson
- Albion (Since 2011) (Joliette)
- La Voie Maltée (Since 2002) (Jonquière, Chicoutimi, Québec)

Thank you Wikipedia for your consistency.

In order to make sure our extraction code will handle all these different formats, we'll first create a list, `sample`, containing both simple and complex examples.  Then we'll test our extraction code on `sample` to make sure it handles all the variations.

### a. Create Sample Data


```python
alley_kat = 'Alley Kat Brewing Company (Edmonton)'
brewsters = 'Brewsters Brewing Company (Calgary), (Edmonton)'
garrison = '1997–present: Garrison Brewing Company[2](Halifax)'
molson = '1786–present: Molson'
albion = 'Albion (Since 2011) (Joliette)'
la_voie_maltee = 'La Voie Maltée (Since 2002) (Jonquière, Chicoutimi, Québec)'
sample = [alley_kat, brewsters, garrison, molson, albion, la_voie_maltee]
for brewer in sample:
    print(brewer)
```

    Alley Kat Brewing Company (Edmonton)
    Brewsters Brewing Company (Calgary), (Edmonton)
    1997–present: Garrison Brewing Company[2](Halifax)
    1786–present: Molson
    Albion (Since 2011) (Joliette)
    La Voie Maltée (Since 2002) (Jonquière, Chicoutimi, Québec)


### b. Remove unnecessary text
If there is any text before the brewery's name, let's get rid of it.  It looks like the colon character is used to separate the text we want to keep and the text to remove.


```python
for brewer in sample:
    data = brewer.split(':', maxsplit=1)[-1].strip()
    print(data)
```

    Alley Kat Brewing Company (Edmonton)
    Brewsters Brewing Company (Calgary), (Edmonton)
    Garrison Brewing Company[2](Halifax)
    Molson
    Albion (Since 2011) (Joliette)
    La Voie Maltée (Since 2002) (Jonquière, Chicoutimi, Québec)


### c. Extract brewery name
Next we'll get the name of the brewer, which is all the text before either a square bracket `[` or a parenthesis `(`:


```python
pattern_text_before_brackets = r'[^[\(]+'  # pattern to match all text before [ or ( character
for brewer in sample:
    data = brewer.split(':', maxsplit=1)[-1].strip()
    name = re.match(pattern_text_before_brackets, data).group()
    print(name)
```

    Alley Kat Brewing Company
    Brewsters Brewing Company
    Garrison Brewing Company
    Molson
    Albion
    La Voie Maltée


### d. Extract city name
Finally, let's get all the text inside the parentheses.  *Usually* there is only one parentheses group, and *usually* it contains a city.  However, there are exceptions:
- multiple groups, like *(Calgary), (Edmonton)*
- no parenthesis at all, like the entry for *Molson*
- non-city text like *Since 2002*
- multiple cities inside one group, like *Jonquière, Chicoutimi, Québec*

This might get ugly, but we'll break it down into parts.  **First step** is to get any and all text within parentheses:


```python
pattern_text_in_brackets = r'\((.*?)\)'  # pattern to match all text within (...)
for brewer in sample:
    # Get a list of all text within parentheses
    cities = re.findall(pattern_text_in_brackets, brewer)
    print(cities)
```

    ['Edmonton']
    ['Calgary', 'Edmonton']
    ['Halifax']
    []
    ['Since 2011', 'Joliette']
    ['Since 2002', 'Jonquière, Chicoutimi, Québec']


That's a start, but the results are all over the place.  We need to **clean** this text and make it consistent by converting the text into a list of city names.  We will build on our previous code and do the following:
- split comma-separated lists into individual cities
- remove any text that aren't cities e.g. *Since 2002*


```python
def flatten(list_of_lists):
    """Flatten a list of lists without flattening strings"""
    for x in list_of_lists:
        if hasattr(x, '__iter__') and not isinstance(x, str):
            for y in flatten(x):
                yield y
        else:
            yield x

pattern_text_in_brackets = r'\((.*?)\)' # pattern to match all text within (...)
pattern_no_digits = r'^[^\d]*$'  # pattern to match text that doesn't contain any digits

for brewer in sample:
    # Get a list of all text within parentheses
    cities = re.findall(pattern_text_in_brackets, brewer)

    # split any strings containing comma seperated city names
    cities = [item.split(', ') if ',' in item else item for item in cities]

    # flatten the resulting list of of cities
    cities = list(flatten(cities))

    # remove any "cities" with numbers
    cities = [item for item in cities if re.match(pattern_no_digits, item)]

    print(cities)
```

    ['Edmonton']
    ['Calgary', 'Edmonton']
    ['Halifax']
    []
    ['Joliette']
    ['Jonquière', 'Chicoutimi', 'Québec']


A lot happened there.  After getting a list of all the text within parentheses, we then **split any text** that was a list of comma separated cities.  Notice the delimiter `', '` was used to remove the single space after the comma when splitting.  We could have used just a comma, but then we would be left with whitespace that would require additional calls to `.strip()`.  Again, a tradeoff between robustness and readability.  Also notice that the split is conditional and only occurs if there is a comma in the text group.  We don't want to split cities like *Mont-Tremblant* with a hyphen in their name.

The result of a `split()` is a list, which would leave us with a nested list.  We don't want that, so a helper function `flatten()` is written that will **flatten nested lists** while leaving strings untouched.

Finally, I am quite confident that no cities have a number in their name, so we **eliminate text groups with digits**.  This removes the text groups like *Since 2002*.

# 6. Putting it all together
Ready to apply all of the above to our entire set of data?  Let's do it!


```python
brewery_data = []  # initialize an empty list to contain the breweries

def flatten(list_of_lists):
    """Flatten a list of lists without flattening strings"""
    for x in list_of_lists:
        if hasattr(x, '__iter__') and not isinstance(x, str):
            for y in flatten(x):
                yield y
        else:
            yield x

for province in provinces:
    # Get the name of the province
    province_name = province.contents[0].string.strip()

    # Get a list of breweries
    breweries = province.find_next_sibling('ul').find_all('li')

    for brewery in breweries:
        # Remove unnecessary text
        data = brewery.text.split(':', maxsplit=1)[-1].strip()

        # Extract name of the brewery
        pattern_text_before_brackets = r'[^[\(]+'  # pattern to match all text before [ or ( character
        name = re.match(pattern_text_before_brackets, data).group().strip()

        # Extract list of cities
        pattern_text_in_brackets = r'\((.*?)\)'  # pattern to match all text within (...)

        # Get a list of all text within parentheses
        cities = re.findall(pattern_text_in_brackets, brewery.text)

        # split any strings containing comma seperated city names
        cities = [item.split(', ') if ',' in item else item for item in cities]

        # flatten the resulting list of of cities
        cities = list(flatten(cities))

        # remove any "cities" with numbers
        pattern_no_digits = r'^[^\d]*$'  # pattern to match text that doesn't contain any digits
        cities = [item for item in cities if re.match(pattern_no_digits, item)]

        # Gather into a single dictionary
        brewer = {
            'name': name,
            'city': cities,
            'province': province_name
        }

        # Add the brewery to our brewery list
        brewery_data.append(brewer)
```

# 7. Create *pandas* dataframe
With the dictionary of all the scraped breweries, `brewery_data`, we can now create a *pandas* dataframe:


```python
df = pd.DataFrame(brewery_data)
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


This is great!  There's still a lot of data cleaning to do, but we'll save that for the next tutorial.  Let's finish by **saving this dataframe** into a csv file so we can access it again later.  I like to put local copies of files in a subdirectory of my working directory called `data`:


```python
filename = './data/breweries_in_canada_messy.csv'
df.to_csv(filename)
```

That's it! *pandas* has a convenient method `to_csv()` which writes a dataframe into a file.

# Conclusion
Congratulations! After getting this far, you're now ready to wield the might of **Beautiful Soup** and **regex** to scrape web pages for data!  In our next tutorial, we'll focus on using *pandas* to clean our data.  Remember, our current dataframe contains the raw data from the Wikipedia page, but it has some issues:
- the `city` feature is a list object, and sometimes the list contains multiple entries (e.g. *Unibroue*)
- some entries in `name` end with a comma (e.g. *Les 3 Brasseurs,*) so we should fix that

And that's just from looking at the tail of our dataframe!  What other problems will we find?  Stay tuned and thanks for reading!

>Have a question about this tutorial, or a suggestion for a future tutorial? Please, leave a comment below!
{:.blockquote}

### Resources
- Beautiful Soup [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [regex101](https://regex101.com/), online regex tester
