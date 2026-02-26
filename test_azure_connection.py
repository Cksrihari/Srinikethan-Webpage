#!/usr/bin/env python3
"""
Test Azure SQL Database Connection

This script tests the connection to Azure SQL Database without making changes.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'srinikethan_website.settings')
django.setup()

def test_connection():
    """Test Azure SQL Database connection"""
    print("🔍 Testing Azure SQL Database connection...")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Successfully connected to Azure SQL Database!")
                print(f"📊 Connection test result: {result[0]}")
                return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure Microsoft ODBC Driver 17 for SQL Server is installed")
        print("   macOS: brew install msodbcsql17")
        print("2. Check your Azure SQL Database firewall settings")
        print("3. Verify database credentials in .env file")
        print("4. Ensure the 'webpage' database exists on the server")
        return False

if __name__ == "__main__":
    test_connection()