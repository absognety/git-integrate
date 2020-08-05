# Github Integration API:  
## What is it?  
**git-integrate** is a python package for flexible and seamless integration with Github to parse and collect crucial information about github repositories and store them in schema of your choice (NoSQL/RDBMS/Graph data stores). The objective of this package is to capture important KPIs to understand how the user behaviour is flowing across time with respect to commits/pull requests/issues/subscribers/watchers/stargazers/forks etc.  
  
## Main features:  
In order to restore the simplicity of this project, the features embedded this project are limited.  
+ Currently the subroutines added to this codebase will handle the following:  
  - Perform REST API calls to [Github API v3](https://docs.github.com/en/rest) to capture the attributes associated with all issues of a project (Including pull requests).  
  - Parsing of API responses and storing them in selective RDBMS schema (sqlite DB store is used in this project).  
  - Populate sqlite DB tables with updated issues information for every N minuties/hours (N is arbitrary).  
  
## Number of KRs Completed:  
**Completed two of 3 KRs (KR1 & KR3)**.  
  
## Number of KRs not Completed:  
**KR2 not completed**.  

## Development steps:  
1. This codebase of this project is distributed as a python package.  
2. Write helper functions and driver code that achieve required functionality.  
3. Add `setup.py` to describe the package information and attributes (more can be added, for example: Ability to run to from command line terminal like a CLI script with arguments provided).  
4. Add `requirements.txt` for the dependencies.   
5. Add `README.md`  
6. Add `.gitignore` to redundant local cache, untracked files, hidden system files, files generated at run time.  

## How to deploy this:  
1. Clone this repository using `git clone https://github.com/absognety/git-integrate.git`.  
2. Navigate to git repository directory (cd `git-integrate`).  
3. Do `pip install -e .`  
4. `import git_integrate` and start using this package`.  
