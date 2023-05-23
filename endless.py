import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from betterlib import logging
import sys
import shutil

logger = logging.Logger("./endless.log", "endless")
root = tk.Tk()

if not os.path.exists(".did_setup"):
    root.withdraw()
    messagebox.showinfo("Welcome", "Welcome to Endless - A simple modding utility for Dead Cells. Please select your game install folder.")
    folder_selected = filedialog.askdirectory()
    with open(".did_setup", "w") as f:
        f.write(folder_selected)
    # show window again
try:
    folder_selected
except NameError:
    with open(".did_setup", "r") as f:
        folder_selected = f.read()

logger.info("Selected folder: " + folder_selected)

# draw window
root.title("Endless")
root.geometry("400x500")
root.resizable(False, False)

def check_backup():
    if os.path.exists(folder_selected + "/backup"):
        logger.info("Found backup")
        return True
    else:
        messagebox.showwarning("No backup found", "No backup found. Please backup your game files first, as shown in the installation guide.")
        logger.warn("No backup found")
        return False

def unpack(show_messagebox=True, unpack_filename="res.pak", unpack_to="UnpackedFiles"):
    check_backup()
    logger.info("Unpacking game files... (this may take a while)")
    origDir = os.getcwd()
    os.chdir(folder_selected)
    os.system("ModTools\PAKTool.exe -Expand -outdir " + unpack_to + " -refpak " + unpack_filename)
    os.chdir(origDir)
    logger.info("Unpacked game files!")
    if show_messagebox:
        messagebox.showinfo("Done", "Unpacked game files!")

def repack():
    check_backup()
    logger.info("Repacking game files... (this may take a while)")
    origDir = os.getcwd()
    os.chdir(folder_selected)
    os.system("ModTools\PAKTool.exe -Collapse -indir UnpackedFiles -outpak res.pak")
    logger.info("Repacked files, deleting unpacked files...")
    shutil.rmtree("UnpackedFiles")
    os.chdir(origDir)
    logger.info("Repacked game files!")
    messagebox.showinfo("Done", "Repacked game files!")

def fixPath(path):
    fixed = ""
    j = 0
    for i in path:
        if j <= len(fixed):
            fixed += i + "/"
            continue
        fixed += i
    return fixed

def package():
    check_backup()
    logger.info("Unpacking game files for diff... (this may take a while)")
    origDir = os.getcwd()
    os.chdir(folder_selected)
    os.system("ModTools\PAKTool.exe -Expand -outdir UnpackedFiles2 -refpak backup/res.pak")
    logger.info("Unpacked vanilla files.")
    logger.info("Diffing files...")
    os.system("diff -rq UnpackedFiles UnpackedFiles2 > diff.txt")
    logger.info("Deleting unpacked files...")
    shutil.rmtree("UnpackedFiles2")
    os.makedirs("ModFiles", exist_ok=True)
    logger.info("Copying changed files...")
    changed = []
    with open(folder_selected + "/diff.txt", "r") as f:
        for diff in f.readlines():
            if diff.strip().endswith("differ"):
                changed.append(fixPath(diff.split("Files ")[1].split(" and ")[0].split("/")[1:]))
    logger.info("Changed files: " + str(changed))
    for file in changed:
        fixedFile = file[:-1]
        logger.debug("copying " + fixedFile)
        # make directory if it doesn't exist
        os.makedirs("./ModFiles/" + "/".join(fixedFile.split("/")[:-1]), exist_ok=True)
        shutil.copyfile(folder_selected + "/UnpackedFiles/" + fixedFile, "./ModFiles/" + fixedFile)
    logger.info("Copied changed files to ModFiles.")
    logger.info("Packing mod...")
    origDir = os.getcwd()
    os.chdir(folder_selected)
    os.system("ModTools\PAKTool.exe -Collapse -indir " + origDir + "\ModFiles -outpak " + origDir + "\mod.pak")
    logger.info("Packed mod!")
    os.chdir(origDir) # just in case
    shutil.rmtree("ModFiles")

def start_modded():
    logger.info("Prompting user to choose mods...")
    messagebox.showinfo("Choose mods", "Please choose the mods you want to use.")
    mod_selected = filedialog.askopenfilenames(defaultextension=".pak", filetypes=[("Pak files", "*.pak")])
    logger.info("Selected mods: " + str(mod_selected))
    logger.info("Checking unpacked files...")
    if not os.path.exists(folder_selected + "/UnpackedFiles"):
        logger.info("Unpacked files not found, unpacking...")
        unpack(show_messagebox=False, unpack_filename="backup/res.pak")
    logger.info("Unpacked vanilla pak, unpacking mods...")
    i = 0
    for mod in mod_selected:
        unpack(show_messagebox=False, unpack_filename=mod, unpack_to="mod" + str(i))
        i += 1
    logger.info("Overwriting vanilla files with modded files...")
    j = 0
    for mod in mod_selected:
        try:
            shutil.copytree("mod" + str(i), "UnpackedFiles")
        except:
            logger.error("Failed to copy mod: " + mod + ". Will continue anyway.")
        j += 1
    logger.info("Packing modded files...")
    repack()
    logger.info("Deleting unpacked mods...")
    i = 0
    for mod in mod_selected:
        try:
            shutil.rmtree("mod" + str(i))
        except:
            logger.error("Failed to delete mod: " + mod + ". Will continue anyway.")
        i += 1
    logger.info("Starting game (modded pak)...")
    origDir = os.getcwd()
    os.chdir(folder_selected)
    os.system("start deadcells.exe")
    os.chdir(origDir)

def start_vanilla():
    logger.info("Starting game (vanilla pak)...")
    origDir = os.getcwd()
    os.chdir(folder_selected)
    shutil.copyfile("backup/res.pak", "res.pak")
    os.system("start deadcells.exe")
    os.chdir(origDir)

def unpack_cdb():
    logger.info("Unpacking CastleDB...")
    origDir = os.getcwd()
    os.chdir(folder_selected)
    os.system("ModTools\CDBTool.exe -Expand -outDir UnpackedCDB -refCDB UnpackedFiles/data.cdb")
    logger.info("Unpacked CastleDB!")
    os.chdir(origDir)
    messagebox.showinfo("Done", "Unpacked CastleDB!")

def repack_cdb():
    logger.info("Repacking CastleDB...")
    origDir = os.getcwd()
    os.chdir(folder_selected)
    os.system("ModTools\CDBTool.exe -Collapse -inDir UnpackedCDB -outCDB UnpackedFiles/data.cdb")
    logger.info("Repacked CastleDB!")
    os.chdir(origDir)
    messagebox.showinfo("Done", "Repacked CastleDB!")
    
# header
tk.Label(root, text="Endless", font=("Arial", 20)).grid(row=0, column=5)
tk.Label(root, text="A simple modding utility for Dead Cells", font=("Arial", 10)).grid(row=1, column=5)

buttons = {
    "Unpack game files": unpack,
    "Unpack CastleDB (Run after unpacking)": unpack_cdb,
    "Repack CastleDB (Run before repacking)": repack_cdb,
    "Repack game files": repack,
    "Package mod": package,
    "Start game (Modded)": start_modded,
    "Start game (vanilla)": start_vanilla,
    "Exit": sys.exit
}

for i, (text, command) in enumerate(buttons.items()):
    tk.Button(root, text=text, command=command).grid(row=(i*2)+4, column=5)

root.mainloop()