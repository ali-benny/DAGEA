import os


def getFolderFilesNames(path: str) -> list | str:
    filesNames = []
    for file in os.scandir(path):
        if file.name != ".gitkeep":
            filesNames.append(path + file.name)
    if len(filesNames) == 1:
        return filesNames[0]
    else:
        return filesNames


def deleteFolderFiles(path: str) -> None:
    for file in os.scandir(path):
        if file.name != ".gitkeep":
            os.remove(file)


def numberOfFolderFiles(path: str) -> int:
    fileCounter = 0
    for file in os.scandir(path):
        fileCounter += 1
    return fileCounter
