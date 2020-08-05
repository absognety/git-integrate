import os
import pandas as pd
from github import Github
from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dateutil
import logging
from .dbstore import create_connection

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
#Initialize your assigned access token
#Add your credentials to ~/.bashrc or obfuscate it some other way
access_token = os.environ['GIT_ACCESS_TOKEN']
thisdir = os.path.dirname(__file__)

try:
    os.makedirs(os.path.join(thisdir,'logs'))
except:
    pass
    
def initialize_repo(repo_name:str):
    """
    params:
        repo_name:str: Repository name (format: organization_name/repository_name)
    output:
        Repository Object
    """
    #Instantiate a Github object
    git = Github(login_or_token=access_token)
    repo = git.get_repo(repo_name)
    return repo

def store_issue_attrs(repo_name:str,state:str,since:datetime) -> tuple:
    """

    Parameters
    ----------
    repo_name : str
        Repository name (format: organization_name/repository_name)
    state : str
        State of issues ('open'/'closed')
    since : str
        a datetime object

    Returns
    -------
    tuple
        Tuple of two tables:
            1. Detailed issues information parsed from API response
            2. Computed statistics from given input payload

    """
    repo = initialize_repo(repo_name)
    df_dict = defaultdict(list)
    for issue in repo.get_issues(state=state,since=since):
        
        #pass the repo name
        df_dict['project_id'].append(repo.id)
        
        # pass the id
        df_dict['issue_id'].append(issue.id)
        
        # pass boolean pull_request
        if issue.pull_request:
            df_dict['is_pull_request'].append('true')
        else:
            df_dict['is_pull_request'].append('false')
            
        #parse label names from github.label.Label object
        labels = issue.labels
        labels = [label.name for label in labels]
            
        #collect labels and body
        df_dict['labels'].append(';'.join(labels))
        df_dict['body'].append(issue.body)
        df_dict['title'].append(issue.title)
        df_dict['state'].append(issue.state)
        
        #collect created times
        if issue.created_at:
            df_dict['created_time'].append(datetime.strftime(issue.created_at,
                                                            "%Y-%m-%d %H:%M:%S"))
            df_dict['created_date'].append(issue.created_at.date().isoformat())
        else:
            df_dict['created_time'].append("")
            df_dict['created_date'].append("")
        
        #collect updated times
        if issue.updated_at:
            df_dict['updated_time'].append(datetime.strftime(issue.updated_at,
                                                        "%Y-%m-%d %H:%M:%S"))
            df_dict['updated_date'].append(issue.updated_at.date().isoformat())
        else:
            df_dict['updated_time'].append("")
            df_dict['updated_date'].append("")
        
        #collect closed times
        if issue.closed_at:
            df_dict['closed_time'].append(datetime.strftime(issue.closed_at,
                                                    "%Y-%m-%d %H:%M:%S"))
            df_dict['closed_date'].append(issue.closed_at.date().isoformat())
        else:
            df_dict['closed_time'].append("")
            df_dict['closed_date'].append("")
            
    return df_dict,repo


def compute_stats_issues(repo_name:str,state='open',
                         months=2) -> tuple:
    
    """
    Inputs:
        repo_name: Repository name (format: organization_name/repository_name)
        state: 'open' or 'closed' (Default: 'open')
        months = Number of months windows (Default: 2)
        
    Returns a tuple of two tables:
        1. Table with average defect density and performance issue percentage
        2. Granular level information on all the issues generated in given
        window
    """
    
    #Initialize tempfile
    name = os.path.basename(repo_name)
    tempfile = "temp-{}.log".format(name)
    #check for cache of last completion date
    logdir = os.path.join(thisdir,'logs')
    ts = None
    if os.path.exists(os.path.join(logdir, tempfile)):
        with open(os.path.join(logdir, tempfile),"r") as f:
            for line in f.readlines():
                ts = line.strip()
        try:
            os.remove(os.path.join(logdir,tempfile))
        except:
            pass
    fh = logging.FileHandler(os.path.join(logdir, tempfile),
                             mode = 'w')
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    ts_feed = datetime.now().isoformat()
    logger.info(f"{ts_feed}")
    
    if ts:
        dfdict,repo = store_issue_attrs(repo_name, state,
                                        since=dateutil.parser.parse(ts))
    else:
        dfdict,repo = store_issue_attrs(repo_name, state,
                                   since=datetime.now() + relativedelta(months=-months))
        
    issues_df = pd.DataFrame(dfdict)
    if len(issues_df.columns) == len(dfdict.keys()):
        if issues_df.shape[0] == len(dfdict['issue_id']):
            del dfdict
    if issues_df.shape[0] == 0:
        return {},issues_df
    bug_maker = (issues_df['labels'].str.contains('bug',case=False) |
                   issues_df['labels'].str.contains('blocker',case=False) |
                   issues_df['labels'].str.contains('defect',case=False) |
                   issues_df['labels'].str.contains('fault',case=False) |
                   issues_df['labels'].str.contains('error',case=False) |
                   issues_df['labels'].str.contains('fix',case=False))
    
    perf_maker = (issues_df['labels'].str.contains('feature',case=False) |
                   issues_df['labels'].str.contains('performance',case=False) |
                   issues_df['labels'].str.contains('info',case=False) |
                   issues_df['labels'].str.contains('change',case=False))
    
    #compute Average defect density & performance issue percentage
    defect_density = issues_df[bug_maker].shape[0]/issues_df.shape[0]
    performance_issue_percentage = (issues_df[perf_maker].shape[0]/issues_df.shape[0]) * 100
    
    #Create another schema for results
    final = {}
    final['project_id'] = repo.id
    final['project'] = repo_name
    if ts:
        dt_from = dateutil.parser.parse(ts)
        final['from'] = datetime.strftime(dt_from,"%Y-%m-%d %H:%M:%S")
    else:
        temp = datetime.now() + relativedelta(months=-2)
        final['from'] = datetime.strftime(temp, "%Y-%m-%d %H:%M:%S")
    dt_to = dateutil.parser.parse(ts_feed)
    final['to'] = datetime.strftime(dt_to,"%Y-%m-%d %H:%M:%S")
    final['average_defect_density'] = defect_density
    final['perf_issue_percent'] = performance_issue_percentage
    
    return final,issues_df

def populate_tables(repo_name:str,state='open',
                         months=2):
    """

    Parameters
    ----------
    repo_name : str
        Repository name (format: organization_name/repository_name).
    state : TYPE, optional
        State of issues ('open'/'closed'). The default is 'open'.
    months : TYPE, optional
        Window of number of months. The default is 2.

    Returns
    -------
    TYPE
        exit status (0/fallback string: 'No issues created during observed window').

    """
    final,issues = compute_stats_issues(repo_name,state,months)
    conn = create_connection(os.path.join(thisdir,"sqlite.db"))
    if (len(final) == 0) and (issues.shape[0] == 0):
        return "No issues created during observed window"
    final_df = pd.DataFrame(final,index=[0])
    final_df.to_sql("projects_issue_stats",conn,if_exists='append',
                 index=False)
    issues.to_sql("issues_detailed",conn,if_exists='append',
                  index=False)
    conn.commit()
    conn.close()
    return 0