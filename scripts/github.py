import requests
import json


class Github(object):
    def __init__(self, username, token):
        self.auth = (username, token)
        self.base_url = 'https://api.github.com'

    def check_user_exist(self, user):
        url = self.base_url + "/users/{}".format(user)
        res = requests.get(url, auth=self.auth)
        return res.status_code == 200

    def create_organization_repo(self, organization, repo, description, private=False):
        url = self.base_url + '/orgs/{}/repos'.format(organization)
        data = {
            "name": repo,
            "description": description,
            "homepage": "https://github.com",
            "private": private,
            "has_issues": True,
            "has_wiki": True,
            "has_downloads": True
        }
        res = requests.post(url, auth=self.auth, data=json.dumps(data))
        return res.status_code == 201

    def add_collaborator(self, owner, repo, collaborator, permission="pull"):
        url = self.base_url + "/repos/{}/{}/collaborators/{}".format(owner, repo, collaborator)
        data = {
            "permission": permission
        }
        res = requests.put(url, auth=self.auth, data=json.dumps(data))
        return res.status_code == 204

    def delete_collaborator(self, owner, repo, collaborator):
        url = self.base_url + "/repos/{}/{}/collaborators/{}".format(owner, repo, collaborator)
        res = requests.delete(url, auth=self.auth)
        return res.status_code == 204

    def delete_organization_repo(self, owner, repo):
        url = self.base_url + "/repos/{}/{}".format(owner, repo)
        res = requests.delete(url, auth=self.auth)
        return res.status_code == 204

    def get_organization_repos(self, organization):
        url = self.base_url + "/orgs/{}/repos".format(organization)
        res = requests.get(url, auth=self.auth)
        ls = json.loads(res.text)
        return [x["name"] for x in ls]