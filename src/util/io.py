import json
import os


def init(plotsFolder: str, dataFilePath: str):
    if not os.path.exists(plotsFolder):
        os.makedirs(plotsFolder)

    if not os.path.exists(dataFilePath):
        dataDir, fileName = os.path.split(dataFilePath)
        os.makedirs(dataDir, exist_ok=True)

        with open(dataFilePath, mode='w') as f:
            json.dump({}, f, indent=3)


def saveData(data: dict, dataFilePath: str, indent=3, sortKeys=False) -> str:
    with open(dataFilePath, mode='r') as f:
        d: dict = json.load(f)

    saveId = int(max(d.keys())) + 1 if len(d.keys()) else 0
    d[saveId] = data

    with open(dataFilePath, mode='w') as f:
        json.dump(d, f, indent=indent, sort_keys=sortKeys)

    return str(saveId)




