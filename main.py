import google_drive


def main():
    search_list = google_drive.names_generated("16.11.22", "20.11.22", 'Приходы')
    folders_list = google_drive.find_folders_ids_and_mkdir('1n6R50IOR3eTFcIDVbZ-jBBs-HXLYC2yt', search_list, 'C:\Приходы')
    for key in folders_list:
        item = folders_list.get(key)
        files_to_download = google_drive.get_files_dic(item)
        folder_name = key
        for key in files_to_download:
            file_id = files_to_download.get(key)
            google_drive.file_download(file_id, key, folder_name)





if __name__ == '__main__':
    main()
