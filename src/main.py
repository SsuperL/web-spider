from http_util import HTTPManager


def main():
    http_manager = HTTPManager()
    http_manager.post(
        "https://xskydata.jobs.feishu.cn/api/v1/search/job/posts","res.json")


if __name__ == '__main__':
    main()
