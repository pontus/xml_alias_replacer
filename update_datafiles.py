#!/usr/bin/env python3

import xml.etree.ElementTree
import uuid
import typing

files = ("dataset.xml", "images.xml")
types = ("BPDATASET", "IMAGE")

idmapping = {}
trees = {}


def generate_id(tag: str, alias: str) -> str:
    u = uuid.uuid4()
    id = f"{tag}-{u}"
    idmapping[alias] = id
    return id


def assign_ids(tree: xml.etree.ElementTree.Element) -> None:
    if tree.tag in types:
        tree.attrib["accession"] = generate_id(tree.tag, tree.attrib["alias"])
        del tree.attrib["alias"]

    for child in tree:
        assign_ids(child)


def replace_aliases(tree: xml.etree.ElementTree.Element) -> None:
    if "refname" in tree.attrib and tree.attrib["refname"] in idmapping:
        tree.attrib["accession"] = idmapping[tree.attrib["refname"]]
        del tree.attrib["refname"]

    for child in tree:
        replace_aliases(child)


for xmlfile in files:
    tree = xml.etree.ElementTree.parse(xmlfile)
    root = tree.getroot()
    assign_ids(root)
    trees[xmlfile] = tree

for tree in trees.values():
    replace_aliases(tree.getroot())

for filename in trees:
    trees[filename].write(f"{filename}.ny")
