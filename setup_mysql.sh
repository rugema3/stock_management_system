#!/bin/bash
# Bash script to create a MySQL database for the Stock Management System

# Load environment variables from a file
source passwords.env

# Create the database and user
mysql -u root -p <<MYSQL_SCRIPT
CREATE DATABASE IF NOT EXISTS $db_name;
CREATE USER IF NOT EXISTS '$db_user'@'$db_host' IDENTIFIED BY '$db_password';
GRANT ALL PRIVILEGES ON $db_name.* TO '$db_user'@'$db_host';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

# Output completion message
echo "MySQL database setup complete."
