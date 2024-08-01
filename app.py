from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def get_proxy():
    proxy = []
    with open('proxy.txt', encoding='utf-8') as file:
        file_data = file.read().split('\n')
    for proxy_row in file_data:
        proxy.append(
            dict(
                zip(
                    ('ip', 'port', 'proxy_type', 'anonymity', 'timeout',
                     'country', 'country_code'),
                    proxy_row.split(', '))
            )
        )
    return jsonify(proxy)


if __name__ == '__main__':
    from proxy_check import check_start

    check_start()
    app.run()
