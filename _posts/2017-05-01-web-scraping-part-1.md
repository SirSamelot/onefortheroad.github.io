---
layout: post
title:  "Web Scraping, Part&nbsp;1"
subtitle:   "Starring Beautiful Soup and Pandas"
date:   2017-05-01 13:08:03
author:     "Sam Wong"
categories: python tutorial
---
# Introduction
TODO
assumes basic understanding of html and css
assumes something like Anaconda is installed

## 1. Import Libaries
First, we need to import some required libraries.  For this tutorial, these libraries will be used for the following:
* `re`: extract text from strings using Regular Expressions
* `requests`: download html pages
* `bs4`: BeautifulSoup extracts text from html pages quickly and elegantly
* `pandas`: high-performance data structure and analysis tools
I recommend reading their respective documentation to fully learn the amazing capabilities of these libraries.  But not right now.  We're here to learn how to scrape web data!


```python
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
```

## 2. Download the webpage
It is very easy to download a webpage using the requests library.  We just pass in the URL as a string to `requests.get()`.  This will return a `Response` object


```python
url = 'https://www.beeradvocate.com/lists/ca/'
# page = requests.get(url)

# Offline Development
soup = BeautifulSoup(open('./data/Top Rated Beers_ Canada _ BeerAdvocate.html'), 'lxml')
```

We can explore the `page` object a bit more.  The following will return the HTTP status code of the request:


```python
# page.status_code
```

A code of 200 means all is well.  The familiar 404 would be returned for File Not Found if the URL we requested pointed to a non-existent file.  Other status codes can be returned too.

> In a production setting, you should always handle any unexpected status codes.  How would you do that?  *Hint: `requests` will raise exceptions, so it's up to you to catch them!*

Now let's take a look at the first 500 characters of what we downloaded:


```python
# print(page.content[:500])
```

Whoa, OK, hang on a minute.  What's all this?  If I squint hard enough, I can start picking out html tags here and there, and now my eyes are blurry and I'm not even drinking anything.

What `page.text` did was return the raw contents of the downloaded html file.  That's a great start (thank you `requests.get()`) but what we want is that table of Top 100 beers.  That brings us to our next tool, **Beautiful Soup**.

## 3. Parsing the html, or "What devilry is this?!"
Now that we have a nice `page` object containing our page's HTML code, we can then use the magic inside Beautiful Soup to pick out the parts we want.  This is called *parsing*.  To start, we simply instantiate Beautiful Soup with our page's content using the *lxml* HTML parser.


```python
# soup = BeautifulSoup(page.content, 'lxml')
```

Now we have a `soup` object that is ready for us to poke around.  Behind the scenes, Beautiful Soup has turned the HTML into a nested data structure.  The full scope of Beautiful Soup is beyond this tutorial, but let's explore the basics.

First, we now have access to a nicely formatted version of our downloaded page.  Here's a snippet of the first 1000 characters:


```python
print(soup.prettify()[:1000])
```

    <!DOCTYPE html>
    <html class="Public NoJs uix_javascriptNeedsInit LoggedOut Sidebar Responsive pageIsLtr not_hasTabLinks hasSearch is-sidebarOpen hasRightSidebar is-setWidth navStyle_3 pageStyle_0 hasFlexbox" dir="LTR" id="XenForo" lang="en-US" xmlns:fb="http://www.facebook.com/2008/fbml">
     <head>
      <meta charset="utf-8"/>
      <meta content="IE=Edge,chrome=1" http-equiv="X-UA-Compatible"/>
      <meta content="width=device-width, initial-scale=1" name="viewport"/>
      <base href="https://www.beeradvocate.com/community/"/>
      <script>
       var _b = document.getElementsByTagName('base')[0], _bH = "https://www.beeradvocate.com/community/";
    			if (_b && _b.href != _bH) _b.href = _bH;
      </script>
      <title>
       Top Rated Beers: Canada | BeerAdvocate
      </title>
      <noscript>
       <style>
        .JsOnly, .jsOnly { display: none !important; }
       </style>
      </noscript>
      <link href="css.php?css=xenforo,form,public&amp;style=7&amp;dir=LTR&amp;d=1492562935" rel="stylesheet"/>
      <link href="css.php?css=login_bar,mode


Better than `page.content` don't you agree?

Let's learn the basics of navigating a Beautiful Soup object.

One common task is seaching for HTML sections by tag.  For example, let's search for all `<h1>` tags.


```python
soup.find_all('h1')
```




    [<h1>Top Rated Beers: Canada</h1>]



`find_all()` finds every instance of the tag(s) in its argument list, and returns a list of `Tag` object.  In our case, there was only a single `<h1>` tag.

`Tag` objects have a number of attributes and methods.  For example, look at the output of the following lines:


```python
h1_tags = soup.find_all('h1')  # returns a list
print(h1_tags[0])
print(h1_tags[0].contents)
print(h1_tags[0].string)
```

    <h1>Top Rated Beers: Canada</h1>
    ['Top Rated Beers: Canada']
    Top Rated Beers: Canada


Notice two things.  Since `find_all()` returned a list, we access the first (and in this case, only) list item with the index [0]. Also, notice the difference in outputs depending on how we accessed `h1_tags[0]`.  We'll explore this further later on.

What happens when more than one tag is found?


```python
h3_tags = soup.find_all('h3')
print('There are {} <h3> tags.'.format(len(h3_tags)))
print(h3_tags)
```

    There are 5 <h3> tags.
    [<h3>Lists</h3>, <h3>FAQs</h3>, <h3 class="bigFooterHeader">
    <i class="uix_icon fa fa-caret-square-o-right"></i>
    								About Us
    							</h3>, <h3 class="bigFooterHeader">
    <i class="uix_icon fa fa-beer"></i>
    								BeerAdvocate Microbrew Invitational
    							</h3>, <h3 class="bigFooterHeader">
    <i class="uix_icon fa fa-book"></i>
    								Subscribe to BeerAdvocate Magazine
    							</h3>]


Since `find_all()` returns a list, we can easily iterate over the list to look at each individual tag.  This is a technique you will use often.  For example, let's print a numbered list of each `<h3>` tag:


```python
for index, tag in enumerate(h3_tags):
    print('{}.\t{}'.format(index, tag))
```

    0.	<h3>Lists</h3>
    1.	<h3>FAQs</h3>
    2.	<h3 class="bigFooterHeader">
    <i class="uix_icon fa fa-caret-square-o-right"></i>
    								About Us
    							</h3>
    3.	<h3 class="bigFooterHeader">
    <i class="uix_icon fa fa-beer"></i>
    								BeerAdvocate Microbrew Invitational
    							</h3>
    4.	<h3 class="bigFooterHeader">
    <i class="uix_icon fa fa-book"></i>
    								Subscribe to BeerAdvocate Magazine
    							</h3>


Wow, look how far we've come!  We went from a mash of HTML tags (the soup) and we've extracted an ordered list of specific tags.

There are many ways to search through Beautiful Soup objects.  There are also many ways to navigate the structure of the soup which mirror the HTML structure of the document.  We will explore this further in Part II of this tutorial, and I encourage you to look at Beautiful Soup's excellent [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

For now, we know enough to be dangerous, and we can start parsing this relatively simple page.

## 4. Examine the HTML structure
In order to parse our HTML Page, *Top Rated Canadian Beers*, we have to understand what we are looking for.  Since we're interested in the table of beers, right click the table header and select "Inspect" to enter your browser's HTML code inspector.  A snippet of the HTML table looks like this:

```html
<table width="100%" cellpadding="2" cellspacing="0" border="0">
<tr>
<td colspan="4" width="100%" align="left" valign="top" bgcolor="#000000"><span style="color: #FFFFFF; font-weight: bold;">Top Rated Beers: Canada</span></td>
</tr>
<tr>
	<td width="5%" align="left" valign="middle" bgcolor="#F0F0F0">&nbsp;</td>
	<td width="60%" align="left" valign="middle" bgcolor="#F0F0F0">&nbsp;</td>
	<td width="10%" align="left" valign="middle" bgcolor="#F0F0F0">WR</td>
	<td width="25%" align="right" valign="middle" bgcolor="#F0F0F0">Reviews | Ratings</td>
</tr>
<tr>
	<td align="center" valign="top" class="hr_bottom_light" bgcolor="#F7F7F7">
		<span style="font-weight:bold;color:#666666;">1</span></td>
	<td align="left" valign="middle" class="hr_bottom_light">
		<a href="/beer/profile/1141/10325/"><b>Péché Mortel</b></a>
		<div id="extendedInfo"><a href="/beer/profile/1141/">Brasserie Dieu du Ciel!</a><br>
		<a href="/beer/style/157/">American Double / Imperial Stout</a> / 9.50% ABV</div></td>
	<td align="left" valign="top" class="hr_bottom_light"><b>4.39</span></td><td align="right" valign="top" class="hr_bottom_light"><b>1,828</b> <span class="muted">| 5,081</span></td>
</tr>
```

Our table is contained within the `<table>` tag. A quick `find_all()` will let us know if there are other `<table>` tags in our document:


```python
print(len(soup.find_all('table')))
```

    1


Good news, there is only one `<table>` in our document.  If there were others, we would have to take care to find the one we're interested in (this technique will be covered in Part II).

We further notice that each beer is contained in its own `<tr>` tag, and each beer's details are contained within `<td>` tags.  (For a quick primer on HTML tables, take a look [here](https://developer.mozilla.org/en/docs/Web/HTML/Element/table).)

Armed with this knowledge, let's grab each `<tr>`:


```python
rows = soup.find_all('tr')
print(len(rows))
```

    102


Wait a minute... looking in our browser, we see that there are 100 beers in the list.  Why are there 102 rows in our table?


```python
print(rows[0].contents, '\n')
print(rows[1].contents, '\n')
print(rows[2].contents, '\n')
print(rows[3].contents, '\n')
```

    ['\n', <td align="left" bgcolor="#000000" colspan="4" valign="top" width="100%"><span style="color: #FFFFFF; font-weight: bold;">Top Rated Beers: Canada</span></td>, '\n']

    ['\n', <td align="left" bgcolor="#F0F0F0" valign="middle" width="5%"> </td>, '\n', <td align="left" bgcolor="#F0F0F0" valign="middle" width="60%"> </td>, '\n', <td align="left" bgcolor="#F0F0F0" valign="middle" width="10%">WR</td>, '\n', <td align="right" bgcolor="#F0F0F0" valign="middle" width="25%">Reviews | Ratings</td>, '\n']

    ['\n', <td align="center" bgcolor="#F7F7F7" class="hr_bottom_light" valign="top">
    <span style="font-weight:bold;color:#666666;">1</span></td>, '\n', <td align="left" class="hr_bottom_light" valign="middle">
    <a href="/beer/profile/1141/10325/"><b>PÃ©chÃ© Mortel</b></a>
    <div id="extendedInfo"><a href="/beer/profile/1141/">Brasserie Dieu du Ciel!</a><br/>
    <a href="/beer/style/157/">American Double / Imperial Stout</a> / 9.50% ABV</div></td>, '\n', <td align="left" class="hr_bottom_light" valign="top"><b>4.39</b></td>, '\n', <td align="right" class="hr_bottom_light" valign="top"><b>1,828</b> <span class="muted">| 5,081</span></td>, '\n']

    [<td align="center" bgcolor="#F7F7F7" class="hr_bottom_light" valign="top"><span style="font-weight:bold;color:#666666;">2</span></td>, <td align="left" class="hr_bottom_light" valign="middle"><a href="/beer/profile/1141/50803/"><b>PÃ©chÃ© Mortel En FÃ»t De Bourbon AmÃ©ricain</b></a><div id="extendedInfo"><a href="/beer/profile/1141/">Brasserie Dieu du Ciel!</a><br/><a href="/beer/style/157/">American Double / Imperial Stout</a> / 9.50% ABV</div></td>, <td align="left" class="hr_bottom_light" valign="top"><b>4.37</b></td>, <td align="right" class="hr_bottom_light" valign="top"><b>101</b> <span class="muted">| 484</span></td>]



Ah-ha!  The first two `<tr>` are table headers, and our beer list actually starts at index 2.  We can rewrite our `find_all()` as follow:


```python
rows = soup.find_all('tr')[2:]
print(len(rows))
print(rows[0].contents)
```

    100
    ['\n', <td align="center" bgcolor="#F7F7F7" class="hr_bottom_light" valign="top">
    <span style="font-weight:bold;color:#666666;">1</span></td>, '\n', <td align="left" class="hr_bottom_light" valign="middle">
    <a href="/beer/profile/1141/10325/"><b>PÃ©chÃ© Mortel</b></a>
    <div id="extendedInfo"><a href="/beer/profile/1141/">Brasserie Dieu du Ciel!</a><br/>
    <a href="/beer/style/157/">American Double / Imperial Stout</a> / 9.50% ABV</div></td>, '\n', <td align="left" class="hr_bottom_light" valign="top"><b>4.39</b></td>, '\n', <td align="right" class="hr_bottom_light" valign="top"><b>1,828</b> <span class="muted">| 5,081</span></td>, '\n']


That's better!  `rows` is now a list of 100 table rows, each containing a single beer entry.  We now have to go down to the next level in the HTML structure and get the `<td>` tags which correspond to each column in the row.  We'll start with the first row, and later we will put this all in a loop to process every row.


```python
col = rows[0].find_all('td')
print(len(col))
for index, column in enumerate(col):
    print('{}.\t{}'.format(index, column.contents))

```

    4
    0.	['\n', <span style="font-weight:bold;color:#666666;">1</span>]
    1.	['\n', <a href="/beer/profile/1141/10325/"><b>PÃ©chÃ© Mortel</b></a>, '\n', <div id="extendedInfo"><a href="/beer/profile/1141/">Brasserie Dieu du Ciel!</a><br/>
    <a href="/beer/style/157/">American Double / Imperial Stout</a> / 9.50% ABV</div>]
    2.	[<b>4.39</b>]
    3.	[<b>1,828</b>, ' ', <span class="muted">| 5,081</span>]


Excellent work!  We found all four columns, and now we can more clearly see the contents of each column.  Let's work through each column one at a time and extract the information into some easy to understand variables.


```python
rank = int(col[0].string.strip())
print(rank)
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-33-f24c7174ff41> in <module>()
    ----> 1 rank = int(col[0].string.strip())
          2 print(rank)


    AttributeError: 'NoneType' object has no attribute 'strip'


We store the first column's value in a variable named `rank`.   Here we introduce a few new things.  First, `.string` gets only the string contents of a `Tag`.  Since we don't care about the other tags (e.g. the `<span>` tag), this is exactly what we need.  The second function we chained on is `.strip()`, a Python function that strips leading and trailing whitespace from a string.  It's usually a good idea to use this when parsing HTML strings, just in case there are any hidden whitespace characters in the text.  Finally, we explicitly cast this value to type `int` so Python will treat it appropriately.

Let's do the same thing on the next column:


```python
col1 = col[1].string.strip()
print(col1)
```

Uh oh!  What happened?  Looking back at the second column, we can see that it contains a lot more than just a single value within a single tag.  In fact, it contains four values: the beer's name, the brewery, the style, and the ABV, all contained within their own tags.  What's happening is `col[1]` contains multiple *children*, with each child having their own string.   When this happens to `.string`, it's not clear which string it should return, so it returns a `None` object.  Then when `strip()` is called on a `None` object, it throws the error above.

So how do we fix this?  Just like before, we go down another level in the HTML structure!  To be clear, there are multiple ways to do this next step, so use the below as an example and  practice other methods on your own.


```python
col1_a_tag = col[1].find_all('a')
beer_name = col1_a_tag[0].string.strip()
brewery = col1_a_tag[1].string.strip()
style = col1_a_tag[2].string.strip()
print(beer_name, brewery, style, sep=' | ')
```

So far so good.  We astutely noticed that three of the four values in the second column are located inside their own `<a>` tag, so we grabbed them like we did before.  However, the last value, the ABV, isn't like the others.  It's not contained within its own tag at all.  Never fear, Beautiful Soup to the rescue!


```python
abv = col1_a_tag[2].next_sibling.strip()
print(abv)
```

Sweet!  What did we do exactly?  Since the ABV is right after the beer style, we used Beautiful Soup's `.next_sibling` attribute on the beer style tag, and boom we've got what we wanted!  Well, not exactly.  There's the `/` character in front that's a bit ugly.  Also, for future data analysis we will probably want to treat the ABV as a number and not a string.  So let's get the ABV as a number only, and for that we use Python's powerful Regular Expression library:


```python
abv = float(re.findall(r"(?<![a-zA-Z:])[-+]?\d*\.?\d+", abv)[0])
print(abv, type(abv))
```

The long expression within `re.findall()` is known a *Regular Expression*, or *regex* for short.  Basically, this particular *regex* finds and returns a numeric value contained within a string.  There are many ways to write this expression, and I would recommend becoming familiar with *regex* if you plan to do any sort of text or expression matching work.  Google has a great overview on *regex* [here](https://developers.google.com/edu/python/regular-expressions).

Whew, that second column was a bit of work.  Thankfully, the next two columns are again simple single-value columns.


```python
score = float(col[2].string.strip())
rating = int(col[3].string.strip().replace(',', ''))
print(score, type(score))
print(rating, type(rating))
```

The only thing special about these lines is we removed the comma separator in the Ratings string before casting it to an int.

Now let's put it all together by neatly packaging all that information into a single dictionary entry we'll call `beer`:


```python
beer = {
    'rank': rank,
    'name': beer_name,
    'brewery': brewery,
    'style': style,
    'abv': abv,
    'score': score,
    'rating': rating
}
```

Time for a little review.  We've read in a single table row containing a beer, and extracted seven different values from that row.  We've cleaned up these values a bit so that they are ready for future analysis.  Finally, we stored all these values as key-value pairs in a dictinary.  Now, we just have to do this all again for the the next 99 beers.  Say what?  Well, that's where Python comes in to do the repetitive work so we don't have to.

Putting everything above together, we get:


```python
beers = []  # Initialize an empty list to contain all the beer
for row in soup.find_all('tr')[2:]:
    col = row.find_all('td')

    # First column
    rank = int(col[0].string.strip())

    # Second column
    col1_a_tag = col[1].find_all('a')
    beer_name = col1_a_tag[0].string.strip()
    brewery = col1_a_tag[1].string.strip()
    style = col1_a_tag[2].string.strip()
    abv = col1_a_tag[2].next_sibling.strip()
    abv = float(re.findall(r"(?<![a-zA-Z:])[-+]?\d*\.?\d+", abv)[0])

    # Third column
    score = float(col[2].string.strip())

    # Fourth column
    rating = int(col[3].string.strip().replace(',', ''))

    # Gather into a single dictionary
    beer = {
        'rank': rank,
        'name': beer_name,
        'brewery': brewery,
        'style': style,
        'abv': abv,
        'score': score,
        'rating': rating
    }

    # Add the beer to our beer list
    beers.append(beer)
```

# TODO: left off here
