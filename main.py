import os
import re
from pathlib import Path
from rich.progress import track
from upload import UploadPic


class CSDNTransform:
    def __init__(self, upload:UploadPic, file_path, walk_path='C:/Users/Administrator/Documents/Obsidian Vault/'):
        self.upload = upload
        self.file_path = file_path
        self.walk_path = walk_path

        self.markdown_text = ''
        self.image_lst = []
        self.posterior_image_lst = []
        self.image_2_url_dic = {}

    def _get_markdown_text(self):
        with open(self.file_path, mode='r', encoding='utf-8') as f:
            markdown_text = f.read()
        self.markdown_text = markdown_text

    def _process_markdown_text(self):
        image_lst = re.findall(r'(!\[\[.*]])', self.markdown_text)
        posterior_image_lst = [item[3:-2] for item in image_lst]

        self.image_lst = image_lst
        self.posterior_image_lst = posterior_image_lst

    def _get_target_image_path(self, target_path):
        for root, floders, files in os.walk(self.walk_path):
            for file in files:
                if file == target_path:
                    return str(Path(root) / file)

    def _get_the_url_of_image(self, image_path):
        image_url = self.upload.upload_image(image_path)
        return image_url

    def get_the_urls(self):
        self._get_markdown_text()
        self._process_markdown_text()

        not_exist_image_index = []

        for ix, (origin_image, target_path) in track(enumerate(zip(self.image_lst, self.posterior_image_lst))):
            image_path = self._get_target_image_path(target_path)
            if image_path is not None:
                image_url = self._get_the_url_of_image(image_path)
                self.image_2_url_dic[origin_image] = image_url
            else:
                not_exist_image_index.append(ix)

        # 清楚掉需要删除的index
        num = 0
        for ix in not_exist_image_index:
            del self.image_lst[ix-num]
            del self.posterior_image_lst[ix-num]
            num += 1

    def _the_transform_data_from(self, image_url):
        data_form = f"""\n<div align=center><img src="{image_url}"></div>\n"""
        return data_form

    def _save_markdown_text(self, output_file='markdown_processed.txt'):
        with open(output_file, mode='w', encoding='utf-8') as f:
            f.write(self.markdown_text)

    def get_transform(self):
        self.get_the_urls()

        print(f"上传成功{len(self.image_2_url_dic)}张图片,总共有{len(self.image_lst)}张图片")

        for origin_image, image_url in self.image_2_url_dic.items():
            self.markdown_text = self.markdown_text.replace(origin_image, self._the_transform_data_from(image_url))

        self._save_markdown_text()



if __name__ == '__main__':
    cookie = 'uuid_tt_dd=10_20714563540-1713279603925-839503; c_adb=1; UserName=m0_72947390; UserInfo=dc1d0c7f5d4c41d1a2269fc9e40e106e; UserToken=dc1d0c7f5d4c41d1a2269fc9e40e106e; UserNick=Bigcrab__; AU=B30; UN=m0_72947390; BT=1713280879102; p_uid=U010000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22m0_72947390%22%2C%22scope%22%3A1%7D%7D; _ga=GA1.1.1507512576.1713742454; _ga_7W1N0GEY1P=GS1.1.1713742454.1.1.1713743378.60.0.0; cf_clearance=Zn_31_NYZRTEoXUU9U4ZmNtglGiDbTXzVl9g68guerQ-1716736800-1.0.1.1-a9LGvsxSouna2gNDTlVXqKlmckaD.HonsTUdoNjAXRumQYmMyFv0uSXBxlvstWBSoe1_dneyvp96hDwg9U0Vhw; c_dl_um=-; management_ques=1718199213695; c_segment=15; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1718202605,1718226557,1718250946,1718349628; m0_72947390comment_new=1718372139743; dc_session_id=10_1718599166103.323360; is_advert=1; creative_btn_mp=3; firstDie=1; _clck=qgkyji%7C2%7Cfmp%7C0%7C1567; SidecHatdocDescBoxNum=true; fe_request_id=1718606019662_4581_7070551; dc_sid=1ea6c25242946f01cf39d148facd8511; c_first_ref=www.bing.com; c_dl_prid=1718199316497_588345; c_dl_rid=1718609344051_229444; c_dl_fref=https://blog.csdn.net/lyzzs222/article/details/119701569; c_dl_fpage=/download/qq_30330655/12547344; c_utm_medium=distribute.pc_relevant.none-task-download-2%7Edefault%7EOPENSEARCH%7EPaidSort-1-12547344-blog-119701569.235%5Ev43%5Epc_blog_bottom_relevance_base4; c_utm_relevant_index=2; c_first_page=https%3A//blog.csdn.net/qq_41447478/article/details/114527367; c_dsid=11_1718609491331.309738; c_page_id=default; c_pref=https%3A//www.csdn.net/%3Fspm%3D1011.2124.3001.4476; c_ref=https%3A//mp.csdn.net/; log_Id_click=2877; _clsk=q2suyr%7C1718610171568%7C69%7C0%7Ck.clarity.ms%2Fcollect; log_Id_pv=3709; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1718610203; log_Id_view=64862; dc_tos=sf7s4g'
    # file_path = 'C:/Users/Administrator/Documents/Obsidian Vault/UE开发/Animation Blueprint.md'
    file_path = './markdown.txt'
    upload = UploadPic(cookie)
    transform = CSDNTransform(upload, file_path)
    markdown_text = transform.get_transform()

