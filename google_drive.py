import os
import io

from desktop_files import make_directory
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime, timedelta
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

gauth = GoogleAuth()


# Функция возвращает список с сгенерированными именами файлов.
# Получает дату начала и конца периода в формате '01.01.01' и строку.
def names_generated(start_date, end_date, word):
    start = datetime.strptime(start_date, '%d.%m.%y')
    end = datetime.strptime(end_date, '%d.%m.%y')
    delta = end - start
    folders_names_list = []
    if delta.days <= 0:
        print('Нет диапзона')
    for i in range(delta.days + 1):
        date = start + timedelta(i)
        file_date = date.strftime("%m %d")
        file_name = f'{word}  {file_date}'
        folders_names_list.append(file_name)
    return folders_names_list


# Функция возвращает список со списками имен файлов или папок и их id в заданной папке google Drive
def get_files_names_and_ids(gauth, folder_id):
    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    files_names = []
    files_id = []
    for file in file_list:
        name = file['title']
        id = file['id']
        files_names.append(name)
        files_id.append(id)
    return [files_names, files_id]


# Возвращает словарь со всеми файлами в директории google drive, где ключ - название, значение - id.
# Получает объект GoogleAuth и id папки
def get_files_dic(folder_id):
    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    files_names = {}
    for file in file_list:
        title = file['title']
        id = file['id']
        files_names[f'{title}'] = f'{id}'
    return files_names


# Функция поиска совпадений названий из списков на диске в указанной папке.
# Получает id папки в которой искать, Список названий файлов.
# Возвращает словарь где ключ - название файла/папки, значение - id.
def find_matches(search_list, folder_id):
    founded_files = {}
    files_list = get_files_dic(folder_id)

    print(files_list)
    for item in search_list:
        for key in files_list:
            if item == key:
                name = key
                id = files_list.get(key)
                founded_files[f'{name}'] = f'{id}'
    return founded_files


# Функиця скачивания файлов с google drive. Получает id файлов и адрес к директории, в которую нужно скачать.
def file_download(file_id, file_name, path):
        request = service.files().export_media(fileId=file_id,
                                               mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        # done = False
        #
        # while not done:
        #     status, done = downloader.next_chunk()
        fh.seek(0)

        with open(os.path.join(f'{path}', f'{file_name}.xlsx'), 'wb') as f:
            f.write(fh.read())
            f.close()


# Функция поиска нужных папок в директории на google drive и создания папки на компьютере с таким же именем, в случае совпадения
# Получает объект GoogleAuth, id папки. список для поиска, путь, по которому нужно создать папку
def find_folders_ids_and_mkdir(id, names_list, path):
    finding_folders_id = {}
    folders_dic = get_files_dic(id)
    for name in names_list:
        for key in folders_dic:
            if key == name:
                item = folders_dic.get(key)
                finding_folders_id[f'{key}'] = f'{item}'
                make_directory(path, name)
    return finding_folders_id
