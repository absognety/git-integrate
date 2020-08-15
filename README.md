# Github Integration API:  
## What is it?  
**git-integrate** is a python package for flexible and seamless integration with Github to parse and collect crucial information about github repositories and store them in schema of your choice (NoSQL/RDBMS/Graph data stores). The objective of this package is to capture important KPIs to understand how the user behaviour is flowing across time with respect to commits/pull requests/issues/subscribers/watchers/stargazers/forks etc.  
  
## Requirements:  
  
**Objective** : Improve the overall development process quality of a github project.KPIs Identified:  
**KPI1** : Average defect density in GitHub commits must not exceed X  
**KPI2** : Maximum average time to merge a PR into master branch must not exceed Y  
**KPI3** : A minimum of Z performance improvement issue percentage.  
  
Github integration that calculates these for a list of projects and updates them every 30-minutes and keeps a record of all the computations in sql/nosql DB store. Try to retain historical data of all these metrics over time to allow data scientists to build models on top of this.  
  
  
## Definitions of metrics/KPIs:  
  
**Defect density** = (Number of issues with the label bug)/Total number of issues.  
**Performance issue %** = ((Number of issues with the label performance)/Total number of issues) X 100.  
  
## Main features:  
In order to restore the simplicity of this intitative for now, the features embedded in this project are limited.  
+ Currently the subroutines added to this codebase will handle the following:  
  - Perform REST API calls to [Github API v3](https://docs.github.com/en/rest) to capture the attributes associated with all issues of a project (Including pull requests).  
  - Parsing of API responses and storing them in selective RDBMS schema (sqlite DB store is used in this project).  
  - Populate sqlite DB tables with updated issues information for every N minuties/hours (N is arbitrary).  
  
## Number of KPIs Completed:  
**Completed two of 3 KPIs (KPI1 & KPI3)**.  
  
## KPIs which are Work in Progress:  
This requires capturing `created_time` and `merge_time` of all issues with `is_pull_request` flag as `true` and computing the difference and storing it in our db - Essentially another function that does this task.  

## Development steps:  
1. This codebase of this project is distributed as a python package.  
2. Write helper functions and driver code that achieve required functionality.  
3. Add `setup.py` to describe the package information and attributes (more can be added, for example: Ability to run to from command line terminal like a CLI script with arguments provided).  
4. Add `requirements.txt` for the dependencies.   
5. Add `README.md`  
6. Add `.gitignore` to ignore redundant local cache, untracked files, hidden system files, files generated at run time.  

## How to deploy this:  
0. Create a personal access token for your github account and add it to the environment variables so that sdk will read it. (In Linux based systems: Add it to ~/.bashrc - export GIT_ACCESS_TOKEN=XXXXXXXXXXXXXXXXXYYYYYYYYY).  
1. Clone this repository using `git clone https://github.com/absognety/git-integrate.git`.  
2. Navigate to git repository directory (cd `git-integrate`).  
3. Do `pip install -e .`  
4. `import git_integrate` and start using this package`.  
5. Setup a custom script where you can have only 2 lines:  
For example:  
```
import git_integrate
result = git_integrate.populate_tables('pandas-dev/pandas') #give repo_name (org_name/repo_name) - check the docstrings using help(git_integrate)
```
Schedule this script by generating a crontab schedule for every 30 min/1 hour etc (More advanced workflows can be managed by prefect, airflow - open to user).  
  
## Known Bugs:  
+ Currently this application is using rate-limit values of a github API (5000 requests per hour).  
+ The python github connector used here is `PyGithub`. Instead of using API throttling techniques, I minimized the events usage to a window of 2 months by default for the simplicity purposes.  
+ Advanced techniques to handle rate-limit exceeding can be done by: 
  - 1. Introducing delays.  
  - 2. Run multiple threads of the same process (`Thread spawning`), (Use `multiprocessing`) - But maintaining this complex application with metadata and log management is challenging.  
  - 3. Using `cache stores` like `Redis` (or use existing db) to avoid repetitively hitting the API for events that are already consumed - This will remove the tendency of having dupicate records in db.  
+ credentials/access tokens configuration is a bit of a bottleneck. (We can research generation of token on the fly using API itself - haven't done it yet).  

## Future Ideas:  
+ Currently code written is using rule based logic to look for issues labeled `Bug` and `Performance` with conjunctions to compute defect density and performance issue percentage. We can use NLP based techniques here to build a vocabulary of words used in labels and Build a text similarity model that gives words similar to `Bug` and `Performance` - This will give us much more accurate numbers of defect density and performance issue percentages.  
+ The lag proposed for now is 30 min, but I built my solution in such a way that I am storing last known timestamp when the run is happening in a tempfile and that tempfile will be read in the next run if tempfile exists, if not it will hit API for last 2 months of events based on updated time attribute.      
+ This solution can expect a loss of data of 1 or 2 events based on way it is implemented now, (Example: if an issue is created in the window before last saved timestamp and current timestamp - Much more efficient solution is setup a producer and consumer (Maybe a kafka solution) to have continuous stream of events.  

## Output schemas:  
1. Issues detailed table:  
  
| project_id | issue_id  | is_pull_request | labels                                  | body | title                                                            | state | created_time        | created_date | updated_time        | updated_date | closed_time | closed_date |
|------------|-----------|-----------------|-----------------------------------------|------|------------------------------------------------------------------|-------|---------------------|--------------|---------------------|--------------|-------------|-------------|
| 167174     | 668193508 | true            | Attributes;Behavior Change;Needs review | XXXX | Attributes: Drop the `toggleClass(boolean\|undefined)` signature | open  | 2020-07-29 21:57:20 | 2020-07-29   | 2020-07-30 23:30:32 | 2020-07-30   |             |             |
| 167174     | 667938072 | true            | Event;Needs review                      | YYYY | Event: Remove the event.which shim                               | open  | 2020-07-29 15:32:54 | 2020-07-29   | 2020-07-31 00:28:13 | 2020-07-31   |             |             |
| 167174     | 667933925 | true            | Needs review;Tests                      | ZZZZ | Tests: Recognize callbacks with dots in the Node.js mock server  | open  | 2020-07-29 15:26:54 | 2020-07-29   | 2020-07-30 01:52:19 | 2020-07-30   |             |             |  
  
    
2. Computed KPIS table:  
  
| project_id | project           | from                | to                  | avg_defect_density | perf_issue_percent |
|------------|-------------------|---------------------|---------------------|--------------------|--------------------|
| 858127     | pandas-dev/pandas | 2020-06-05 11:22:37 | 2020-08-05 11:17:48 | 0.418114143920596  | 4.71464019851117   |
| 858127     | pandas-dev/pandas | 2020-06-04 23:43:22 | 2020-08-04 23:38:36 | 0.416770963704631  | 4.75594493116396   |  

Checkout `git_integrate/sqlite.db` to have a peek at the tables.  
