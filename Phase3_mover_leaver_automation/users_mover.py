import boto3
import csv
from datetime import datetime

iam = boto3.client('iam')
sts = boto3.client('sts')
account_id = sts.get_caller_identity()['Account']

def user_exists(username):
    try:
        iam.get_user(UserName=username)
        return True
    except iam.exceptions.NoSuchEntityException:
        return False

def detach_all_policies(username):
    policies = iam.list_attached_user_policies(UserName=username)['AttachedPolicies']
    for policy in policies:
        iam.detach_user_policy(UserName=username, PolicyArn=policy['PolicyArn'])

def remove_from_all_groups(username):
    groups = iam.list_groups_for_user(UserName=username)['Groups']
    for group in groups:
        iam.remove_user_from_group(UserName=username, GroupName=group['GroupName'])

def handle_mover(username, new_group, new_policy, department):
    print(f"\n🔁 Processing MOVER: {username}")
    
    if not user_exists(username):
        iam.create_user(UserName=username)
        print(f"[+] Created user: {username}")

    remove_from_all_groups(username)

    try:
        iam.add_user_to_group(UserName=username, GroupName=new_group)
    except iam.exceptions.NoSuchEntityException:
        iam.create_group(GroupName=new_group)
        iam.add_user_to_group(UserName=username, GroupName=new_group)
        print(f"[+] Group created and user added: {new_group}")

    detach_all_policies(username)

    policy_arn = f"arn:aws:iam::{account_id}:policy/{new_policy}"
    try:
        iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)
    except Exception as e:
        print(f"[!] Failed to attach policy: {e}")
        return

    iam.tag_user(UserName=username, Tags=[
        {"Key": "Department", "Value": department},
        {"Key": "LastUpdated", "Value": datetime.utcnow().isoformat()}
    ])

    print(f"[✓] {username} moved to {new_group} with new policy\n")

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

if __name__ == "__main__":
    main()
