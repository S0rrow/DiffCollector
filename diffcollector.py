import sys
import os
import subprocess
import git

def clone(github_url:str):
    # current working directory
    cwd = os.getcwd()
    # check if repo directory exists
    if not os.path.exists('repo'):
        os.mkdir('repo')
    # check if sources directory exists
    if not os.path.exists('sources'):
        os.mkdir('sources')
    # clone the repository under the repo folder
    git.Git(os.path.join(cwd, 'repo')).clone(github_url)
    # return the path to the local repository
    return os.path.join(cwd, 'repo', reponame(github_url))

def checkout(gitpath:str, hash:str):
    git.Git(gitpath).checkout(hash)

def copy_file(local_repo:str, file:str, dest:str, new_name:str=None):
    # copy the file from the local repo to the destination
    try:
        if new_name is None:
            subprocess.run(['cp', os.path.join(local_repo, file), dest])
        else:
            subprocess.run(['cp', os.path.join(local_repo, file), os.path.join(dest, new_name)])
    except Exception as e:
        print(f'file {file} not found')
        return False
    return True

def read_input(line:str):
    line = line.split(',')
    hash1 = line[0]
    hash2 = line[1]
    file1 = line[2]
    file2 = line[3]
    github_url = line[4]
    jira_key = line[5]
    return hash1, hash2, file1, file2, github_url, jira_key

# extract the repository name from the github url or local path
def reponame(github_url:str):
    return github_url.split('/')[-1].split('.')[0]

# extract git diff from the two files
def extract_diff(rev1:str, rev2:str, source1:str, source2:str, local_repo:str, execution_index:int, dest:str='diffs'):
    try:
        if not os.path.exists(dest):
            os.mkdir(dest)
        # get the diff
        # git diff rev1:source1 rev2:source2
        diff = git.Git(local_repo).diff(f'{rev1}:{source1}', f'{rev2}:{source2}')
        # write the diff to a file
        with open(os.path.join(dest, f"diff_{reponame(local_repo)}_{execution_index}.txt"), 'w') as f:
            f.write(diff)
        # return execution result
    except:
        print(f'error extracting diff from {source1} and {source2} on {local_repo}')
        return False
    return True

def path_to_filename(path:str):
    return path.split('/')[-1]

def main(args):
    # csv file to read
    # default
    path = '/home/codemodel/turbstructor/SimilarPatchIdentifier/components/LCE/commit_file.csv'
    # if argument given
    if len(args) > 1:
        path = args[1]    
    print(f"reading input from {path}")
    # read csv file line by line
    with open(path, 'r') as f:
        lines = f.readlines()
    lineindex = 0
    # for each line, and index
    for line in lines:
        if line=='' or line=='\n' or len(line)==0:
            continue
        hash1, hash2, file1, file2, github_url, jira_key = read_input(line)
        print(f"jira key: {jira_key}")
        # clone the repository
        repo_name = reponame(github_url)
        # if the repo is already cloned, skip the clone step
        if not os.path.exists(os.path.join('repo', repo_name)):
            local_repo = clone(github_url)
        else:
            local_repo = os.path.join('repo', repo_name)
        # extract the diff
        extract_diff(hash1, hash2, file1, file2, local_repo, lineindex)
        lineindex += 1
    print(f"done")
    exit(0)

if __name__ == "__main__":
    main(sys.argv)