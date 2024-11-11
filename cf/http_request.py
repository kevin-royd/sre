import requests


class Header:
    def __init__(self, profile):
        self.session = requests.Session()
        self.headers_map = {
            "No1": {
                'X-Auth-Email': 'x',
                'X-Auth-Key': 'x',
                'Content-Type': 'application/json'
            },
            'No2': {
                'X-Auth-Email': 'x',
                'X-Auth-Key': 'x',
                'Content-Type': 'application/json'
            },
            'No3': {
                'X-Auth-Email': 'x',
                'X-Auth-Key': 'x',
                'Content-Type': 'application/json'
            }
        }
        self.session.headers.update(self.headers_map.get(profile))

    def send_request(self, method, url, name, data=None, params=None):
        try:
            response = self.session.request(method, url, json=data, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"处理 {name} 错误: {e}")
            return None
        return response

    def get_account_info(self, url):
        items = []
        per_page = 100
        cursor = None  # 初始化游标为 None

        while True:
            # 构建请求参数
            params = {'per_page': per_page}
            if cursor:
                params['cursor'] = cursor
            # 发送请求
            response = self.send_request('GET', url, "get_info", params=params)
            # 检查响应状态
            if response.status_code == 200:
                data = response.json()
                # 获取返回的结果
                result_items = data.get('result', [])
                # 添加当前页数据
                items.extend(result_items)
                # 获取游标，用于下一次请求
                result_info = data.get('result_info', {})
                cursor = result_info.get('cursors', {}).get('after', None)
                # 如果没有游标，表示数据已经全部加载
                if not cursor:
                    print("No more items, pagination complete.")
                    break
            elif response.status_code == 400:
                print(f"Bad Request (400): {response.text}")
                # 打印详细的错误信息来分析问题
                return []

            else:
                print(f"Error: Received unexpected status code {response.status_code}.")
                return []

        print(f"Total items fetched: {len(items)}")
        return items