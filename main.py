import psycopg2
from psycopg2.extras import Range
import json
from db_config import db_config

def main():
    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_config)

    # Create a cursor object
    cur = conn.cursor()

    # Load state from genesis
    with open('genesis.json') as f:
        data = json.load(f)

    # Insert user
    for user in data['app_state']['gitopia']['userList']:
        cur.execute("INSERT INTO sgd10.user (block_range, id, userid, creator, name, username, createdat, updatedat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                    (str(Range(empty=True)), user['id'], user['id'], user['creator'], user['name'], user['username'], user['createdAt'], user['updatedAt']))

    # Insert dao
    for dao in data['app_state']['gitopia']['daoList']:
        cur.execute("INSERT INTO sgd10.dao (block_range, id, creator, address, name, createdat, updatedat) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (str(Range(empty=True)), dao['id'], dao['creator'], dao['address'], dao['name'], dao['createdAt'], dao['updatedAt']))

    # Insert member
    for member in data['app_state']['gitopia']['memberList']:
        cur.execute("INSERT INTO sgd10.member (block_range, id, address, daoaddress, role) VALUES (%s, %s, %s, %s, %s)", 
                    (str(Range(empty=True)), '{}-{}'.format(member['id'], member['address']), member['address'], member['daoAddress'], member['role']))

    # Insert issue
    for issue in data['app_state']['gitopia']['issueList']:
        cur.execute("INSERT INTO sgd10.issue (block_range, id, creator, iid, title, state, description, comments, commentscount, pullrequests, repositoryid, labels, weight, assignees, bounties, createdat, updatedat, closedat, closedby) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (str(Range(empty=True)), issue['id'], issue['creator'], issue['iid'], issue['title'], issue['state'], issue['description'], issue['comments'], issue['commentsCount'], issue['pullRequests'], issue['repositoryId'], issue['labels'], issue['weight'], issue['assignees'], issue['bounties'], issue['createdAt'], issue['updatedAt'], issue['closedAt'], issue['closedBy']))

    # Insert repository
    for repository in data['app_state']['gitopia']['repositoryList']:
        cur.execute("INSERT INTO sgd10.repository (block_range, id, creator, name, owner, owner_type, description, createdat, updatedat, archived, license, defaultbranch, parent, fork, collaborators, allowforking, enablearweavebackup) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (str(Range(empty=True)), repository['id'], repository['creator'], repository['name'], repository['owner']['id'], repository['owner']['type'], repository['description'], repository['createdAt'], repository['updatedAt'], repository['archived'], repository['license'], repository['defaultBranch'], repository['parent'], repository['fork'], repository['collaborators'], repository['allowForking'], repository['enableArweaveBackup']))

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
