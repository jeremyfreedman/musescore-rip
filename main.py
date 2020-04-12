#!/usr/bin/python3
import requests
import sys


def get_file_path(url):
    r = requests.get(url)
    c = str(r.content)
    i0 = c.find("image/svg+xml")
    i1 = c.find("http", i0)
    i2 = c.find("svg", i1) + 3
    return c[i1:i2]


def get_all_paths(path):
    underscore = path.find("_")
    pre = path[:underscore+1]
    post = path[underscore+2:]
    done = False
    paths = []
    counter = 0
    while not done:
        r = requests.get(pre+str(counter)+post)
        if (r.status_code == 200):
            paths.append(r.url)
            counter += 1
        else:
            done = True
    return paths


def build_pdf(paths):
    for p in paths:
        filename = 'download/'+p.split('/')[-1]
        r = requests.get(p)
        with open(filename, 'wb') as output_file:
            output_file.write(r.content)
    return 0


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: ./main.py <musescore url>")
    else:
        build_pdf(get_all_paths(get_file_path(sys.argv[1])))
