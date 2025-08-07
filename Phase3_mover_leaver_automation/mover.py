import boto3
import csv
from datetime import datetime

# 🧩 Step 1: Initialize AWS IAM and STS clients
iam = boto3.client('iam')
sts = boto3.client('sts')
account_id = sts.get_caller_identity()['Account']

# 🧩 Step 2: Check if IAM user exists
def user_exists(username):
    try:
        iam.get_user(UserName=username)
        return True
    except iam.exceptions.NoSuchEntityException:
        return False

# 🧩 Step 3: Detach all managed policies from user
def detach_all_policies(username):
    policies = iam.list_attached_user_policies(UserName=username)['AttachedPolicies']
    for policy in policies:
        iam.detach_user_policy(UserName=username, PolicyArn=policy['PolicyArn'])

# 🧩 Step 4: Remove user from all current IAM groups
def remove_from_all_groups(username):
    groups = iam.list_groups_for_user(UserName=username)['Groups']
    for group in groups:
        iam.remove_user_from_group(UserName=username, GroupName=group['GroupName'])

# 🧩 Step 5: Main handler to process a MOVER (role change)
def handle_mover(username, new_group, new_policy, department):
    print(f"\n🔁 Processing MOVER: {username}")
    
    # Step 5.1: Create user if not already created
    if not user_exists(username):
        iam.create_user(UserName=username)
        print(f"[+] Created user: {username}")

    # Step 5.2: Remove from old groups
    remove_from_all_groups(username)

    # Step 5.3: Add to new group (create group if not found)
    try:
        iam.add_user_to_group(UserName=username, GroupName=new_group)
    except iam.exceptions.NoSuchEntityException:
        iam.create_group(GroupName=new_group)
        iam.add_user_to_group(UserName=username, GroupName=new_group)
        print(f"[+] Group created and user added: {new_group}")

    # Step 5.4: Detach all policies and attach new one
    detach_all_policies(username)
    policy_arn = f"arn:aws:iam::{account_id}:policy/{new_policy}"
    iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)

    # Step 5.5: Tag user with department and timestamp
    iam.tag_user(UserName=username, Tags=[
        {"Key": "Department", "Value": department},
        {"Key": "LastUpdated", "Value": datetime.utcnow().isoformat()}
    ])

    print(f"[✓] {username} moved to {new_group} with new policy\n")

# 🧩 Step 6: Read and process each user from CSV
def main():
    try:
        with open('users_mover.csv', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if all(row.get(k) for k in ['username', 'group', 'policy', 'department']):
                    handle_mover(
                        username=row['username'].strip(),
                        new_group=row['group'].strip(),
                        new_policy=row['policy'].strip(),
                        department=row['department'].strip()
                    )
                else:
                    print(f"[!] Skipping row due to missing fields: {row}")
    except FileNotFoundError:
        print("[ERROR] users_mover.csv not found!")

# 🧩 Step 7: Run the script
if __name__ == "__main__":
    main()
