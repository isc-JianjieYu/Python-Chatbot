from typing import List

def add_to_list(ls : List[str], adding : str):
    ls.append(adding)

lsCP : List[str] = list()

lsCP.append("hi")
lsCP.append("you")
lsCP.append("haha")
lsCP.append("lol")

print(lsCP)

add_to_list(lsCP, "ADD")

print(lsCP)