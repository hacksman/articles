#!/usr/bin/env python 
# coding:utf-8
# @Time :2/17/19 10:05

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

        image_url = per_img.split("/")[-1].replace(")", "")
        mf_read = mf_read.replace(per_img, "![pic_{}.png]({}{}/imgs/{})".format(img_count + 1, github_base_url, md_name, image_url))

    new_md_f = mf_read

with open("{}_juejin.md".format(md_name), "w", encoding="utf-8") as wechat_md_f:
    wechat_md_f.write(new_md_f)
