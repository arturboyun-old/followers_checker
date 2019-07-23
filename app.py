import requests
from flask import Flask, render_template, request, redirect, url_for
from instagram_private_api import Client, ClientCompatPatch
from instagram_private_api.errors import ClientError
from json.decoder import JSONDecodeError

app = Flask(__name__)

user_name = 'archieruin'
password = '102938382910RuinArchie'

api = Client(user_name, password)
rank_token = Client.generate_uuid()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/output', methods=['POST'])
def output():
    global first_second_followers
    if request.method == 'POST':
        first_username = request.form['first_username']
        second_username = request.form['second_username']
        try:
            first_followers = get_followers(first_username)
            second_followers = get_followers(second_username)
            first_second_followers = [username for username in first_followers if username in second_followers]
            show_error = False
        except ClientError:
            show_error = True
        return render_template('index.html', usernames=first_second_followers,
                               users_count=len(first_second_followers), show_error=show_error)
    else:
        return redirect(url_for('index'))


def get_followers(username):
    users = api.user_followers(get_user_id(username), rank_token).get('users')
    return [user['username'] for user in users]


def get_user_id(username):
    r = requests.get('https://www.instagram.com/{username}/?__a=1'.format(username=username))
    try:
        user_id = r.json()['logging_page_id'].split('_')[1]
    except JSONDecodeError:
        return 1
    return user_id


if __name__ == '__main__':
    app.run()
