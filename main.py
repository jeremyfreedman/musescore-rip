#!/usr/bin/python3
import requests
import sys
import os
import glob
import pigar
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from fpdf import FPDF


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
            print("[musescore-rip] Found page", str(counter))
        else:
            done = True
    return paths


def get_id():
    i0 = sys.argv[1].find("scores/")
    return sys.argv[1][i0+8:]+'/'


def grab_svg(paths):
    foldername = "download/"+get_id()
    files = []
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    for p in range(len(paths)):
        filename = foldername+paths[p].split('/')[-1]
        r = requests.get(paths[p])
        with open(filename, 'wb') as output_file:
            output_file.write(r.content)
            d = svg2rlg(filename)
            renderPM.drawToFile(d, filename+'.png', fmt='PNG')
            files.append(filename+'.png')
            print("[musescore-rip] Successfully grabbed page", str(p+1))
    return files


def build_pdf(files):
    pdf = FPDF()
    position = "download/"+get_id()+"complete.pdf"
    for f in files:
        pdf.add_page()
        pdf.image(f, 0, 0)
    pdf.output(position)
    print("[musescore-rip] Done! Output:", position)


def cleanup():
    images = glob.glob("download/"+get_id()+"*.svg*")
    for i in images:
        os.remove(i)
    print("[musescore-rip] Cleaning up...")


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: ./main.py <musescore url> [nocleanup]")
    else:
        print(get_file_path(sys.argv[1]))
        build_pdf(grab_svg(get_all_paths(get_file_path(sys.argv[1]))))
        if len(sys.argv) == 2:
            cleanup()
        elif sys.argv[2] != 'nocleanup':
            cleanup()
