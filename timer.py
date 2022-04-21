import time
import requests


class Response:
    def __init__(self):
        self.url = "http://127.0.0.1:8000/monitor/"

    def get_html(self, url):
        html = requests.get(url=url).text
        return html

    def run(self):
        while True:
            self.get_html(self.url)
            time.sleep(60)


if __name__ == '__main__':
    res = Response()
    res.run()
