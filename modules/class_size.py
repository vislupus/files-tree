import os
from pathlib import Path


class Structure():
    def __init__(self):
        self.size = 0
        self.folders = {}
        self.files = {}


class File_tree():
    """This is a module for visualizing the file tree and the size of files."""

    def __init__(self, runtests=False):
        self.root_path = os.getcwd()
        self.data = {}
        self.level_add = set()
        self.level_rem = set()
        self.fold = []

        # if runtests:
        #     self.traverse()


    def size_con(self, num):
        return f"{num/1000000:.1f} MB"


    def add_dict(self, obj, parent, folder):
        if (parent in obj) and (folder not in obj[parent]['folders']):
            obj[parent]['folders'][folder] = vars(Structure())

        for p in obj:
            if p != parent:
                if isinstance(obj[p], dict):
                    self.add_dict(obj[p], parent, folder)


    def add_files(self, obj, parent, folder, file):
        if parent in obj:
            obj[parent]['folders'][folder]['files'][file] = os.path.getsize(file)

        for p in obj:
            if p != parent:
                if isinstance(obj[p], dict):
                    self.add_files(obj[p], parent, folder, file)


    def file_paths(self, d, seen=[]):
        for k, v in d.items():
            if not isinstance(v, dict):
                if k!='size':
                    yield {v:seen+[k]}
            else:
                yield from self.file_paths(v, seen+[k])


    def add_size(self, d, key, size):
        for k, v in d.items():
            if key == k:
                d[k]["size"] += size
            else:
                if isinstance(v, dict):
                    self.add_size(v, key, size)


    def traverse(self):
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                file_path = os.path.join(root, file)

                folder_path = os.path.dirname(file_path)
                folder_p = Path(folder_path)
                folder_parent_path = str(Path(*folder_p.parts[:-1]))

                if folder_path == self.root_path:
                    if folder_path not in self.data:
                        self.data[folder_path] = vars(Structure())

                    self.data[folder_path]['files'][file_path] = os.path.getsize(file_path)
                else:
                    self.add_dict(self.data, folder_parent_path, folder_path)

                self.add_files(self.data, folder_parent_path, folder_path, file_path)


        paths = list(self.file_paths(self.data))

        for p in paths:
            key=[*p][0]
            val=p[key]
            for v in val[:-1]:
                if (v!="folders") and (v!="files"):
                    self.add_size(self.data, v, key)


        # self.read_tree(self.data)
        return self.data



    def read_tree(self, obj, level=0):
        space = '    '
        branch = '│   '
        tee = '├── '
        last = '└── '


        for k, v in obj.items():
            name = str(Path(*Path(k).parts[-1:]))
           
            if name == 'folders':
                if level not in self.level_rem:
                    self.level_add.add(level)

            if isinstance(obj[k], dict):
                size = 0
                try:
                    size = obj[k]['size']
                except:
                    pass

                if ('folders' not in obj[k].keys()) and (len(obj[k].keys()) > 1):
                    root, ext = os.path.splitext(list(obj[k].keys())[0])
                    if ext == "":
                        self.fold.append(str(Path(*Path(list(obj[k].keys())[-1]).parts[-1:])))
                        self.level_add.add(level + 1)

                text = ""
                for i in range(level):
                    if i + 1 == level:
                        text += last
                    elif name in self.fold:
                        self.level_rem.add(level - 1)
                        self.level_add.discard(level)

                        text += branch
                    elif i + 1 in self.level_add:
                        text += branch
                    else:
                        text += space
                
                if (name!="folders") and (name!="files"):
                    print(f"""{text}{name} - {self.size_con(size)}""")
                else:
                    print(f"""{text}{name}""")

                self.read_tree(obj[k], level=level + 1)
            else:
                if k != "size":
                    text = ""
                    for i in range(level):
                        self.level_rem.add(level - 1)
                        self.level_add.discard(level)

                        if i + 1 == level:
                            text += last
                        elif (i + 1 in self.level_add) and (i + 1 < level - 1):
                            text += branch
                        else:
                            text += space

                    print(f"""{text}{name} - {self.size_con(v)}""")


print(__name__)