import boto3
import csv

# 0. Initialize AWS clients
iam = boto3.client('iam')
sts = boto3.client('sts')
account_id = sts.get_caller_identity()['Account']

# 1. Check if the user already exists
def user_exists(username):
    try:
        iam.get_user(UserName=username)
        return True
    except iam.exceptions.NoSuchEntityException:
        return False

# 2. Detach all user-attached policies
def detach_all_policies(username):
    policies = iam.list_attached_user_policies(UserName=username)['AttachedPolicies']
    for policy in policies:
        iam.detach_user_policy(UserName=username, PolicyArn=policy['PolicyArn'])

# 3. Remove user from all IAM groups
def remove_from_all_groups(username):
    groups = iam.list_groups_for_user(UserName=username)['Groups']
    for group in groups:
        iam.remove_user_from_group(UserName=username, GroupName=group['GroupName'])

# 4. Handle MOVER logic
def handle_mover(username, group, policy_name, department):
    # 4.1 Create user if they don't exist
    if not user_exists(username):
        iam.create_user(UserName=username)
        print(f"[+] Created user: {username}")

    # 4.2 Remove from old groups and add to new one
    remove_from_all_groups(username)
    try:
        iam.add_user_to_group(UserName=username, GroupName=group)
    except iam.exceptions.NoSuchEntityException:
        iam.create_group(GroupName=group)
        iam.add_user_to_group(UserName=username, GroupName=group)
        print(f"[+] Group created and added: {group}")

    # 4.3 Detach old policies and attach new one
    detach_all_policies(username)
    policy_arn = f"arn:aws:iam::{account_id}:policy/{policy_name}"
    iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)

    # 4.4 Tag the user
    iam.tag_user(UserName=username, Tags=[
        {"Key": "Department", "Value": department}
    ])

    print(f"[✓] Updated user {username} with new group/policy for MOVER\n")

# 5. Handle LEAVER logic
def handle_leaver(username):
    if user_exists(username):
        detach_all_policies(username)
        remove_from_all_groups(username)

        # 5.1 Disable console access
        try:
            iam.delete_login_profile(UserName=username)
        except iam.exceptions.NoSuchEntityException:
            pass  # If no console access, skip

        # 5.2 Delete user
        iam.delete_user(UserName=username)
        print(f"[✓] Deprovisioned and deleted LEAVER: {username}\n")
    else:
        print(f"[!] User {username} already deleted.\n")

# 6. Main loop - Read from lifecycle CSV
def main():
    with open('users_lifecycle.csv', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data = {k.strip(): v.strip() for k, v in row.items()}
            username = data['username']
            status = data['status'].lower()

            if status == "active":
                handle_mover(
                    username=username,
                    group=data['group'],
                    policy_name=data['policy'],
                    department=data['department']
                )
            elif status == "inactive":
                handle_leaver(username)

# 7. Entry point
if __name__ == "__main__":
    main()
