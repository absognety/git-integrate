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
6. Add `.gitignore` to ignore redundant local cache, untracked files, hidden system files, files generated at run time.  

## How to deploy this:  
1. Clone this repository using `git clone https://github.com/absognety/git-integrate.git`.  
2. Navigate to git repository directory (cd `git-integrate`).  
3. Do `pip install -e .`  
4. `import git_integrate` and start using this package`.  
  
## Known Bugs:  
+ Currently this application is using rate-limit values of a github API (5000 requests per hour).  
+ The python github connector used here is `PyGithub`. Instead of using API throttling techniques, I minimized the events usage to a window of 2 months by default for the simplicity purposes.  
+ Advanced techniques to handle rate-limit exceeding can be done by: 
  - 1. Introducing delays.  
  - 2. Run multiple threads of the same process (`Thread spawning`), (Use `multiprocessing`) - But maintaining this complex application with metadata and log management is challenging.  
  - 3. Using `cache stores` like `Redis` (or use existing db) to avoid repetitively hitting the API for events that are already consumed - This will remove the tendency of having dupicate records in db.  
  
## What would I have done if I had more time:  
+ Currently code written is using rule based logic to look for issues labeled `Bug` and `Performance` with conjunctions to compute defect density and performance issue percentage. We can use NLP based techniques here to build a vocabulary of words used in labels and Build a text similarity model that gives words similar to `Bug` and `Performance` - This will give us much more accurate numbers of defect density and performance issue percentages.  
+ The lag proposed in the assignment is 30 min, but I built my solution in such a way that I am storing last known timestamp when the run is happening in a tempfile and that tempfile will be read in the next run if tempfile exists, if not it will hit API for last 2 months of events.  
+ This solution can expect a loss of data of 1 or 2 events based on way it is implemented now, (Example: if an issue is created in the window before last saved timestamp and current timestamp - Much more efficient solution is setup a producer and consumer (Maybe a kafka solution) to have continuous stream of events
