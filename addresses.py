#!/usr/bin/env python3
import requests

members_url = 'https://api.github.com/orgs/cyberwizardinstitute/members'

def main():
    import csv, sys
    w = csv.writer(sys.stdout)
    w.writerow(('name', 'email_address'))
    w.writerows(itermembers())

def itermembers():
    for member in requests.get(members_url).json():
        done = False
        repositories = requests.get(member['repos_url']).json()
        for repository in repositories:
            if done:
                break
            commits_url = repositories[0]['commits_url'].replace('{/sha}', '')
            commits = requests.get(commits_url).json()
            for commit in commits:
                if done or commit == None:
                    continue

                real_commit = commit['commit']
                author = real_commit['author']
                email = author['email']
                if email != None and 'no-reply' not in email:
                    yield real_commit.get('name', member['login']), email
                    done = True
        break

if __name__ == '__main__':
    main()
