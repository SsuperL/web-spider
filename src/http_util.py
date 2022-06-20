
import json
import logging
import requests


COOKIE = "passport_web_did=7039262390625681409; trust_browser_id=3a777241-65ef-4af1-aea1-01c3f8281483; fid=8951a448-be16-437f-9e48-347d8acbbd9c; new_web_session_list_tag=done; lang=zh; _ga=GA1.2.913932656.1639970235; __tea__ug__uid=7043620289230980616; session=XN0YXJ0-a81sdf60-3dc8-402b-9ddb-0a2ad08765d5-WVuZA; session_list=XN0YXJ0-a81sdf60-3dc8-402b-9ddb-0a2ad08765d5-WVuZA_XN0YXJ0-309hce0b-a45d-45df-a825-fd1c79e7f1da-WVuZA; is_anonymous_session=; Hm_lvt_e78c0cb1b97ef970304b53d2097845fd=1653375260,1654740402; locale=zh-CN; Hm_lpvt_e78c0cb1b97ef970304b53d2097845fd=1655259332; QXV0aHpDb250ZXh0=7293bae1edce48fab99a4f36f65f1681; _csrf_token=96dbcfed9c9184bab11d6a5ce22e2380f49eafe7-1657609866; swp_csrf_token=919cc7ef-b2e8-4d06-823a-7318766db6dc; t_beda37=b966c2f0775d6ce389eadcc8dd7fff55693b3ca2a2c5944180f4a9abd70ab588; channel=saas-career; platform=pc; s_v_web_id=verify_l5rigr7a_5KKHQEWb_utb3_4uuB_9QFx_gMwbEzdXqMwE; device-id=7121893088129304102; atsx-csrf-token=zZdqR2S7IvWlxZ5Zftoh1rUTU9h749m0l8q0xP8zai0%3D"
X_CSRF_TOKEN = "zZdqR2S7IvWlxZ5Zftoh1rUTU9h749m0l8q0xP8zai0="


class HTTPManager:
    """http请求封装"""

    def post(self, url: str, filepath: str):
        """
        :param url: 请求url
        :param filepath: 文件存储路径
        """
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-length": "194",
            "content-type": "application/json",
            "env": "undefined",
            "origin": "https://xskydata.jobs.feishu.cn",
            "portal-channel": "saas-career",
            "portal-platform": "pc",
            "referer": "https://xskydata.jobs.feishu.cn/school",
            "sec-ch-ua": '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
            "sec-ch-ua-mobile": "0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "x-csrf-token": X_CSRF_TOKEN,
            "cookie": COOKIE,
            "website-path": "school",
            "sec-fetch-site": "same-origin"
        }
        data = {"keyword": "", "limit": 36, "offset": 0, "job_category_id_list": [], "location_code_list": [
        ], "subject_id_list": [], "recruitment_id_list": [], "portal_type": 6, "job_function_id_list": [], "portal_entrance": 1}
       
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                job_list = response.json().get('data', {}).get('job_post_list')
            else:
                logging.error('failed to get response')
                return
        except Exception as e:
            logging.error("failed to get response, error: %s", str(e))
            raise e

        res_dict = {}
        for item in job_list:
            res_dict[item["id"]] = {}
            res_dict[item["id"]].update({
                "title": item["title"],
                "description": item["description"],
                "requirement": item["requirement"],
                "job_category": item["job_category"].get('name'),
                "recruit_type": item["recruit_type"].get('name'),
                "city": item["city_list"][0].get('name'),
            })

        with open(filepath, 'w') as fp:
            json.dump(res_dict, fp, ensure_ascii=False, indent=4)
