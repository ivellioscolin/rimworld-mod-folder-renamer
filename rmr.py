# BSD 3-Clause License

# Copyright (c) 2023- , Colin Xu <colin.xu@gmail.com>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import sys, os, unicodedata, re
import json, xml.etree.ElementTree

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def ParseModDatabase(db_f):
    db = None
    try:
        db_json = open(db_f, 'r', encoding = 'utf-8')
        db = json.load(db_json)
    except:
        # Change to your code page if can't load
        db_json = open(db_f, 'r', encoding = 'gbk')
        db = json.load(db_json)
    return db

def RenameModFolder(mod_dir, mod_db, bSteam, test_mode):
    if test_mode:
        print('******** Trial Run Mode ********')
    if bSteam:
        print('Rename mod folder to steam style')
    else:
        print('Rename mod folder to steam mod id + mod name')
    for fd in os.listdir(mod_dir):
        mod_local = os.path.join(mod_dir, fd)
        if os.path.isdir(mod_local):
            mod_local_info = xml.etree.ElementTree.parse(os.path.join(mod_local, 'About', 'About.xml'))
            mod_local_name = mod_local_info.find('name').text
            mod_local_package_id = mod_local_info.find('packageId').text

            steam_mod_id = None
            steam_mod_name = None
            for mod_steam in mod_db['database']:
                if mod_local_package_id.lower() == (mod_db['database'][mod_steam]["packageId"]).lower():
                    steam_mod_id = mod_steam
                    break

            mod_src = mod_local

            if steam_mod_id is None:
                print('W:',mod_local_name+'('+mod_local_package_id+') is not a steam mod')
                dst = slugify(mod_local_name, True)
                #mod_dst = os.path.join(os.path.dirname(mod_local), slugify(mod_local_name, True))
            else:
                if bSteam == True:
                    dst = steam_mod_id
                    #mod_dst = os.path.join(os.path.dirname(mod_local), steam_mod_id)
                else:
                    dst = steam_mod_id+"("+slugify(mod_local_name, True)+")"
                    #mod_dst = os.path.join(os.path.dirname(mod_local), steam_mod_id+"("+slugify(mod_local_name, True)+")")

            if not fd == dst:
                print('I:',fd,"->",dst)
                if not test_mode:
                    os.rename(os.path.join(mod_dir, fd), os.path.join(mod_dir, dst))
            #if not mod_src == mod_dst:
                #print('o',mod_src,"->",mod_dst)
                #if not test_mode:
                #    os.rename(mod_src, mod_dst)
    if test_mode:
        print('-------- Trial Run Mode --------')

def Help():
    print("Rimworld Mod folder Renamer\n")
    print("Usage:")
    print("python rmr.py <mod_dir> <mode> <t>")
    print("  mod_dir: The parent directory of all mods")
    print("  mode:")
    print("        s: Mod folder will be renamed to \"<steam workshop ID>\"")
    print("        n: Mod folder will be renamed to \"<steam workshop ID>(<mod name>)\"")
    print("        Non-steam mod folder will be renamed to \"<mod name>\"")
    print("  t: If specified, only trial run without actual renaming")

def main():
    args = sys.argv[1:]
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'db.json')

    if not os.path.isfile(db_file):
        print("Missing db.json. Copy database/db.json from RimPy to script directory and re-run.")
        quit()

    if (len(args) == 2 or len(args) == 3) and os.path.isdir(args[0]) and (args[1].lower() == 's' or args[1].lower() == 'n'):
        test_mode = False
        if len(args) == 3:
            if args[2].lower() == 't':
                test_mode = True
            else:
                print("Only t enables trial run")
                quit()
        mod_database = ParseModDatabase(db_file)
        RenameModFolder(args[0], mod_database, True if args[1].lower() == 's' else False, test_mode)

    else:
        Help()
        quit()

if __name__ == "__main__":
    main()