#!/usr/bin/env python
"""
Script to create the default admin user for the blog application.
Run this script after creating the database and running migrations.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogsite.settings')
django.setup()

from django.contrib.auth import get_user_model
from blog.models import CustomUser

def create_default_admin():
    """Create the default admin user if it doesn't exist"""
    User = get_user_model()
    
    # Check if the default admin user already exists
    if not CustomUser.objects.filter(username='Admin').exists():
        try:
            # Create the user
            user = CustomUser.objects.create_user(
                username='Admin',
                email='admin@blogpython.com',
                password='Admin123',
                is_admin=True
            )
            print(f"✅ Default admin user created successfully!")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Password: Admin123 (default)")
            return True
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            return False
    else:
        print("✅ Default admin user already exists.")
        return True

if __name__ == '__main__':
    print("🚀 Creating default admin user...")
    success = create_default_admin()
    if success:
        print("\n🎉 Setup complete! You can now log in with:")
        print("   Username: Admin")
        print("   Password: Admin123")
    else:
        print("\n💥 Setup failed!")
        sys.exit(1)