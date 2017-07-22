"""
reference:
https://github.com/michaelliao/githubpy
githubpy is a simple Python SDK for GitHub's API v3. It's all contained in one easy-to-use file.
"""

import github

def get_user_info(gh,user):
    info=gh.users(user).get()
    for key,value in info.items():
        print(key,value)

def get_repo_issues(gh,user,repo):
    issue= gh.repos(user)(repo).issues.get(state='open')
    print(issue)

def main():
    
    gh=github.GitHub()
    #input your github account name below
    user='terasakisatoshi'
    repo='PythonCode'
    get_user_info(gh,user)
    #get_repo_issues(gh,user,repo)



if __name__ == '__main__':
    main()