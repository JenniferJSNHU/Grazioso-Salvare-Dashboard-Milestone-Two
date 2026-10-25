# CS 499 Milestone Two: Software Design and Engineering 
Grazioso Salvare Animal Shelter Dashboard

## Project Overview

This project enhances the original CS 340 animal shelter dashboard by converting it into a standalone Dash application. Improvements include reorganized application components, staff authentication, input validation, and a more accessible interface for managing and analyzing animal shelter records.

## Live Dashboard

The enhanced dashboard is deployed on Render and can be accessed without installing additional software.

**Dashboard URL:** To be added after deployment.

**Staff Login:**
- Username: staff
- Password: provided in submission zip README

The hosted dashboard connects to MongoDB Atlas and includes the animal shelter records needed to evaluate the application.

**Note:** The dashboard may take 1–2 minutes to load if the Render service has been inactive.

## Requirements

- Python 3
- MongoDB Community Server
- MongoDB Compass

## Local Setup

### 1. Install Dependencies

Open a terminal in the project folder and run:

```powershell
py -m pip install -r requirements.txt
```

### 2. Import the Database

The `data/animals.json` file contains 10,000 animal shelter records.

1. Start MongoDB Community Server.
2. Open MongoDB Compass.
3. Connect to `mongodb://localhost:27017/`.
4. Create a database named `aac`.
5. Create a collection named `animals`.
6. Open the collection and select **Add Data > Import JSON or CSV file**.
7. Select `data/animals.json` and import it as JSON.
8. Confirm that 10,000 records were imported.

### 3. Configure Staff Authentication

Copy `.env.example` and rename the copy `.env`.

Generate a password hash:

```powershell
py -c "from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass('Staff password: ')))"
```

Update `.env` with the following values:

```dotenv
GRAZIOSO_STAFF_USER=staff
GRAZIOSO_STAFF_PASSWORD_HASH=YOUR_GENERATED_HASH
MONGODB_URI=mongodb://localhost:27017/
```

Replace `YOUR_GENERATED_HASH` with the generated hash.

The password entered during hash generation will be used to sign in.

### 4. Run the Dashboard

Start the application:

```powershell
py app.py
```

Open http://127.0.0.1:8052 in a browser.

Sign in using the username `staff` and the password configured in Step 3.

## Software Design and Engineering Enhancements

- Converted the original Jupyter Notebook dashboard into a standalone Python application.
- Separated database operations, application logic, and interface components.
- Added server-side staff authentication using password hashing.
- Improved input validation and handling of animal records.
- Reorganized the dashboard interface for easier navigation.
- Added automated tests to verify application functionality.

## Security

Staff credentials and database configuration are stored in environment variables.

The `.env` file is excluded from version control.

## Project Data

The included animal shelter dataset supports the dashboard's records, filtering, rescue candidate analysis, and geographic mapping features.
