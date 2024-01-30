import os
import schedule
import time
from zipfile import ZipFile
from datetime import datetime

def zip_directory(directory_path, zip_file_path):
    try:
        with ZipFile(zip_file_path, 'w') as zipf:
            for foldername, subfolders, filenames in os.walk(directory_path):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, directory_path)
                    zipf.write(file_path, arcname)
                for subfolder in subfolders:
                    subfolder_path = os.path.join(foldername, subfolder)
                    arcname = os.path.relpath(subfolder_path, directory_path)
                    zipf.write(subfolder_path, arcname)
        print(f'成功创建压缩文件: {zip_file_path}')
    except Exception as e:
        print(f'创建压缩文件时发生错误: {e}')


def backup_job(source_directory, backup_directory):
    if not os.path.exists(source_directory):
        print(f'错误: 目录 "{source_directory}" 不存在')
        return

    current_datetime = datetime.now()
    timestamp = current_datetime.strftime("%Y%m%d-%H%M%S")
    zip_file_name = f"backup_{timestamp}.zip"
    zip_file_path = os.path.join(backup_directory, zip_file_name)

    zip_directory(source_directory, zip_file_path)

def schedule_backup(source_directory, backup_directory, interval_minutes):
    # 初始备份
    backup_job(source_directory, backup_directory)

    # 设置定时任务
    schedule.every(interval_minutes).minutes.do(backup_job, source_directory, backup_directory)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # 输入你的目录路径、备份目录路径和备份间隔时间（分钟）
    source_directory = input("请输入要打包的目录路径 (例如: C:\\Program Files): ")
    backup_directory = input("请输入备份文件夹路径 (例如: C:\\Program Files\\backup): ")
    interval_minutes = int(input("请输入备份的间隔时间（分钟）: "))

    # 启动定时备份
    schedule_backup(source_directory, backup_directory, interval_minutes)
