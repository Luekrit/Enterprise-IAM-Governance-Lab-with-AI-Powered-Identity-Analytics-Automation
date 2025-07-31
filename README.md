# 🛡️ Enterprise IAM Governance Lab with AI-Powered Identity Analytics & Automation

This project simulates enterprise-grade **Identity and Access Management (IAM)** governance across multiple phases, combining **lifecycle orchestration**, **access automation**, and **AI-based anomaly detection**. Designed for cloud and security engineering portfolios, it replicates what happens in a real-world Joiner-Mover-Leaver (JML) environment.

---

## 🚀 Project Overview

This lab demonstrates:

- ✅ IAM lifecycle automation across Joiner, Mover, and Leaver phases
- 🔐 Role-based access enforcement with custom IAM policies
- 📊 Governance via metadata (tags), RBAC, and structured inputs
- 🧠 (Coming Soon) AI-powered anomaly detection and role recommendation

Built using:
- **AWS IAM**
- **Python 3.11+**
- **Boto3**
- **CSV-driven lifecycle simulation**
- *(Upcoming: AI/ML for access pattern analytics)*

---

## 📂 Phases

### **Phase 1 – Manual Joiner Setup**
- Provision IAM users manually via AWS Console
- Apply tags (`Department=HR`) and assign custom policies
- Use this to document and understand the IAM flow before automation

### **Phase 2 – Joiner Automation with Python & Boto3**
- Automatically provisions IAM users from `users.csv`
- Creates missing groups, attaches policies, applies tags
- CLI-based onboarding simulation for Joiner lifecycle

### **Phase 3 – Mover & Leaver Lifecycle Automation**
- Reads `users_lifecycle.csv` with user statuses
- Reassigns group and policy if user changes role (Mover)
- Detaches and deletes users marked as `inactive` (Leaver)

### **Phase 4 – AI-Driven Anomaly Detection (Coming Soon)**
- Analyzes CloudTrail and IAM activity
- Detects abnormal behavior like:
  - Unexpected policy escalation
  - After-hours access
  - Location/device anomalies
- Uses Python (Pandas, Scikit-learn) or integrates with AWS ML tools

---

## 📥 Sample CSV Files

### `users.csv` (Phase 2 – Joiner)
```csv
username,group,policy,department
alice.hr,HR-ReadOnly,s3-readonly,HR
bob.dev,Developers-AWS,ec2-admin,Development
carol.sec,Security-AWS,security-audit,Security


