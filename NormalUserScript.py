import time
from pydantic import FilePath
import requests
import json
import random
import pathlib


f = open("AccessTokens", 'r')
line = f.readline()

Auth = "Bearer "+line


def list_folder(token, path=""):

    list_folder_req = {"url": "https://api.dropboxapi.com/2/files/list_folder",
                       "data": {"path": path},
                       "headers": {
                           "Authorization": token,
                           "Content-Type": "application/json"
                       }
                       }
    r = requests.post(list_folder_req["url"], headers=list_folder_req["headers"],
                      data=json.dumps(list_folder_req["data"]))
    return r


def search(token, query="file"):

    list_folder_req = {"url": "https://api.dropboxapi.com/2/files/search_v2",
                       "data": {"query": query},
                       "headers": {
                           "Authorization": token,
                           "Content-Type": "application/json"
                       }
                       }
    r = requests.post(list_folder_req["url"], headers=list_folder_req["headers"],
                      data=json.dumps(list_folder_req["data"]))
    return r


def get_preview(filepath, token):
    print(filepath+"in preview")
    preview_req = {"url": "https://content.dropboxapi.com/2/files/get_preview",
                   "headers": {
                       "Authorization": token,
                       "Dropbox-API-Arg": "{\"path\":\""+filepath+"\"}"
                   }
                   }
    fileName = filepath + ".pdf"
    indx = fileName.rfind("/")
    fileName = fileName[indx+1:]
    r = requests.post(preview_req["url"], headers=preview_req["headers"])
    if (r.status_code == 200):
        PreviewFileHandle = open(fileName, "wb")
        PreviewFileHandle.write(r.content)
        PreviewFileHandle.close()
        return fileName
    else:
        return "Error occured"


def get_thumbnail(filepath, token):

    preview_req = {"url": "https://content.dropboxapi.com/2/files/get_thumbnail",
                   "headers": {
                       "Authorization": token,
                       "Dropbox-API-Arg": "{\"path\":\"/"+filepath+"\",\"format\":{\".tag\":\"png\"}}"
                   }
                   }
    fileName = filepath + ".png"
    indx = fileName.rfind("/")
    fileName = fileName[indx+1:]
    r = requests.post(preview_req["url"], headers=preview_req["headers"])
    if (r.status_code == 200):
        PreviewFileHandle = open(fileName, "wb+")
        PreviewFileHandle.write(r.content)
        PreviewFileHandle.close()
        return fileName
    else:
        print(r.status_code)
        return "Error occured"


def download(filepath, token):
    download_req = {"url": "https://content.dropboxapi.com/2/files/download",
                    "headers": {
                        "Authorization": token,
                        "Dropbox-API-Arg": "{\"path\":\""+filepath+"\"}"
                    }
                    }
    fileName = filepath
    indx = fileName.rfind("/")
    fileName = fileName[indx+1:]
    r = requests.post(download_req["url"], headers=download_req["headers"])
    if (r.status_code == 200):
        DownloadFileHandle = open(fileName, "wb+")
        DownloadFileHandle.write(r.content)
        DownloadFileHandle.close()
        return fileName
    else:
        print(r.text)
        print(r.status_code)
        return "Error occured"


def get_folder_path():
    r = list_folder(Auth)
    response = json.loads(r.text)
    folders = []
    for entry in response["entries"]:
        if(entry[".tag"] == 'folder'):
            folders.append(entry)
    size = len(folders)
    i = random.randint(0, size-1)
    return folders[i]["path_lower"]


def copy(token, from_path, to_path):
    copy_req = {
        "url": "https://api.dropboxapi.com/2/files/copy_v2",
        "headers": {
            "Authorization": token,
            "Content-Type": "application/json"
        },
        "data": {
            "from_path": from_path,
            "to_path": to_path
        }
    }
    r = requests.post(copy_req["url"], headers=copy_req["headers"],
                      data=json.dumps(copy_req["data"]))
    return r


def move(token, from_path, to_path):
    copy_req = {
        "url": "https://api.dropboxapi.com/2/files/move_v2",
        "headers": {
            "Authorization": token,
            "Content-Type": "application/json"
        },
        "data": {
            "from_path": from_path,
            "to_path": to_path
        }
    }
    r = requests.post(copy_req["url"], headers=copy_req["headers"],
                      data=json.dumps(copy_req["data"]))
    return r


# idx = 0
# r = list_folder(Auth)
# response = json.loads(r.text)
# for entry in response["entries"]:
#     if(entry[".tag"] == 'file' and entry["name"] == "Org Design Bureacacy.png"):
#         name = download(entry["path_lower"], Auth)
#         print(name)
#         exit()
# res = list_folder(Auth, "/New")
# print(res.text)


def find_file():
    i = random.randint(0, 99)
    folder = ""
    flag = 0
    file = None
    while flag == 0:
        if i < 50:
            print("Listing folder "+folder)
            r = list_folder(Auth, folder)
            # print(r.text)
            data = json.loads(r.text)
            size = len(data["entries"])
            idx = random.randint(0, size-1)
            if(data["entries"][idx][".tag"] == "file"):
                file = data["entries"][idx]
                flag = 1
            elif(data["entries"][idx][".tag"] == "folder"):
                folder = data["entries"][idx]["path_lower"]
                i = random.randint(0, 99)
            else:
                print("Error")
                exit()
        else:
            print("Searching in "+folder)
            r = search(Auth)
            data = json.loads(r.text)
            # print(r.text)
            size = len(data["matches"])
            idx = random.randint(0, size-1)
            if(data["matches"][idx]["metadata"]["metadata"][".tag"] == "file"):
                file = data["matches"][idx]["metadata"]["metadata"]
                flag = 1
            elif(data["matches"][idx]["metadata"]["metadata"][".tag"] == "folder"):
                folder = data["matches"][idx]["metadata"]["metadata"]["path_lower"]
                i = random.randint(0, 99)
            else:
                print("Error")
                exit()
    return file


def preview_file(file_entry):
    file = file_entry["path_lower"]
    file_extension = pathlib.Path(file).suffix
    if (file_extension in [".jpg", ".jpeg", ".png"]):
        prob = random.randint(0, 99)
        if(prob < 90):
            get_thumbnail(file, Auth)
            print("Got thumbnail for file "+file_entry["name"])
    elif (file_extension in [".ai", ".doc", ".docm", ".docx", ".eps", ".gdoc", ".gslides", ".odp", ".odt", ".pps", ".ppsm", ".ppsx", ".ppt", ".pptm", ".pptx", ".rtf"]):
        prob = random.randint(0, 99)
        if(prob < 90):
            get_preview(file, Auth)
            print("Got preview for file "+file_entry["name"])


def tamper_file(file):
    prob = random.randint(0, 99)
    if(prob < 60):

        from_path = file["path_lower"]
        idx = from_path.rfind("/")
        fileName = from_path[idx:]
        to_path = get_folder_path()+fileName
        prob2 = random.randint(0, 1)
        if(prob2 == 0):
            print("Moving file "+file["name"] +
                  " from "+from_path+" to "+to_path)
            r = move(Auth, from_path, to_path)
            if(r.status_code != 200):
                print(r.text)
            print("Moved file "+file["name"]+" from "+from_path+" to "+to_path)
        else:
            print("Copying file "+file["name"] +
                  " from "+from_path+" to "+to_path)
            r = copy(Auth, from_path, to_path)
            if(r.status_code != 200):
                print(r.text)
            print("Copied file "+file["name"] +
                  " from "+from_path+" to "+to_path)
    else:
        print("Downloading File "+file["name"])
        download(file["path_lower"], Auth)
        print("Downloaded file "+file["name"])


def user_process():
    file = find_file()
    print("file Found "+file["name"])
    preview_file(file)
    tamper_file(file)


while(True):
    # time.sleep(1)
    x = random.randint(0, 99)
    if(x < 10):
        user_process()
# get_preview("/f20190104@pilani.bits-pilani.ac.in’s files (1)/tutorial 9.pptx")
