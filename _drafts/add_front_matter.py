"""
Script to publish draft markdown files into Jekyll posts
- Insert Front Matter into markdown
- Create new, renamed markdown file in _posts
- Delete old markdown file
- Rename and move notebook to ./ipynb
"""
import os
import sys
import datetime
import random

print('[INFO] running add_front_matter.py')

# Input and output filenames
ftitle = sys.argv[1].split('.')[0]
markdown_fname = ftitle + '.md'
print('[INFO] Input:\t{}'.format(markdown_fname))

title = ftitle.replace('-', ' ').title()

# If a date is passed in, use that. Otherwise use current date
if (sys.argv[2]):
    date = sys.argv[2]
    # Create random time
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    random_time = datetime.time(hour, minute, second)
    timestamp = date + ' ' + str(random_time)
else:
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %X')
    date = now.strftime('%Y-%m-%d')

img_fname = date + '-' + sys.argv[1].split('.')[0] + '.jpg'

output_fname = date + '-' + markdown_fname
output_path = '../_posts/'

# Jekyll Front Matter template
front_matter = """---
layout: post
title:  "{title}"
subtitle:   "INSERT SUBTITLE"
date:   {timestamp}
author:     "Sam Wong"
header-img: "img/{img_filename}"
categories: python tutorial
comments: true
---""".format(title=title, timestamp=timestamp, img_filename=img_fname)

# Read contents of current markdown file
with open(markdown_fname, 'r') as f:
    content = f.read()

# Write updated markdown to _posts
with open(output_path + output_fname, 'w') as f:
    f.write(front_matter + content)
    print('[INFO] Output:\t{}'.format(output_path + output_fname))

# Delete original markdown file
os.remove(markdown_fname)
print('[INFO] {} deleted'.format(markdown_fname))

# Rename and move iPython notebook to ./ipynb
new_ipynb_fname = date + '-' + sys.argv[1]
ipynb_dir = '../ipynb/'
os.rename(sys.argv[1], ipynb_dir + new_ipynb_fname)
print('[INFO] draft published to {} as {}'.format(ipynb_dir, new_ipynb_fname))
