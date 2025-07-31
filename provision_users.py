import boto3
import csv

# Initialize AWS clients
iam = boto3.client('iam')
sts = boto3.client('sts')

# Get your AWS account ID (for customer-managed policy ARNs)
account_id = sts.get_caller_identity()['Account']

def create_user(username, group, policy_name, department):
    try:
        # 1. Create the user
        iam.create_user(UserName=username)
        print(f"[+] Created user: {username}")

        # 2. Add user to IAM group
        try:
            iam.add_user_to_group(UserName=username, GroupName=group)
        except iam.exceptions.NoSuchEntityException:
            iam.create_group(GroupName=group)
            iam.add_user_to_group(UserName=username, GroupName=group)
            print(f"[+] Group created and added: {group}")

        # 3. Construct full ARN for customer-managed policy
        policy_arn = f"arn:aws:iam::{account_id}:policy/{policy_name}"
        
        # 4. Attach the policy to the user
        iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)

        # 5. Tag the user
        iam.tag_user(UserName=username, Tags=[
            {"Key": "Department", "Value": department}
        ])

        print(f"[✓] {username} provisioned with group, policy, and tags.\n")

    except Exception as e:
        print(f"[!] Failed to create user {username}: {e}\n")

def main():
    with open('users.csv', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Clean headers/values to avoid Excel whitespace or BOM issues
            cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
            create_user(
                username=cleaned_row['username'],
                group=cleaned_row['group'],
                policy_name=cleaned_row['policy'],
                department=cleaned_row['department']
            )

if __name__ == "__main__":
    main()
