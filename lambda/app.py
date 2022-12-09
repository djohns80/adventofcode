import json
import os
from datetime import date, datetime
import urllib3
import boto3

s3 = boto3.client('s3')
sec = boto3.client('secretsmanager')
http = urllib3.PoolManager()

get_secret_value = sec.get_secret_value(SecretId = os.environ['SECRET_ARN'])
secret = json.loads(get_secret_value['SecretString'])
today = date.today()

def get_current_leaderboard():
    cookies = [('session', secret['SessionToken'])]
    headers = {'Cookie': '; '.join([f'{c[0]}={c[1]}' for c in cookies])}
    req = http.request('GET', f"https://adventofcode.com/{today.year}/leaderboard/private/view/{secret['LeaderBoard']}.json", headers=headers)
    put_leaderboard_s3(req.data)
    return json.loads(req.data.decode('utf-8'))

def put_leaderboard_s3(data):
    s3.put_object(
        Bucket = os.environ['S3_BUCKET'],
        Key = f"{os.environ['S3_PREFIX']}/{today.year}/{secret['LeaderBoard']}.json",
        Body = data
    )

def get_previous_leaderboard():
    get_object = s3.get_object(
        Bucket = os.environ['S3_BUCKET'],
        Key = f"{os.environ['S3_PREFIX']}/{today.year}/{secret['LeaderBoard']}.json"
    )
    return json.loads(get_object['Body'].read().decode('utf-8'))

def post_slack_message(message):
    slack_url = secret['WebhookUrl']
    resp = http.request('POST', slack_url, body = json.dumps({'message': message}).encode('utf-8'))
    return resp

def diff_members(prev, curr):
    join = [v['name'] for k,v in curr['members'].items() if k not in prev['members']]
    left = [v['name'] for k,v in prev['members'].items() if k not in curr['members']]
    return {'left': left, 'join': join}

def completed_parts(prev, curr):
    completed_curr = [{'id': km, 'name': vm['name'], 'day': kd, 'part': kl, 'timestamp': vl['get_star_ts']} for km, vm in curr['members'].items() for kd, vd in vm['completion_day_level'].items() for kl, vl in vd.items()]
    completed_prev = [{'id': km, 'name': vm['name'], 'day': kd, 'part': kl, 'timestamp': vl['get_star_ts']} for km, vm in prev['members'].items() for kd, vd in vm['completion_day_level'].items() for kl, vl in vd.items()]
    return [c for c in completed_curr if c not in completed_prev]

def handler(event, context):
    prev_leaderboard = get_previous_leaderboard()
    curr_leaderboard = get_current_leaderboard()

    members = diff_members(prev_leaderboard, curr_leaderboard)
    print(members)
    for m in members['left']:
        post_slack_message(f'{m} has left the leaderboard.')
    for m in members['join']:
        post_slack_message(f'{m} has joined the leaderboard.')

    parts = completed_parts(prev_leaderboard, curr_leaderboard)
    print(parts)
    sorted_parts = sorted(parts, key=lambda k: k['timestamp'])
    for p in sorted_parts:
        post_slack_message(f"{p['name']} completed part {p['part']} from day {p['day']} at {datetime.fromtimestamp(p['timestamp'])} UTC")
