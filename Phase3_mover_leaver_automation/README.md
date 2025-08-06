## 🔁 Phase 3: Mover & Leaver Lifecycle Automation

---

### 🎯 Objective

Automate the **Mover** and **Leaver** phases of the IAM lifecycle using Python and Boto3.  
This phase simulates internal role changes (movers) and secure offboarding (leavers) — critical to access governance and risk reduction.

---

### 📁 Files Used

- `mover_leaver.csv`  
  Contains user action data for movers and leavers, including username, action type (`mover` or `leaver`), old group, new group, and policy updates.

- `process_mover_leaver.py`  
  Python script to:
  - Update user roles by changing group and policy assignments
  - Revoke access for leavers (disable sign-in, deactivate keys, remove from groups)
  - (Optional) Delete user for complete offboarding

---

### ✅ Use Cases Covered

#### 🔁 MOVER  
Simulate role transitions, e.g., Developer → Security Analyst  
✔ Remove from old IAM group  
✔ Add to new IAM group  
✔ Update attached IAM policies (if needed)  
✔ Rotate credentials (optional)

#### 🧹 LEAVER  
Simulate offboarding securely  
✔ Deactivate console access  
✔ Disable or delete access keys  
✔ Remove from IAM groups  
✔ Delete user (optional, based on org policy)

---

### 🚀 How to Run (Step-by-Step)

1. ✅ **Prepare the Data**  
   Ensure your `mover_leaver.csv` is accurate and saved in the Phase 3 folder.

2. ▶️ **Run the Automation Script**

   ```bash
   python process_mover_leaver.py
3. 📋 Actions Performed
  - Movers: Group and policy reassignment
  - Leavers: Access revocation and optional deletion
  - Logs success/failure per user
4. 🖥 Verify in AWS Console
  - IAM > Users: Check group memberships and access keys
  - Confirm expected changes match the CSV file actions
