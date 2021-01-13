import copy
import json
from internetarchive import get_item, modify_metadata
import subprocess

# This is a botch script, its not meant to be perfect, just meant to get the job done


# --------------
from tqdm import tqdm


# As the function's name says, ods to json, ignore for now
def ods2json(dataset: dict):
    templist = []
    dataset.pop("README", None)  # Removing the Readme Page
    dataset.pop("TARs", None)  # Removing the TARS Page
    dataset.pop("Dropdowns", None)  # Removing the DROPDOWNS Page
    for key in dataset:
        del (dataset[key][0])  # Deleting File Name Table
        for j in range(0, len(dataset[key])):
            for a in range(0, len(dataset[key][j])):
                try:
                    if dataset[key][j][a] == '':
                        dataset[key][j][a] = 'unsorted'
                except:
                    pass
            try:

                template = {
                    "title": dataset[key][j][1],
                    "description": dataset[key][j][2],
                    "developers": dataset[key][j][4],
                    "date": dataset[key][j][5],
                    "version": dataset[key][j][6],
                    "category": dataset[key][j][7],
                    "ppsspp": dataset[key][j][8],
                    "psp": dataset[key][j][9],
                    'url': dataset[key][j][10]
                }
                templist.append(template)
            except:
                pass
    return templist


# IGNORE
template_tags = ['application',
                 'game',
                 'emulator',
                 'port',
                 'demo']

if __name__ == '__main__':

    print("""
Made by Crisp.
THIS IS ONLY TO BE USED BY ADMINS

WARNING THIS SCRIPT WILL GIVE EVERY UPLOAD THE TAG "PSP Homebrew"
Then it will check if category tags are present in "subject" and it will try to fill them.

This script has been tested before but ALWAYS monitor it since changes are done to the main tags!!
It will only check for and add if present the following categories :
'application','game','emulator','port','demo'

Enter 1 to start
Enter 2 to exit

""")
    usrinput = input("Enter value : ")
    if str(usrinput) == '1':
        ids = subprocess.run("ia search 'collection:psp-homebrew-library'", shell=True, capture_output=True)
        ids = ids.stdout
        ids = ids.decode('utf-8').splitlines()
        for i in tqdm(range(1, len(ids))):
            idz = json.loads(ids[i])['identifier']
            cache = get_item(idz).item_metadata['metadata']
            temp = copy.deepcopy(cache)
            if 'subject' not in temp.keys():
                temp['subject'] = ['PSP homebrew']
                cache['subject'] = ['PSP homebrew']

            if isinstance(temp['subject'], list):
                if 'PSP homebrew' not in temp['subject']:
                    temp['subject'].append('PSP homebrew')
                if 'psp homebrew' in temp['subject']:
                    temp['subject'].remove('psp homebrew')
                val = False
                for z in range(0, len(temp['subject'])):
                    if temp['subject'][z] in template_tags:
                        val = True
                if val is False:
                    try:
                        tag = searcher(idz)['category'].lower()
                        temp['subject'].append(tag)
                    except:
                        pass

            elif isinstance(temp['subject'], str):
                temp['subject'] = [temp['subject']]
                cache['subject'] = [cache['subject']]
                if 'PSP homebrew' not in temp['subject']:
                    temp['subject'].append('PSP homebrew')
                if 'psp homebrew' in temp['subject']:
                    temp['subject'].remove('psp homebrew')
                val = False
                for z in range(0, len(temp['subject'])):
                    if temp['subject'][z] in template_tags:
                        val = True
                if val is False:
                    try:
                        tag = searcher(idz)['category'].lower()
                        temp['subject'].append(tag)
                    except:
                        pass
            if 'psp homebrew' in cache['subject']:
                cache['subject'].remove('psp homebrew')
            modify_metadata(idz, metadata={'subject': list(set((temp['subject'] + cache['subject'])))})
            modify_metadata(idz, metadata={'mediatype': 'software'})
            print(f"{idz} is now {list(set((temp['subject'] + cache['subject'])))}")
    elif str(usrinput) == '2':
        print('Program Aborted.')
        exit()
    else:
        exit()
