import os
from pathlib import Path


class Structure():
    def __init__(self):
        self.size = 0
        self.folders = {}
        self.files = {}


class File_tree():
    """This is a module for visualizing the file tree and the size of files."""

    def __init__(self, runtests=True):
        self.root_path = os.getcwd()
        self.data = {}
        self.level_add = set()
        self.level_rem = set()
        self.fold = []
        self.exclude_dirs = [".git", ".vscode", "modules"]

        if runtests:
            self.traverse()


    def size_con(self, num):
        return f"{num/1000000:.1f} MB"
    

    def sub_add_dic(self, obj, parent, folder):
        print(parent)
        print(folder)
        dirs = [item for item in os.listdir(folder) if os.path.isdir(os.path.join(folder, item))]
        print("++ ", dirs)
        print(obj)

        for dir in dirs:
            if not dir in self.exclude_dirs:
                new_dir_child = os.path.join(folder, dir)
                obj[new_dir_child] = vars(Structure())

                print(new_dir_child)
                print([item for item in os.listdir(new_dir_child) if os.path.isdir(os.path.join(new_dir_child, item))])

                self.sub_add_dic(obj[new_dir_child]['folders'], folder, new_dir_child)
                # print(obj[parent]['folders'][folder]['folders'])

                    



    def add_dict(self, obj, parent, folder):
        # print("==", parent)
        # print(folder)
        # print([item for item in os.listdir(parent) if os.path.isdir(os.path.join(parent, item))])
        # folder_path = Path(self.root_path)
        # last_folder = Path(*Path(folder).parts[len(folder_path.parts):])
        # level = len(folder_path.parts) - folder_path.parts.index(last_folder) - 1
        # print(len(folder_path.parts), len(last_folder.parts))
        # print(Path().joinpath(*Path(folder).parts[-4:]))
        if parent in obj:
            print(" -- ", folder)
            if folder not in obj[parent]['folders']:
                obj[parent]['folders'][folder] = vars(Structure())

                self.sub_add_dic(obj[parent]['folders'][folder]['folders'], parent, folder)

                # dirs = [item for item in os.listdir(folder) if os.path.isdir(os.path.join(folder, item))]
                # print("++ ", dirs)

                # for dir in dirs:
                #     if not dir in self.exclude_dirs:
                #         if dir not in obj[parent]['folders'][folder]['folders']:
                #             new_dir_child = os.path.join(folder, dir)
                #             obj[parent]['folders'][folder]['folders'][new_dir_child] = vars(Structure())

                #             print(new_dir_child)
                #             print([item for item in os.listdir(new_dir_child) if os.path.isdir(os.path.join(new_dir_child, item))])


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

                # check if it is on the root level
                if folder_path in self.root_path:
                    if folder_path not in self.data:
                        self.data[folder_path] = vars(Structure())
                    
                    # add files on root level
                    self.data[folder_path]['files'][file_path] = os.path.getsize(file_path)

                    # add directories on root level
                    for dir in dirs:
                        # exclude some directories
                        if not dir in self.exclude_dirs:
                            if dir not in self.data[folder_path]['folders']:
                                self.data[folder_path]['folders'][os.path.join(folder_path, dir)] = vars(Structure())
                else:
                    # exclude some directories
                    if not any(exclude_dir in folder_path for exclude_dir in self.exclude_dirs):
                        self.add_dict(self.data, folder_parent_path, folder_path)
                        self.add_files(self.data, folder_parent_path, folder_path, file_path)



        paths = list(self.file_paths(self.data))

        for p in paths:
            key=[*p][0]
            val=p[key]
            for v in val[:-1]:
                if (v!="folders") and (v!="files"):
                    self.add_size(self.data, v, key)


        self.read_tree(self.data)
        # return self.data



    def read_tree(self, obj, level=0):
        space = '    '
        branch = '│   '
        tee = '├── '
        last = '└── '

        for n, (k, v) in enumerate(obj.items()):
            name = str(Path(*Path(k).parts[-1:]))
            # print(level, n, self.level_add, k)
            # print(self.level_add)
            # remove level with folders
            if name == 'folders':
                if level not in self.level_rem:
                    self.level_add.add(level)
                    # print(138, self.level_add)

            if isinstance(obj[k], dict):
                size = 0
                try:
                    size = obj[k]['size']
                except:
                    pass
                
                # print(obj[k].keys(), 
                #       'folders' not in obj[k].keys(), len(obj[k].keys()) > 1, 
                #       ('folders' not in obj[k].keys()) and (len(obj[k].keys()) > 1))
                if ('folders' not in obj[k].keys()) and (len(obj[k].keys()) > 1):
                    root, ext = os.path.splitext(list(obj[k].keys())[0])
                    if ext == "":
                        # self.fold.append(str(Path(*Path(list(obj[k].keys())[-1]).parts[-1:])))
                        # print(self.fold)
                        self.level_add.add(level + 1)
                        # print(155, self.level_add)

                text = ""
                for i in range(level):
                    if i + 1 == level:
                        if n + 1 == len(obj):
                            # print("end", self.level_add)
                            self.level_add.add(level + 1)

                            text += last

                            self.level_rem.add(level - 1)
                            self.level_add.discard(level)
                        else:
                            # print("start", self.level_add)

                            self.level_add.add(level + 1)

                            text += tee
                    # elif name in self.fold:
                        # self.level_rem.add(level - 1)
                        # self.level_add.discard(level)
                        # print(168, self.level_add)

                        # text += branch
                    elif i + 1 in self.level_add:
                        # self.level_rem.add(level - 1)
                        # self.level_add.discard(level)
                        # print(173, self.level_add)

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
                        # self.level_rem.add(level - 1)
                        # self.level_add.discard(level)

                        # print(190, self.level_add)

                        if i + 1 == level:
                            if n + 1 == len(obj):
                                # self.level_rem.add(level - 1)
                                # self.level_add.discard(level)

                                text += last
                            else:
                                # self.level_add.add(level + 1)

                                text += tee

                        elif (i + 1 in self.level_add) and (i + 1 < level - 1):
                            text += branch
                        else:
                            text += space

                    print(f"""{text}{name} - {self.size_con(v)}""")


# print(__name__)

File_tree()