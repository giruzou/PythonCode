import git
from collections import defaultdict

LOCAL_REPOSITORY = '/Users/terasakisatoshi/Documents/work/mps-cancer'
ITEMS = ['author', 'authored_datetime', 'hexsha', 'message',
         'name_rev', 'parents', 'stats', 'summary']


class Commit(object):

    def __init__(self, commit, items):
        self.commit = commit
        self.items = items

    def __getattr__(self, name):
        return getattr(self.commit, name)

    def show(self):
        for item in self.items:
            if item == 'parents':
                print(item, '=')
                for parent in eval('self.commit.%s' % item):
                    print(parent)
            elif item == 'stats':
                print(item, '=')
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
    repository = Repository(LOCAL_REPOSITORY, ITEMS)
    main_branch = 'develop'
    repo_info = repository.extract_commits(main_branch)
    # for commit in repo_info:
    #    commit.show()
    authors = defaultdict(list)
    for commit in repo_info:
        authors[commit.author].append(commit)

    print("commit contribute share")
    for key, value in authors.items():
        print(key, 100.0*len(value)/len(repo_info), "%")


if __name__ == '__main__':
    main()
