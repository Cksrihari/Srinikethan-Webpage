# Azure SQL Database Setup Guide

## Current Status
✅ **Azure SQL Database**: Configured and ready
⚠️ **ODBC Driver Required**: Microsoft ODBC Driver 17 for SQL Server needed

## Azure SQL Database Details
- **Server**: srinikethan.database.windows.net
- **Database**: webpage
- **User**: adminuser
- **Password**: BlueDragon11

## Prerequisites

### Install ODBC Driver

**macOS:**
```bash
# Install Microsoft ODBC Driver 17 for SQL Server
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql17 mssql-tools
```

**Linux (Ubuntu/Debian):**
```bash
# Add Microsoft repository
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list

# Update package list
sudo apt-get update

# Install ODBC driver
sudo apt-get install msodbcsql17
```

## Local Development Setup

1. **Ensure ODBC driver is installed** (see above)

2. **Install Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables** (create `.env` file):
   ```
   DB_NAME=webpage
   DB_HOST=srinikethan.database.windows.net
   DB_USER=adminuser
   DB_PASSWORD=BlueDragon11
   DEBUG=True
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Start development server**:
   ```bash
   python manage.py runserver
   ```

## Production Deployment

### For Azure App Service:

1. **Configure Application Settings**:
   ```
   DB_NAME=webpage
   DB_HOST=srinikethan.database.windows.net
   DB_USER=adminuser
   DB_PASSWORD=BlueDragon11
   DEBUG=False
   PYTHONPATH=/home/site/wwwroot
   ```

2. **Deploy your application files**

3. **Run initial setup**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

## Admin Access
- **Local**: http://127.0.0.1:8000/admin/
- **Production**: https://your-app-name.azurewebsites.net/admin/

## Troubleshooting

### Connection Issues
- Verify Azure SQL server firewall allows your IP
- Check that the database 'webpage' exists
- Ensure credentials are correct
- Confirm ODBC driver is installed

### Driver Issues on macOS
If you encounter ODBC driver issues:
```bash
# Verify driver installation
odbcinst -j

# Check available drivers
odbcinst -q -d
```

The application is now configured to use Azure SQL Database exclusively!