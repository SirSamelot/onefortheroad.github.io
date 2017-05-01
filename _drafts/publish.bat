@echo off
REM Publish Jupyter notebooks to Jekyll markdown posts

REM Convert Jupyter notebook to markdown file
jupyter nbconvert %1 --to markdown

REM Run python script to add front matter to markdown file
python add_front_matter.py %1
