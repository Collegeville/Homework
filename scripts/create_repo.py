from config import *
from github import Github


def read_users(filename):
    with open(filename) as f:
        lines = f.readlines()
    users = []
    first_ls = lines[0].strip().split(',')
    username_index = first_ls.index("Username")
    for line in lines[1:]:
        users.append(line.split(',')[username_index].strip())
    return users


def run():
    users = read_users("users.csv")
    gh = Github(USERNAME, TOKEN)
    existing_repos = gh.get_organization_repos(ORGANIZATION)
    for user in users:
        if not gh.check_user_exist(user):
            print "User {} does not exit".format(user)
        else:
            repo = "{}_{}_{}".format(COURSE, TERM, user)
            if repo in existing_repos:
                print "User {} already had repo.".format(user)
            else:
                gh.create_organization_repo(ORGANIZATION, repo, "Sample description")
                gh.add_collaborator(ORGANIZATION, repo, user, permission="push")
                print "User {} has been added to repo".format(user)


if __name__ == '__main__':
    run()