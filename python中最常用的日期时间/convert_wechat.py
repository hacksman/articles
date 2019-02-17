#!/usr/bin/env python 
# coding:utf-8
# @Time :1/13/19 11:04

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

    # 先替换图片
    img_block_regx = re.compile("!\\[[^\\]]+\\]\\([^\\)]+\\)")

    img_list = img_block_regx.findall(mf_read)

    for img_count, per_img in enumerate(img_list):

        mf_read = mf_read.replace(per_img, "![pic_{}.png]({}{}/imgs/{})".format(img_count + 1, github_base_url, md_name, per_img))

    # 再替换代码
    code_block_regx = re.compile("```([\\s\\S]*?)```[\\s]?")

    code_list = code_block_regx.findall(mf_read)

    for code_count, per_code in enumerate(code_list):

        per_code = "```" + per_code + "```"

        if code_count == 0:
            mf_read = mf_read.replace(per_code, "![carbon.png]({}{}/imgs/carbon.png)".format(github_base_url, md_name))
        else:
            mf_read = mf_read.replace(per_code, "![carbon_{}.png]({}{}/imgs/carbon_{}.png)".format(code_count, github_base_url, md_name, code_count))

    new_md_f = mf_read


with open("{}_wechat.md".format(md_name), "w", encoding="utf-8") as wechat_md_f:
    wechat_md_f.write(new_md_f)
