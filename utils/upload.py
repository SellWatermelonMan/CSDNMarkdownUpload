import requests


class UploadPic:
    def __init__(self, cookie):
        self.cookie = cookie

        # 解析
        self.file_path = ''
        self.img_type = ''

        # 两个请求体
        self.upload_data = {}
        self.csdn_data = {}
        self.output_url = ''

    def _get_file(self, file_path):
        with open(file_path, mode='rb') as f:
            binary_data = f.read()
        return binary_data

    def _upload_request(self):
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-type': 'application/json',
            'cookie': self.cookie,
            'origin': 'https://editor.csdn.net',
            'priority': 'u=1, i',
            'referer': 'https://editor.csdn.net/',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }

        params = {
            'type': 'blog',
            'rtype': 'markdown',
            'x-image-template': '',
            'x-image-app': 'direct_blog',
            'x-image-dir': 'direct',
            'x-image-suffix': self.img_type,
        }

        url = 'https://imgservice.csdn.net/direct/v1.0/image/upload'

        response = requests.get(url, params=params, headers=headers)
        try:
            self.upload_data = response.json()
        except Exception as e:
            return e

    def _csdn_request(self):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Origin': 'https://editor.csdn.net',
            'Referer': 'https://editor.csdn.net/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        files = {
            'key': (None, self.upload_data['data']['filePath']),
            'policy': (None, self.upload_data['data']['policy']),
            'OSSAccessKeyId': (None, self.upload_data['data']['accessId']),
            'success_action_status': (None, '200'),
            'signature': (None, self.upload_data['data']['signature']),
            'callback': (None, self.upload_data['data']['callbackUrl']),
            'file': (f'image.{self.img_type}', self._get_file(self.file_path), f'image/{self.img_type}'),
        }

        url = 'https://csdn-img-blog.oss-cn-beijing.aliyuncs.com/'

        response = requests.post(url, headers=headers, files=files)
        try:
            self.csdn_data = response.json()
            self.output_url = self.csdn_data['data']['imageUrl']
        except Exception as e:
            return e

    def upload_image(self, file_path):
        self.file_path = file_path
        self.img_type = self.file_path.split('.')[-1]

        exception_1 = self._upload_request()
        assert exception_1 is None, exception_1
        exception_2 = self._csdn_request()
        assert exception_2 is None, exception_2

        return self.output_url


if __name__ == '__main__':
    cookie = 'uuid_tt_dd=10_20714563540-1713279603925-839503; c_adb=1; UserName=m0_72947390; UserInfo=dc1d0c7f5d4c41d1a2269fc9e40e106e; UserToken=dc1d0c7f5d4c41d1a2269fc9e40e106e; UserNick=Bigcrab__; AU=B30; UN=m0_72947390; BT=1713280879102; p_uid=U010000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22m0_72947390%22%2C%22scope%22%3A1%7D%7D; _ga=GA1.1.1507512576.1713742454; _ga_7W1N0GEY1P=GS1.1.1713742454.1.1.1713743378.60.0.0; cf_clearance=Zn_31_NYZRTEoXUU9U4ZmNtglGiDbTXzVl9g68guerQ-1716736800-1.0.1.1-a9LGvsxSouna2gNDTlVXqKlmckaD.HonsTUdoNjAXRumQYmMyFv0uSXBxlvstWBSoe1_dneyvp96hDwg9U0Vhw; c_dl_um=-; management_ques=1718199213695; c_segment=15; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1718202605,1718226557,1718250946,1718349628; m0_72947390comment_new=1718372139743; dc_session_id=10_1718599166103.323360; is_advert=1; creative_btn_mp=3; firstDie=1; _clck=qgkyji%7C2%7Cfmp%7C0%7C1567; SidecHatdocDescBoxNum=true; fe_request_id=1718606019662_4581_7070551; dc_sid=1ea6c25242946f01cf39d148facd8511; c_first_ref=www.bing.com; c_dl_prid=1718199316497_588345; c_dl_rid=1718609344051_229444; c_dl_fref=https://blog.csdn.net/lyzzs222/article/details/119701569; c_dl_fpage=/download/qq_30330655/12547344; c_utm_medium=distribute.pc_relevant.none-task-download-2%7Edefault%7EOPENSEARCH%7EPaidSort-1-12547344-blog-119701569.235%5Ev43%5Epc_blog_bottom_relevance_base4; c_utm_relevant_index=2; c_first_page=https%3A//blog.csdn.net/qq_41447478/article/details/114527367; c_dsid=11_1718609491331.309738; c_page_id=default; c_pref=https%3A//www.csdn.net/%3Fspm%3D1011.2124.3001.4476; c_ref=https%3A//mp.csdn.net/; log_Id_click=2877; _clsk=q2suyr%7C1718610171568%7C69%7C0%7Ck.clarity.ms%2Fcollect; log_Id_pv=3709; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1718610203; log_Id_view=64862; dc_tos=sf7s4g'
    upload = UploadPic(cookie)
    url = upload.upload_image('./微信截图_20240617161210.png')
    print(url)


