import os
import time
import shutil
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor


images =  ['.jpeg', '.png', '.jpg', '.svg']
video = ['.avi', '.mp4', '.mov', '.mkv']
document = ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx']
audio = ['.mp3', '.ogg', '.wav', '.amr']
archive = ['.zip', '.gz', '.tar']


def remove_empty_folders(folder_path, exclude):
    for (root, dirs, files) in os.walk(folder_path, topdown=False):
        # если эта путь папки совпадает с путями папок которые мы создали игнорируем
        if any(exclude_f in root for exclude_f in exclude):
            continue
        # удаляем пустые и игнорируем исходную папку
        else:
            if not files and root != folder_path:
                os.rmdir(root)


def sort_files(folder_path):
    # Перевірка, чи існує задана папка
    if not os.path.exists(folder_path):
        print(f"Папка {folder_path} не існує.")
        return

    # прописать путь к новым папкам в переменных
    image_folder = os.path.join(folder_path, 'images')
    video_folder = os.path.join(folder_path, 'videos')
    document_folder = os.path.join(folder_path, 'documents')
    audio_folder = os.path.join(folder_path, 'audio')
    archives_folder = os.path.join(folder_path, 'archives')
    other_folder = os.path.join(folder_path, 'other')

    # перебираем пути, если нет нужной папки она создаётся
    for folder in [image_folder, video_folder, document_folder, audio_folder, archives_folder, other_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    exclude = [image_folder, video_folder, document_folder, audio_folder, archives_folder, other_folder]
    for (root, dirs, files) in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            # определяем суффикс файла деля его по точке
            _, file_extension = os.path.splitext(filename)
            file_extension = file_extension.lower()
                # сортируем по окончаниям в созданные папки
            if file_extension in images:
                shutil.move(file_path, os.path.join(image_folder, filename))

            elif file_extension in video:
                shutil.move(file_path, os.path.join(video_folder, filename))

            elif file_extension in document:
                shutil.move(file_path, os.path.join(document_folder, filename))

            elif file_extension in audio:
                shutil.move(file_path, os.path.join(audio_folder, filename))

            elif file_extension in archive:
                # архив распаковать в новую папку по названию архива
                # прописываем полный адрес куда распаковать(адрес папки, название архива(файла) без расширения)
                archive_folder = os.path.join(archives_folder, os.path.splitext(filename)[0])
                try:
                    shutil.unpack_archive(file_path, archive_folder)
                except shutil.ReadError:
                    shutil.move(file_path, os.path.join(archives_folder, filename))

            else:
                shutil.move(file_path, os.path.join(other_folder, filename))
        remove_empty_folders(folder_path, exclude)


def main(folder_to_sort):
    sort_files(folder_to_sort)


def main2(folder_to_sort):
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        executor.submit(sort_files, folder_to_sort)


# проверяем правильно ли кол во аргументов ввели в консоль
if __name__ == "__main__":
    folder1 = "/Users/polly/Desktop/хлам"
    folder2 = "/Users/polly/Desktop/хлам 2"
    star_time = time.time()
    main(folder1)
    end_time = time.time()

    star_time2 = time.time()
    main2(folder2)
    end_time2 = time.time()

    print("main", end_time - star_time)
    print("main2", end_time2 - star_time2)


# python clean.py /user/Desktop/Мотлох
