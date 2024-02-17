import time
import shutil
from pathlib import Path
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor


def proceed_file(filename: Path, root_folder: Path):
    file_extension = filename.suffix[1:]
    file_extension = file_extension.lower()
    file_name = filename.stem            # назва файлу
    create_folders = root_folder.joinpath(file_extension)
    create_folders.mkdir(exist_ok=True)
    target_file = create_folders.joinpath(file_name + "." + file_extension)
    shutil.move(filename, target_file)


def delete_empty_folder(path):  # видаляємо папки якщо вона пуста
    try:
        if path.is_dir() and len(list(path.iterdir())) == 0:
            path.rmdir()
    except:
        pass


def proceed_folder(path, root_folder):  # функція яка обробляє файли
    for el in path.iterdir():  # переебираємо вкладенні єлементи у папку
        if el.is_dir():        # якщо це папка ми знову пеербираємо папку
            proceed_folder(el, root_folder)
        else:
            proceed_file(el, root_folder)
    else:
        delete_empty_folder(path)


def proceed_folder1(path, root_folder):  # функція яка обробляє файли
    for el in path.iterdir(): # переебираємо вкладенні єлементи у папку
        if el.is_dir():       # якщо це папка ми знову пеербираємо папку
            with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
                executor.submit(proceed_folder1, el, root_folder)
        else:
            with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
                executor.submit(proceed_file, el, root_folder)
    else:
        delete_empty_folder(path)


def main(folder_path):
    if folder_path.exists() and folder_path.is_dir():
        proceed_folder(folder_path, folder_path)  # обробляємо корневий каталог
    else:
        print("Папка не існує або не є папкою.")


def main2(folder_path):
    if folder_path.exists() and folder_path.is_dir():
        proceed_folder1(folder_path, folder_path) 
    else:
        print("Папка не існує або не є папкою.")


# проверяем правильно ли кол во аргументов ввели в консоль
if __name__ == "__main__":
    folder1 = Path("/Users/polly/Desktop/хлам")
    folder2 = Path("/Users/polly/Desktop/хлам 2")
    star_time = time.time()
    main(folder1)
    end_time = time.time()

    star_time2 = time.time()
    main2(folder2)
    end_time2 = time.time()

    print("main", end_time - star_time)
    print("main2", end_time2 - star_time2)
