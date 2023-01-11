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
    with open('/Users/faza/Downloads/testnet-state-261222.json') as f:
        data = json.load(f)

    # Insert user
    for user in data['app_state']['gitopia']['userList']:
        cur.execute("INSERT INTO user (block_range, id, userid, creator, name, username, createdat, updatedat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                    (Range(empty=True), user['userid'], user['userid'], user['creator'], user['name'], user['username'], user['createdat'], user['updatedat']))

    # Insert dao
    for dao in data['app_state']['gitopia']['daoList']:
        cur.execute("INSERT INTO dao (block_range, id, creator, address, name, createdat, updatedat) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (Range(empty=True), dao['id'], dao['creator'], dao['address'], dao['name'], dao['createdat'], dao['updatedat']))

    # Insert member
    for member in data['app_state']['gitopia']['memberList']:
        cur.execute("INSERT INTO member (block_range, id, address, daoaddress, role) VALUES (%s, %s, %s, %s, %s)", 
                    (Range(empty=True), '{}-{}'.format(member['id'], member['address']), member['address'], member['daoaddress'], member['role']))

    # Insert issue
    for issue in data['app_state']['gitopia']['issueList']:
        cur.execute("INSERT INTO issue (block_range, id, creator, iid, title, state, description, comments, commentscount, pullrequests, repositoryid, labels, weight, assignees, bounties, createdat, updatedat, closedat, closedby) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (Range(empty=True), issue['id'], issue['creator'], issue['iid'], issue['title'], issue['state'], issue['description'], issue['comments'], issue['commentscount'], issue['pullrequests'], issue['repositoryid'], issue['labels'], issue['weight'], issue['assignees'], issue['bounties'], issue['createdat'], issue['updatedat'], issue['closedat'], issue['closedby']))

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
