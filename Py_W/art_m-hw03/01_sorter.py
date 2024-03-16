from pathlib import Path
from shutil import copyfile
from threading import Thread, Semaphore


def sort_folder(folder: Path, output: Path, condition: Semaphore):
    with condition:
        result = dict()
        for el in folder.iterdir():
            if el.is_file():
                ext = el.suffix.lower()
                if not ext:
                    continue
                ext_items = result.get(ext, [])
                ext_items.append(el)
                result[ext] = ext_items

        for ext, ext_items in result.items():
            dest_path = output.joinpath(ext[1:])
            dest_path.mkdir(exist_ok=True, parents=True)
            for el in ext_items:
                dest_file = dest_path.joinpath(el.name)
                try:
                    copyfile(el, dest_file)
                except OSError as e:
                    print(f"Error: {e}")


def get_folders(source_path: Path) -> list[Path]:
    folders = list()
    for elem in source_path.glob("*/**"):
        if elem.is_dir():
            folders.append(elem)
    return folders


def main(args_cli: dict = None):
    source = args_cli.get("source")
    output = args_cli.get("output", "sort_result")
    max_threads: int = args_cli.get("threads", 10)

    folders = get_folders(Path(source))
    output_path = Path(output)
    threads = []
    pool = Semaphore(max_threads)
    for num, folder in enumerate(folders):
        th = Thread(
            name=f"Th-{num}",
            target=sort_folder,
            args=(folder, output_path, pool),
        )
        th.start()
        threads.append(th)
    [thread.join() for thread in threads]
