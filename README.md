# Diff Collector
- A tool to collect diffs from git repositories.
- This tool is used for collecting diff files from pool used in [SimilarPatchIdentifier](https://github.com/ISEL-HGU/SimilarPatchIdentifier)

## diffcollector.py
- This script collects diffs from git repository and stores them in files
- The script takes a file as input which contains the BIC commit id, BFC commit id, BIC file path and BFC file path, git url and jira key.
- To launch the script, run the following command
> `python diffcollector.py {commit file path}`