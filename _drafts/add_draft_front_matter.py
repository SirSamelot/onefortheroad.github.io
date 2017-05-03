"""
Script to publish draft markdown files into Jekyll posts
- Insert Front Matter into markdown
- Create new markdown file in current directory
"""
import os
import sys
import datetime

print('[INFO] running add_draft_front_matter.py')

# Input and output filenames
ftitle = sys.argv[1].split('.')[0]
markdown_fname = ftitle + '.md'
print('[INFO] Input:\t{}'.format(markdown_fname))

title = '[DRAFT] ' + ftitle.replace('-', ' ').title()
now = datetime.datetime.now()
timestamp = now.strftime('%Y-%m-%d %X')
date = now.strftime('%Y-%m-%d')
img_fname = 'draft-bg.jpg'

output_fname = markdown_fname

# Jekyll Front Matter template
front_matter = """---
layout: post
title:  "{title}"
subtitle:   "{markdown_fname}"
date:   {timestamp}
author:     "Sam Wong"
header-img: "img/{img_filename}"
categories: python tutorial
---""".format(title=title, markdown_fname=markdown_fname, timestamp=timestamp, img_filename=img_fname)

# Read contents of current markdown file
with open(markdown_fname, 'r') as f:
    content = f.read()

# Write updated markdown to _posts
with open(output_fname, 'w') as f:
    f.write(front_matter + content)
    print('[INFO] Output:\t{}'.format(output_fname))
