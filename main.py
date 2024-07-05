import os
import re
from pathlib import Path
from rich.progress import track
from utils.upload import UploadPic


class CSDNTransform:
    def __init__(
        self,
        upload: UploadPic,
        file_path: str,
        walk_path: str,
    ):
        self.upload = upload
        self.file_path = file_path
        self.walk_path = walk_path

        self.markdown_text = ""
        self.image_list = []
        self.exist_image_list = []
        self.image_2_url_dic = {}

    def _get_markdown_text(self):
        """读取文件的文本内容"""
        with open(self.file_path, mode="r", encoding="utf-8") as f:
            markdown_text = f.read()
        self.markdown_text = markdown_text

    def _get_target_image_path(self, target_path):
        for root, floders, files in os.walk(self.walk_path):
            for file in files:
                if file == target_path:
                    return str(Path(root) / file)

    def _process_markdown_text(self):
        """获取图片信息"""

        # markdown 中的图片以 ![[pic_name]] 表示
        first_image_lst = re.findall(r"(!\[\[.*]])", self.markdown_text)

        # 由于可能会出现匹配错误的情况，因此我们通过判断图片是否存在来做一遍过滤，在这里没有找到文件就是 None
        posterior_image_lst = [(file_name, self._get_target_image_path(file_name[3:-2])) for file_name in first_image_lst]

        self.image_list = posterior_image_lst
        self.exist_image_list = [item for item in self.image_list if item[1]]

        print(
            f"一共有{len(self.image_list)}个匹配字符串, 扫描到图片{len(self.exist_image_list)}张，正在上传！"
        )

    def _get_the_url_of_image(self, image_path):
        image_url = self.upload.upload_image(image_path)
        return image_url

    def get_the_urls(self):
        self._get_markdown_text()
        self._process_markdown_text()

        for origin_name, target_path in track(self.exist_image_list):
            image_url = self._get_the_url_of_image(target_path)
            self.image_2_url_dic[origin_name] = image_url

    @staticmethod
    def _the_transform_data_from(image_url):
        data_form = f"""\n<div align=center><img src="{image_url}"></div>\n"""
        return data_form

    def _save_markdown_text(self, output_file="markdown_processed.txt"):
        with open(output_file, mode="w", encoding="utf-8") as f:
            f.write(self.markdown_text)

    def get_transform(self):
        self.get_the_urls()

        print(
            f"一共有{len(self.image_list)}个匹配字符串, 扫描到图片{len(self.image_2_url_dic)}张，已上传成功！"
        )

        for origin_name, image_url in self.image_2_url_dic.items():
            self.markdown_text = self.markdown_text.replace(
                origin_name, self._the_transform_data_from(image_url)
            )

        self._save_markdown_text()


if __name__ == "__main__":
    # 设置 CSDN 的 cookie
    cookie = ""
    # 设置 Markdown 文件中图片的模糊地址或者 Markdown 的系统地址
    walk_path = "C:/Users/Administrator/Documents/Obsidian Vault/"

    # 由于 CSDN 上传图片次数过多会出现上传失败的问题，所以这里给出两种方式，如下：
    # 方式一：直接给需要上传的 markdown.md 文件的地址
    # file_path = 'C:/Users/Administrator/Documents/Obsidian Vault/UE开发/Animation Blueprint.md'
    # 方式二：直接复制粘贴到当前目录下的 markdown.txt 上
    file_path = "./markdown.txt"

    upload = UploadPic(cookie)
    transform = CSDNTransform(upload, file_path, walk_path)
    transform.get_transform()

    # 得到的结果在 markdown_processed.txt 文件中，直接复制到 CSDN 上即可
