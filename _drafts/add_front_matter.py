"""
Script to publish draft markdown files into Jekyll posts
- Insert Front Matter into markdown
- Create new, renamed markdown file in _posts
- Delete old markdown file
"""
import os
import sys
import datetime

print('[INFO] running add_front_matter.py')

# Input and output filenames
ftitle = sys.argv[1].split('.')[0]
markdown_fname = sys.argv[1].split('.')[0] + '.md'
print('[INFO] Input:\t{}'.format(markdown_fname))

title = ftitle.replace('-', ' ').title()
now = datetime.datetime.now()
timestamp = now.strftime('%Y-%m-%d %X')
date = now.strftime('%Y-%m-%d')

output_fname = date + '-' + markdown_fname
output_path = '../_posts/'

# Jekyll Front Matter template
front_matter = """---
layout: post
title:  "{title}"
date:   {timestamp}
categories: python tutorial
---""".format(title=title, timestamp=timestamp)

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
