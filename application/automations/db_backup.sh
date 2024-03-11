#!/usr/bin/env bash
# A bash script that creates a dump and saves it in a backup

current_date=$(date +'%d-%m-%Y')  # Storing the current time
database_name="stock"  # Database to be saved
backup_path="/home/rugema3/stock_management_system/application/automations"  
backup_filename="$backup_path/$database_name-$current_date.sql"

mysqldump --defaults-file=/home/rugema3/.my.cnf "$database_name" > "$backup_filename"
tar -czvf "$backup_filename.tar.gz" "$backup_filename"
