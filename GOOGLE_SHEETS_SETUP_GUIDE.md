# Google Sheets Database Setup Guide

## 🚀 How to Connect Your Lead Scraper to Google Sheets

### 📋 Prerequisites
1. Google Cloud Project with Google Sheets API enabled
2. Google Sheets Service Account credentials
3. Your Google Sheet created and shared with the service account

### 🔧 Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Google Sheets API
   - Google Drive API

### 🔑 Step 2: Create Service Account

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **Create Service Account**
3. Give it a name (e.g., "lead-scraper-service")
4. Click **Create and Continue**
5. Skip roles for now, click **Done**
6. Find your service account and click the three dots → **Manage keys**
7. Click **Add Key** → **Create new key**
8. Choose **JSON** format
9. Download the JSON file and rename it to `service-account.json`

### 📊 Step 3: Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it something like "Lead Scraper Users"
4. Share the sheet with your service account email:
   - Click **Share** button
   - Paste the service account email (from the JSON file)
   - Give it **Editor** permissions

### ⚙️ Step 4: Configure Streamlit App

#### Option A: Using .streamlit/secrets.toml (Recommended)

1. Create a folder named `.streamlit` in your project root
2. Create a file named `secrets.toml` inside `.streamlit`
3. Add the following content:

```toml
[connections.gsheets]
spreadsheet = "YOUR_GOOGLE_SHEET_ID"  # Get this from the sheet URL
```

#### Option B: Using Environment Variables

1. Set the following environment variables:
   ```
   GOOGLE_SHEETS_SPREADSHEET_ID=YOUR_GOOGLE_SHEET_ID
   GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
   ```

### 🔍 How to Find Your Google Sheet ID

1. Open your Google Sheet
2. Look at the URL: `https://docs.google.com/spreadsheets/d/`**`SHEET_ID`**`/edit`
3. Copy the part after `/d/` and before `/edit`

### 🚀 Step 5: Install Required Packages

Run these commands in your terminal:

```bash
pip install streamlit-gsheets
pip install gspread
pip install google-auth-oauthlib
pip install google-auth-httplib2
```

### 🧪 Step 6: Test Connection

1. Run your Streamlit app:
   ```bash
   streamlit run streamlit_ui.py
   ```

2. Login as admin (username: `admin`, password: `admin`)

3. Go to Admin Panel → Check the storage type at the top

### ✅ Expected Results

If successful, you should see:
- ✅ **Storage Mode: Google Sheets (Persistent)**
- Google Sheets backup options available in Admin Panel
- User data automatically saved to Google Sheets

### 🔧 Troubleshooting

#### Issue: "Google Sheets not connected"
- Check if `streamlit-gsheets` is installed
- Verify your secrets.toml file is in the right location
- Make sure the Google Sheet ID is correct

#### Issue: "Permission denied"
- Ensure the service account email has Editor access to the sheet
- Check if the Google Sheets API is enabled in your Google Cloud project

#### Issue: "No data found in Google Sheets"
- The sheet might be empty initially - this is normal
- The app will create the initial admin user automatically

### 📱 Alternative: Manual Setup

If automatic setup doesn't work, you can manually add the connection code to your app:

```python
import gspread
from google.oauth2.service_account import Credentials

# Add this to your DBHandler.__init__ method
def connect_gsheets_manual():
    try:
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_file(
            'service-account.json', scopes=scopes
        )
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key("YOUR_SHEET_ID")
        return spreadsheet
    except Exception as e:
        print(f"Manual Google Sheets connection failed: {e}")
        return None
```

### 🎯 Quick Test

To test if Google Sheets is working, add this to your admin panel:

```python
if st.button("Test Google Sheets Connection"):
    try:
        if db.use_gsheets:
            df = db.conn.read(ttl=0)
            st.success(f"✅ Connected! Found {len(df)} users in Google Sheets")
            st.dataframe(df)
        else:
            st.error("❌ Google Sheets not connected")
    except Exception as e:
        st.error(f"❌ Connection error: {e}")
```

### 📞 Need Help?

If you're still having trouble:
1. Check the Streamlit logs for error messages
2. Verify your Google Cloud project settings
3. Ensure the service account has proper permissions
4. Make sure the sheet URL is accessible

---

**🎉 Once connected, your user data will be automatically backed up to Google Sheets and persist across app restarts!**
