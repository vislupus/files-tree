from modules.class_size import File_tree

def main():
    files = File_tree()
    print(files.__doc__)
    print(files.root_path)

    data = files.traverse()
    files.read_tree(data)


if __name__ == "__main__":
    main()
