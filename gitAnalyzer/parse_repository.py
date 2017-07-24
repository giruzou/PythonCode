import git
from pprint import pprint

LOCAL_REPOSITORY = '/Users/terasakisatoshi/Documents/work/mps-cancer'
ITEMS = ['author', 'authored_datetime', 'hexsha', 'message',
         'name_rev', 'parents', 'stats', 'summary']

class Commit(object):

    def __init__(self, commit, items):
        self.commit = commit
        self.items = items

    def show(self):
        for item in self.items:
            if item == 'parents':
                print(item, '=')
                for parent in eval('self.commit.%s' % item):
                    print(parent)
            elif item == 'stats':
                print(item,'=')
                print(self.commit.stats.total)
                print(self.commit.stats.files)
            else:
                print(item, '=', eval('self.commit.%s' % item))

class Repository(object):

    def __init__(self, local_repository, items):
        self.repo_path = local_repository
        self.items = items
        self.repository = git.Repo(self.repo_path)

    def extract_commits(self, branch, max_count=None):
        if max_count:
            objects = self.repository.iter_commits(branch, max_count=max_count)
        else:
            objects = self.repository.iter_commits(branch)
        self.commits = [Commit(obj, self.items) for obj in objects]
        return self.commits

def main():
    repository=Repository(LOCAL_REPOSITORY,ITEMS)
    main_branch='develop'
    for commit in repository.extract_commits(main_branch,max_count=10):
        commit.show()

if __name__ == '__main__':
    main()
