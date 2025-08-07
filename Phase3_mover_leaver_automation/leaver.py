import boto3
import csv
from datetime import datetime

# 🧩 Step 1: Initialize AWS IAM client
iam = boto3.client('iam')

# 🧩 Step 2: Check if user exists
def user_exists(username):
    try:
        iam.get_user(UserName=username)
        return True
    except iam.exceptions.NoSuchEntityException:
        return False

# 🧩 Step 3: Detach all managed policies
def detach_all_policies(username):
    policies = iam.list_attached_user_policies(UserName=username)['AttachedPolicies']
    for policy in policies:
        iam.detach_user_policy(UserName=username, PolicyArn=policy['PolicyArn'])

# 🧩 Step 4: Remove user from all groups
def remove_from_all_groups(username):
    groups = iam.list_groups_for_user(UserName=username)['Groups']
    for group in groups:
        iam.remove_user_from_group(UserName=username, GroupName=group['GroupName'])

# 🧩 Step 5: Main handler to process LEAVER (offboarding)
def handle_leaver(username):
    print(f"\n🧹 Processing LEAVER: {username}")

    if not user_exists(username):
        print(f"[!] User {username} does not exist or already deleted.")
        return

    # Step 5.1: Detach policies and remove from groups
    detach_all_policies(username)
    remove_from_all_groups(username)

    # Step 5.2: Disable console access
    try:
        iam.delete_login_profile(UserName=username)
        print("[✓] Console access disabled")
    except iam.exceptions.NoSuchEntityException:
        print("[-] No console access to disable")

    # Step 5.3: Delete all access keys
    access_keys = iam.list_access_keys(UserName=username)['AccessKeyMetadata']
    for key in access_keys:
        iam.delete_access_key(UserName=username, AccessKeyId=key['AccessKeyId'])
        print(f"[✓] Deleted access key: {key['AccessKeyId']}")

    # Step 5.4: Delete the IAM user
    try:
        iam.delete_user(UserName=username)
        print(f"[✓] Deleted IAM user: {username}")
    except Exception as e:
        print(f"[!] Failed to delete user: {e}")

# 🧩 Step 6: Read and process each LEAVER from CSV
def main():
    try:
        with open('users_leaver.csv', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row.get('username', '').strip()
                if username:
                    handle_leaver(username)
                else:
                    print(f"[!] Skipping row with missing username: {row}")
    except FileNotFoundError:
        print("[ERROR] users_leaver.csv not found!")

# 🧩 Step 7: Run the script
if __name__ == "__main__":
    main()
