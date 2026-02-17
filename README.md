# Small Case Portfolio Viewer

A **web-based portfolio analyzer** for small-case or stock holding review Excel files.  
Upload your Excel, visualize stock holding durations, see entry-exit history, and analyze holding patterns easily.

---

## 🚀 Features

- Upload portfolio Excel files (single or multiple sheets supported).  
- Automatically detect the sheet containing required columns:  
  `Date Range`, `Constituents`, `Weightage`.  
- Display **dashboard metrics**:
  - Total stocks  
  - Total holding periods  
  - Average holding duration (weeks)  
  - Longest held stock  
- Visualize **holding duration per stock** with interactive charts.  
- View **all entry-exit records** in a table with **search functionality**.  
- Multiple Excel files supported with automatic timestamp to avoid overwriting.  
- Clean, responsive UI using **Bootstrap 5**.  
- Session-aware navigation showing the currently selected file.  
- Error handling for unsupported Excel files.  

---

## 📸 Screenshots

<img width="1756" height="892" alt="image" src="https://github.com/user-attachments/assets/f4b20859-2daf-4ee9-b3c4-faf6043a6a41" />
*Upload your portfolio Excel file.*
<img width="1739" height="893" alt="image" src="https://github.com/user-attachments/assets/02478974-f285-46e0-b219-8d974d272344" />

<img width="1768" height="705" alt="image" src="https://github.com/user-attachments/assets/b9e02adc-3ca5-4070-8844-e1905459d9f2" />



<img width="879" height="877" alt="image" src="https://github.com/user-attachments/assets/6d58b372-30a9-4766-b28b-a0fb630f13ad" />

*View summary metrics, charts, and entry-exit table.*

<img width="1241" height="889" alt="image" src="https://github.com/user-attachments/assets/1e041027-10ff-4b08-89a3-69344a762e32" />
*Visual timeline of stock holdings.*

---

## 🛠 Installation

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/small-case-portfolio-viewer.git
cd small-case-portfolio-viewer


2. **Create a virtual environment**

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
