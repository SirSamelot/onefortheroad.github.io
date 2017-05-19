---
layout: post
title:  "[DRAFT] Basic Visualization 1"
subtitle:   "basic-visualization-1.md"
date:   2017-05-18 15:15:22
author:     "Sam Wong"
header-img: "img/draft-bg.jpg"
categories: tutorial
---

```python
import pandas as pd
import seaborn as sns

%matplotlib inline

# Global options
pd.set_option('display.width', 1000)
sns.set_style("whitegrid")
sns.set_context('notebook', font_scale=1.2)
```


```python
filename = './data/top_100_canadian_beers_with_city.csv'
df = pd.read_csv(filename)

print(df.head())
```

       rank                                      name                  brewery                             style   abv  score  ratings          city          province
    0     1                              Péché Mortel  Brasserie Dieu du Ciel!  American Double / Imperial Stout   9.5   4.39     5087  Saint-Jérôme            Quebec
    1     2  Péché Mortel En Fût De Bourbon Américain  Brasserie Dieu du Ciel!  American Double / Imperial Stout   9.5   4.45      488  Saint-Jérôme            Quebec
    2     3                           La Fin Du Monde                 Unibroue                            Tripel   9.0   4.31    10021       Chambly            Quebec
    3     4                Unibroue 17 Grande Réserve                 Unibroue           Belgian Strong Dark Ale  10.0   4.24     1140       Chambly            Quebec
    4     5                               Fat Tug IPA        Driftwood Brewery                      American IPA   7.0   4.25      601      Victoria  British Columbia
    


```python
# Easy initial plot to look for any obvious relationships between pairs of numeric variables
sns.pairplot(df)
```




    <seaborn.axisgrid.PairGrid at 0x5433e48>




![png](basic-visualization-1_files/basic-visualization-1_2_1.png)



```python
# Let's look at any relationship between score, ABV, and style
sns.lmplot(x='abv', y='score', hue='style', data=df, fit_reg=False, markers='X', size=8, scatter_kws={'alpha':0.8, 's':200})
```




    <seaborn.axisgrid.FacetGrid at 0xd2f75c0>




![png](basic-visualization-1_files/basic-visualization-1_3_1.png)



```python
# bin the beer styles
beer_families = {
    'barleywine': ['American Barleywine', 'English Barleywine'],
    'belgian dark ales': ['Belgian Strong Dark Ale', 'Quadrupel (Quad)'],
    'IPA': ['American Double / Imperial IPA', 'American IPA', 'Belgian IPA'],
    'pale ale': ['American Pale Ale (APA)', 'Belgian Strong Pale Ale'],
    'porter/stout': ['American Porter', 'Baltic Porter', 'English Porter', 'American Double / Imperial Stout', 'American Stout', 'Irish Dry Stout', 'Milk / Sweet Stout', 'Oatmeal Stout', 'Russian Imperial Stout'],
    'saison': ['Saison / Farmhouse Ale'],
    'tripel': ['Tripel'],
    'wheat beer': ['Berliner Weissbier', 'Witbier'], 
    # Uncategorized
    # American Wild Ale
    # Doppelbock
    # Extra Special / Strong Bitter (ESB)
    # Flanders Red Ale
    # Rye Beer
}

def get_beer_family(style):
    family = [k for k, v in beer_families.items() if style in v]
    return next(iter(family), 'Other')
    
df['family'] = df['style'].apply(lambda x: get_beer_family(x))
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rank</th>
      <th>name</th>
      <th>brewery</th>
      <th>style</th>
      <th>abv</th>
      <th>score</th>
      <th>ratings</th>
      <th>city</th>
      <th>province</th>
      <th>family</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Péché Mortel</td>
      <td>Brasserie Dieu du Ciel!</td>
      <td>American Double / Imperial Stout</td>
      <td>9.5</td>
      <td>4.39</td>
      <td>5087</td>
      <td>Saint-Jérôme</td>
      <td>Quebec</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Péché Mortel En Fût De Bourbon Américain</td>
      <td>Brasserie Dieu du Ciel!</td>
      <td>American Double / Imperial Stout</td>
      <td>9.5</td>
      <td>4.45</td>
      <td>488</td>
      <td>Saint-Jérôme</td>
      <td>Quebec</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>La Fin Du Monde</td>
      <td>Unibroue</td>
      <td>Tripel</td>
      <td>9.0</td>
      <td>4.31</td>
      <td>10021</td>
      <td>Chambly</td>
      <td>Quebec</td>
      <td>tripel</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Unibroue 17 Grande Réserve</td>
      <td>Unibroue</td>
      <td>Belgian Strong Dark Ale</td>
      <td>10.0</td>
      <td>4.24</td>
      <td>1140</td>
      <td>Chambly</td>
      <td>Quebec</td>
      <td>belgian dark ales</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Fat Tug IPA</td>
      <td>Driftwood Brewery</td>
      <td>American IPA</td>
      <td>7.0</td>
      <td>4.25</td>
      <td>601</td>
      <td>Victoria</td>
      <td>British Columbia</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>Red Racer IPA (India Pale Ale)</td>
      <td>Central City Brewers + Distillers</td>
      <td>American IPA</td>
      <td>6.5</td>
      <td>4.23</td>
      <td>1085</td>
      <td>Surrey</td>
      <td>British Columbia</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>Nectarous</td>
      <td>Four Winds Brewing Co.</td>
      <td>American Wild Ale</td>
      <td>5.5</td>
      <td>4.48</td>
      <td>92</td>
      <td>Delta</td>
      <td>British Columbia</td>
      <td>Other</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>Trois Pistoles</td>
      <td>Unibroue</td>
      <td>Belgian Strong Dark Ale</td>
      <td>9.0</td>
      <td>4.20</td>
      <td>4938</td>
      <td>Chambly</td>
      <td>Quebec</td>
      <td>belgian dark ales</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>Grande Cuvée Porter Baltique</td>
      <td>Les Trois Mousquetaires</td>
      <td>Baltic Porter</td>
      <td>10.0</td>
      <td>4.25</td>
      <td>451</td>
      <td>Brossard</td>
      <td>Quebec</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>Solstice D'été Aux Framboises</td>
      <td>Brasserie Dieu du Ciel!</td>
      <td>Berliner Weissbier</td>
      <td>5.9</td>
      <td>4.26</td>
      <td>350</td>
      <td>Saint-Jérôme</td>
      <td>Quebec</td>
      <td>wheat beer</td>
    </tr>
    <tr>
      <th>10</th>
      <td>11</td>
      <td>Moralité</td>
      <td>Brasserie Dieu du Ciel!</td>
      <td>American IPA</td>
      <td>6.9</td>
      <td>4.26</td>
      <td>328</td>
      <td>Saint-Jérôme</td>
      <td>Quebec</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>11</th>
      <td>12</td>
      <td>Aphrodisiaque</td>
      <td>Brasserie Dieu du Ciel!</td>
      <td>American Stout</td>
      <td>6.5</td>
      <td>4.19</td>
      <td>1651</td>
      <td>Saint-Jérôme</td>
      <td>Quebec</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>12</th>
      <td>13</td>
      <td>Maudite</td>
      <td>Unibroue</td>
      <td>Belgian Strong Dark Ale</td>
      <td>8.0</td>
      <td>4.17</td>
      <td>4573</td>
      <td>Chambly</td>
      <td>Quebec</td>
      <td>belgian dark ales</td>
    </tr>
    <tr>
      <th>13</th>
      <td>14</td>
      <td>Dominus Vobiscum Lupulus</td>
      <td>Microbrasserie Charlevoix</td>
      <td>Belgian IPA</td>
      <td>10.0</td>
      <td>4.24</td>
      <td>274</td>
      <td>Baie-Saint-Paul</td>
      <td>Quebec</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>14</th>
      <td>15</td>
      <td>La Terrible</td>
      <td>Unibroue</td>
      <td>Belgian Strong Dark Ale</td>
      <td>10.5</td>
      <td>4.16</td>
      <td>2216</td>
      <td>Chambly</td>
      <td>Quebec</td>
      <td>belgian dark ales</td>
    </tr>
    <tr>
      <th>15</th>
      <td>16</td>
      <td>Sartori Harvest IPA</td>
      <td>Driftwood Brewery</td>
      <td>American IPA</td>
      <td>7.0</td>
      <td>4.36</td>
      <td>107</td>
      <td>Victoria</td>
      <td>British Columbia</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>16</th>
      <td>17</td>
      <td>Bring Out Your Dead</td>
      <td>Bellwoods Brewery</td>
      <td>Russian Imperial Stout</td>
      <td>12.2</td>
      <td>4.34</td>
      <td>117</td>
      <td>Toronto</td>
      <td>Ontario</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>17</th>
      <td>18</td>
      <td>St-Ambroise Stout Impériale Russe</td>
      <td>McAuslan Brewing</td>
      <td>Russian Imperial Stout</td>
      <td>9.1</td>
      <td>4.21</td>
      <td>307</td>
      <td>Montréal</td>
      <td>Quebec</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>18</th>
      <td>19</td>
      <td>Great Lakes Thrust! An IPA</td>
      <td>Great Lakes Brewery</td>
      <td>American IPA</td>
      <td>6.5</td>
      <td>4.32</td>
      <td>115</td>
      <td>Etibicoke</td>
      <td>Ontario</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>19</th>
      <td>20</td>
      <td>Don De Dieu</td>
      <td>Unibroue</td>
      <td>Belgian Strong Pale Ale</td>
      <td>9.0</td>
      <td>4.13</td>
      <td>2868</td>
      <td>Chambly</td>
      <td>Quebec</td>
      <td>pale ale</td>
    </tr>
    <tr>
      <th>20</th>
      <td>21</td>
      <td>Ransack the Universe - Hemisphere IPA</td>
      <td>Collective Arts Brewing</td>
      <td>American IPA</td>
      <td>6.8</td>
      <td>4.19</td>
      <td>229</td>
      <td>Hamilton</td>
      <td>Ontario</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>21</th>
      <td>22</td>
      <td>Yakima IPA</td>
      <td>Microbrasserie Le Castor</td>
      <td>American IPA</td>
      <td>6.5</td>
      <td>4.19</td>
      <td>192</td>
      <td>Rigaud</td>
      <td>Quebec</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>22</th>
      <td>23</td>
      <td>Great Lakes Karma Citra IPA</td>
      <td>Great Lakes Brewery</td>
      <td>American IPA</td>
      <td>6.6</td>
      <td>4.26</td>
      <td>115</td>
      <td>Etibicoke</td>
      <td>Ontario</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>23</th>
      <td>24</td>
      <td>Singularity</td>
      <td>Driftwood Brewery</td>
      <td>Russian Imperial Stout</td>
      <td>12.2</td>
      <td>4.20</td>
      <td>162</td>
      <td>Victoria</td>
      <td>British Columbia</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>24</th>
      <td>25</td>
      <td>St-Ambroise Oatmeal Stout</td>
      <td>McAuslan Brewing</td>
      <td>Oatmeal Stout</td>
      <td>5.0</td>
      <td>4.09</td>
      <td>1237</td>
      <td>Montréal</td>
      <td>Quebec</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>25</th>
      <td>26</td>
      <td>Doppelbock Grande Cuvée Printemps</td>
      <td>Les Trois Mousquetaires</td>
      <td>Doppelbock</td>
      <td>8.6</td>
      <td>4.16</td>
      <td>206</td>
      <td>Brossard</td>
      <td>Quebec</td>
      <td>Other</td>
    </tr>
    <tr>
      <th>26</th>
      <td>27</td>
      <td>Red Racer Imperial IPA</td>
      <td>Central City Brewers + Distillers</td>
      <td>American Double / Imperial IPA</td>
      <td>9.0</td>
      <td>4.17</td>
      <td>184</td>
      <td>Surrey</td>
      <td>British Columbia</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>27</th>
      <td>28</td>
      <td>La Vache Folle - Milk Stout</td>
      <td>Microbrasserie Charlevoix</td>
      <td>American Double / Imperial Stout</td>
      <td>9.0</td>
      <td>4.14</td>
      <td>255</td>
      <td>Baie-Saint-Paul</td>
      <td>Quebec</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>28</th>
      <td>29</td>
      <td>Grande Noirceur</td>
      <td>Brasserie Dieu du Ciel!</td>
      <td>Russian Imperial Stout</td>
      <td>9.0</td>
      <td>4.11</td>
      <td>397</td>
      <td>Saint-Jérôme</td>
      <td>Quebec</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>29</th>
      <td>30</td>
      <td>Black Oak Ten Bitter Years</td>
      <td>Black Oak Brewing Co.</td>
      <td>American Double / Imperial IPA</td>
      <td>8.0</td>
      <td>4.16</td>
      <td>184</td>
      <td>Etobicoke</td>
      <td>Ontario</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>70</th>
      <td>71</td>
      <td>La Fringante</td>
      <td>Unibroue</td>
      <td>Tripel</td>
      <td>10.0</td>
      <td>4.12</td>
      <td>81</td>
      <td>Chambly</td>
      <td>Quebec</td>
      <td>tripel</td>
    </tr>
    <tr>
      <th>71</th>
      <td>72</td>
      <td>Bounty Hunter</td>
      <td>Bellwoods Brewery</td>
      <td>American Porter</td>
      <td>10.3</td>
      <td>4.14</td>
      <td>70</td>
      <td>Toronto</td>
      <td>Ontario</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>72</th>
      <td>73</td>
      <td>Play Dead IPA</td>
      <td>Yellow Dog Brewing</td>
      <td>American IPA</td>
      <td>6.8</td>
      <td>4.14</td>
      <td>65</td>
      <td>Port Moody</td>
      <td>British Columbia</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>73</th>
      <td>74</td>
      <td>La Buteuse</td>
      <td>Le Trou Du Diable</td>
      <td>Tripel</td>
      <td>10.0</td>
      <td>4.01</td>
      <td>173</td>
      <td>Shawinigan</td>
      <td>Quebec</td>
      <td>tripel</td>
    </tr>
    <tr>
      <th>74</th>
      <td>75</td>
      <td>Dernière Volonté Réserve Spéciale En Fût De Pi...</td>
      <td>Brasserie Dieu du Ciel!</td>
      <td>Belgian Strong Pale Ale</td>
      <td>7.5</td>
      <td>4.08</td>
      <td>90</td>
      <td>Saint-Jérôme</td>
      <td>Quebec</td>
      <td>pale ale</td>
    </tr>
    <tr>
      <th>75</th>
      <td>76</td>
      <td>Hopnotist</td>
      <td>Parallel 49 Brewing Company</td>
      <td>American Double / Imperial IPA</td>
      <td>8.5</td>
      <td>4.17</td>
      <td>56</td>
      <td>Vancouver</td>
      <td>British Columbia</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>76</th>
      <td>77</td>
      <td>Farmhand Ale</td>
      <td>Driftwood Brewery</td>
      <td>Saison / Farmhouse Ale</td>
      <td>5.5</td>
      <td>4.01</td>
      <td>169</td>
      <td>Victoria</td>
      <td>British Columbia</td>
      <td>saison</td>
    </tr>
    <tr>
      <th>77</th>
      <td>78</td>
      <td>Dominus Vobiscum Saison</td>
      <td>Microbrasserie Charlevoix</td>
      <td>Saison / Farmhouse Ale</td>
      <td>6.0</td>
      <td>4.05</td>
      <td>112</td>
      <td>Baie-Saint-Paul</td>
      <td>Quebec</td>
      <td>saison</td>
    </tr>
    <tr>
      <th>78</th>
      <td>79</td>
      <td>Isseki Nicho</td>
      <td>Brasserie Dieu du Ciel!</td>
      <td>Saison / Farmhouse Ale</td>
      <td>9.5</td>
      <td>3.99</td>
      <td>222</td>
      <td>Saint-Jérôme</td>
      <td>Quebec</td>
      <td>saison</td>
    </tr>
    <tr>
      <th>79</th>
      <td>80</td>
      <td>Full Moon Pale Ale</td>
      <td>Alley Kat Brewing Company</td>
      <td>American Pale Ale (APA)</td>
      <td>5.0</td>
      <td>4.05</td>
      <td>111</td>
      <td>Edmonton</td>
      <td>Alberta</td>
      <td>pale ale</td>
    </tr>
    <tr>
      <th>80</th>
      <td>81</td>
      <td>Flying Monkeys Smashbomb Atomic IPA</td>
      <td>Flying Monkeys Craft Brewery</td>
      <td>American IPA</td>
      <td>6.0</td>
      <td>3.95</td>
      <td>590</td>
      <td>Barrie</td>
      <td>Ontario</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>81</th>
      <td>82</td>
      <td>Back Hand Of God Stout</td>
      <td>Crannóg Ales</td>
      <td>Irish Dry Stout</td>
      <td>5.2</td>
      <td>4.14</td>
      <td>61</td>
      <td>Sorrento</td>
      <td>British Columbia</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>82</th>
      <td>83</td>
      <td>Rhyme &amp; Reason</td>
      <td>Collective Arts Brewing</td>
      <td>American Pale Ale (APA)</td>
      <td>5.7</td>
      <td>3.99</td>
      <td>187</td>
      <td>Hamilton</td>
      <td>Ontario</td>
      <td>pale ale</td>
    </tr>
    <tr>
      <th>83</th>
      <td>84</td>
      <td>Stranger Than Fiction</td>
      <td>Collective Arts Brewing</td>
      <td>English Porter</td>
      <td>5.5</td>
      <td>4.02</td>
      <td>129</td>
      <td>Hamilton</td>
      <td>Ontario</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>84</th>
      <td>85</td>
      <td>Nickel Brook Immodest</td>
      <td>Nickel Brook Brewing Co.</td>
      <td>American Double / Imperial IPA</td>
      <td>9.5</td>
      <td>4.09</td>
      <td>75</td>
      <td>Burlington</td>
      <td>Ontario</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>85</th>
      <td>86</td>
      <td>Twenty Pounder</td>
      <td>Driftwood Brewery</td>
      <td>American Double / Imperial IPA</td>
      <td>9.0</td>
      <td>4.07</td>
      <td>83</td>
      <td>Victoria</td>
      <td>British Columbia</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>86</th>
      <td>87</td>
      <td>State Of Mind</td>
      <td>Collective Arts Brewing</td>
      <td>American IPA</td>
      <td>4.4</td>
      <td>4.04</td>
      <td>103</td>
      <td>Hamilton</td>
      <td>Ontario</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>87</th>
      <td>88</td>
      <td>Shipwreck IPA</td>
      <td>Lighthouse Brewing Company</td>
      <td>American IPA</td>
      <td>6.5</td>
      <td>4.02</td>
      <td>121</td>
      <td>Victoria</td>
      <td>British Columbia</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>88</th>
      <td>89</td>
      <td>Blackstone Porter</td>
      <td>Driftwood Brewery</td>
      <td>English Porter</td>
      <td>6.0</td>
      <td>4.04</td>
      <td>101</td>
      <td>Victoria</td>
      <td>British Columbia</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>89</th>
      <td>90</td>
      <td>Four Winds IPA</td>
      <td>Four Winds Brewing Co.</td>
      <td>American IPA</td>
      <td>7.0</td>
      <td>4.06</td>
      <td>82</td>
      <td>Delta</td>
      <td>British Columbia</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>90</th>
      <td>91</td>
      <td>Déesse Nocturne</td>
      <td>Brasserie Dieu du Ciel!</td>
      <td>American Stout</td>
      <td>5.0</td>
      <td>4.11</td>
      <td>61</td>
      <td>Saint-Jérôme</td>
      <td>Quebec</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>91</th>
      <td>92</td>
      <td>Woolly Bugger</td>
      <td>Howe Sound Inn &amp; Brewing Company</td>
      <td>English Barleywine</td>
      <td>11.0</td>
      <td>4.03</td>
      <td>99</td>
      <td>Squamish</td>
      <td>British Columbia</td>
      <td>barleywine</td>
    </tr>
    <tr>
      <th>92</th>
      <td>93</td>
      <td>Saison Brett</td>
      <td>Les Trois Mousquetaires</td>
      <td>Saison / Farmhouse Ale</td>
      <td>7.5</td>
      <td>4.11</td>
      <td>60</td>
      <td>Brossard</td>
      <td>Quebec</td>
      <td>saison</td>
    </tr>
    <tr>
      <th>93</th>
      <td>94</td>
      <td>Megadestroyer Imperial Licorice Stout</td>
      <td>Howe Sound Inn &amp; Brewing Company</td>
      <td>American Double / Imperial Stout</td>
      <td>10.0</td>
      <td>3.99</td>
      <td>141</td>
      <td>Squamish</td>
      <td>British Columbia</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>94</th>
      <td>95</td>
      <td>Numbskull</td>
      <td>Lighthouse Brewing Company</td>
      <td>American Double / Imperial IPA</td>
      <td>9.1</td>
      <td>4.12</td>
      <td>56</td>
      <td>Victoria</td>
      <td>British Columbia</td>
      <td>IPA</td>
    </tr>
    <tr>
      <th>95</th>
      <td>96</td>
      <td>Red Racer Gingerhead Gingerbread Stout</td>
      <td>Central City Brewers + Distillers</td>
      <td>Irish Dry Stout</td>
      <td>6.0</td>
      <td>4.04</td>
      <td>84</td>
      <td>Surrey</td>
      <td>British Columbia</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>96</th>
      <td>97</td>
      <td>Solstice D'hiver</td>
      <td>Brasserie Dieu du Ciel!</td>
      <td>American Barleywine</td>
      <td>10.2</td>
      <td>3.91</td>
      <td>921</td>
      <td>Saint-Jérôme</td>
      <td>Quebec</td>
      <td>barleywine</td>
    </tr>
    <tr>
      <th>97</th>
      <td>98</td>
      <td>Long, Dark Voyage To Uranus</td>
      <td>Sawdust City Brewing Co.</td>
      <td>Russian Imperial Stout</td>
      <td>8.5</td>
      <td>4.04</td>
      <td>83</td>
      <td>Gravenhurst</td>
      <td>Ontario</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>98</th>
      <td>99</td>
      <td>Amsterdam Tempest Imperial Stout</td>
      <td>Amsterdam Brewing Company</td>
      <td>Russian Imperial Stout</td>
      <td>9.0</td>
      <td>3.98</td>
      <td>138</td>
      <td>Toronto</td>
      <td>Ontario</td>
      <td>porter/stout</td>
    </tr>
    <tr>
      <th>99</th>
      <td>100</td>
      <td>Rigor Mortis Abt</td>
      <td>Brasserie Dieu du Ciel!</td>
      <td>Quadrupel (Quad)</td>
      <td>10.5</td>
      <td>3.91</td>
      <td>759</td>
      <td>Saint-Jérôme</td>
      <td>Quebec</td>
      <td>belgian dark ales</td>
    </tr>
  </tbody>
</table>
<p>100 rows × 10 columns</p>
</div>




```python
df.family.value_counts()
```




    IPA                  33
    porter/stout         27
    belgian dark ales     8
    tripel                7
    barleywine            7
    saison                6
    pale ale              5
    Other                 5
    wheat beer            2
    Name: family, dtype: int64




```python
# mark any beers with 5 or less entries as Other
threshold = 5
df = df.apply(lambda x: x.mask(x.map(x.value_counts())<=threshold, 'other') if x.name=='family' else x)
print(df.family.value_counts())
```

    IPA                  33
    porter/stout         27
    other                12
    belgian dark ales     8
    tripel                7
    barleywine            7
    saison                6
    Name: family, dtype: int64
    


```python
# Categorize the family name so it will be treated in a certain order

# create the category orders, sorted alphabetically
sorted_family_index = df.family.drop_duplicates().str.lower().sort_values().index
family_order = df.family.iloc[sorted_family_index]

# move 'other' to end of categories
family_order = family_order[family_order != 'other']
family_order = family_order.append(pd.Series('other'))

df.family = df.family.astype('category', ordered=True, categories=family_order)
```


```python
# Create custom color palette with grey as the color for Other
family_palette = sns.color_palette('Set1', len(df.family.cat.categories)-1)
family_palette.append(sns.xkcd_rgb["grey"])  # 'other' category

# Set palette as default
sns.set_palette(family_palette)
```


```python
sns.lmplot(x='abv', y='score', hue='family', data=df, fit_reg=False, markers='X', size=8, scatter_kws={'alpha':0.8, 's':200})
```




    <seaborn.axisgrid.FacetGrid at 0xeed2ef0>




![png](basic-visualization-1_files/basic-visualization-1_9_1.png)



```python
# list of styles in the 'other' family
list(df.loc[df['family'] == 'other']['style'].unique())
```




    ['American Wild Ale',
     'Berliner Weissbier',
     'Belgian Strong Pale Ale',
     'Doppelbock',
     'Extra Special / Strong Bitter (ESB)',
     'Witbier',
     'Rye Beer',
     'American Pale Ale (APA)',
     'Flanders Red Ale']




```python
# list styles in a particular family
beer_families.get('barleywine')
```




    ['American Barleywine', 'English Barleywine']




```python
# scatterplot of family vs abv
sns.stripplot(x="abv", y="family", data=df, marker='X', alpha=0.6, size=20);
```


![png](basic-visualization-1_files/basic-visualization-1_12_0.png)



```python
# bar plot of family
sns.countplot(y='family', data=df, alpha=0.8)
```




    <matplotlib.axes._subplots.AxesSubplot at 0xd34b9b0>




![png](basic-visualization-1_files/basic-visualization-1_13_1.png)



```python
# provinces and beers
sns.countplot(y='province', data=df, order=df.province.value_counts().index, alpha=0.8)
```




    <matplotlib.axes._subplots.AxesSubplot at 0xd627cc0>




![png](basic-visualization-1_files/basic-visualization-1_14_1.png)



```python
# top breweries
with sns.plotting_context("talk"):
    sns.countplot(y='brewery', data=df, order=df.brewery.value_counts().index, alpha=0.8)
```


![png](basic-visualization-1_files/basic-visualization-1_15_0.png)



```python
# rank and style
sns.stripplot(x="rank", y="family", data=df, jitter=False, alpha=0.8, marker='X', size=16, edgecolor='white', linewidth=0.5);
```


![png](basic-visualization-1_files/basic-visualization-1_16_0.png)

