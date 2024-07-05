import requests


class UploadPic:
    def __init__(self, cookie):
        self.cookie = cookie

        # 解析
        self.file_path = ""
        self.img_type = ""

        # 两个请求体
        self.upload_data = {}
        self.csdn_data = {}
        self.output_url = ""

    def _get_file(self, file_path):
        with open(file_path, mode="rb") as f:
            binary_data = f.read()
        return binary_data

    def _upload_request(self):
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json",
            "cookie": self.cookie,
            "origin": "https://editor.csdn.net",
            "priority": "u=1, i",
            "referer": "https://editor.csdn.net/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        }

        params = {
            "type": "blog",
            "rtype": "markdown",
            "x-image-template": "",
            "x-image-app": "direct_blog",
            "x-image-dir": "direct",
            "x-image-suffix": self.img_type,
        }

        url = "https://imgservice.csdn.net/direct/v1.0/image/upload"

        response = requests.get(url, params=params, headers=headers)
        try:
            self.upload_data = response.json()
        except Exception as e:
            return e

    def _csdn_request(self):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Origin": "https://editor.csdn.net",
            "Referer": "https://editor.csdn.net/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }

        files = {
            "key": (None, self.upload_data["data"]["filePath"]),
            "policy": (None, self.upload_data["data"]["policy"]),
            "OSSAccessKeyId": (None, self.upload_data["data"]["accessId"]),
            "success_action_status": (None, "200"),
            "signature": (None, self.upload_data["data"]["signature"]),
            "callback": (None, self.upload_data["data"]["callbackUrl"]),
            "file": (
                f"image.{self.img_type}",
                self._get_file(self.file_path),
                f"image/{self.img_type}",
            ),
        }

        url = "https://csdn-img-blog.oss-cn-beijing.aliyuncs.com/"

        response = requests.post(url, headers=headers, files=files)
        try:
            self.csdn_data = response.json()
            self.output_url = self.csdn_data["data"]["imageUrl"]
        except Exception as e:
            return e

    def upload_image(self, file_path):
        self.file_path = file_path
        self.img_type = self.file_path.split(".")[-1]

        exception_1 = self._upload_request()
        assert exception_1 is None, exception_1
        exception_2 = self._csdn_request()
        assert exception_2 is None, exception_2

        return self.output_url


if __name__ == "__main__":
    cookie = ""
    image_path = "需要上传的图片路径"
    upload = UploadPic(cookie)
    url = upload.upload_image(image_path)
    print(url)
