#!/usr/bin/env python3
import os, json, pickle
import yaml, requests, vlermv

members_url = 'https://api.github.com/orgs/cyberwizardinstitute/members'
hub = os.path.expanduser('~/.config/hub')
headers = {
    'Authorization': 'token %s' % yaml.load(open(hub))['github.com'][0]['oauth_token']
}

def main():
    import csv, sys
    w = csv.writer(sys.stdout)
    w.writerow(('name', 'email_address'))
    w.writerows(itermembers())

@vlermv.cache('~/.github-email-addresses', serializer = pickle)
def get(url):
    return json.loads(requests.get(url, headers = headers).text)

def itermembers():
    members = get(members_url)
    for member in members:
        done = False
        repositories = get(member['repos_url'])
        for repository in repositories:
            if done:
                break
            commits_url = repositories[0]['commits_url'].replace('{/sha}', '')
            commits = get(commits_url)
            for commit in commits:
                if done or commit == None or type(commit) == str:
                    continue
                real_commit = commit['commit']
                author = real_commit['author']

                name = author.get('name', member['login'])
                email = author['email']
                if email != None and 'no-reply' not in email:
                    yield name, email
                    done = True

if __name__ == '__main__':
    main()
