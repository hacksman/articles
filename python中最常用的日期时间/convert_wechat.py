#!/usr/bin/env python 
# coding:utf-8
# @Time :1/13/19 11:04

import sys
import os
import re
pwd = os.getcwd()
files = os.listdir(path=str(pwd))

md_file_regx = re.compile(".*\.md")

md_file = None
for per_file in files:
    if md_file_regx.findall(per_file):
        md_file = per_file

if not md_file:
    print("该文件下没有markdown文档")

md_name = md_file.replace(".md", "")

new_md_f = ""

github_base_url = "https://raw.githubusercontent.com/hacksman/articles/master/"

with open(md_file, "r", encoding="utf-8") as mf:
    mf_read = mf.read()
    code_block_regx = re.compile("```([\\s\\S]*?)```[\\s]?")

    code_list = code_block_regx.findall(mf_read)

    for code_count, per_code in enumerate(code_list):

        per_code = "```" + per_code + "```"

        mf_read = mf_read.replace(per_code, "![code_{}.png]({}{}/imgs/code_{}.png)".format(code_count + 1, github_base_url, md_name, code_count + 1))
    print(mf_read)


    # new_md_f = mf_read

# print(new_md_f)