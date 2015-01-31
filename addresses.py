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
                if done:
                    break
                email = commit['author']['email']
                if 'no-reply' not in email:
                    yield member['name'], email
                    done = True
        break
