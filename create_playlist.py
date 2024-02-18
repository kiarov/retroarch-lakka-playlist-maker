import os
import json
import sys
import re

class Playlist(object):
    playlists = []

    def __init__(self, name, source, output, filters=None, core='', search_recursively=False, dat_file=None):
        '''Class that defines a playlist.

        Args:
            name (str): Name of the playlist.
            source (str): Path to folder containing ROMs.
            output (str): Path to '/retroarch/playlists'.
            filters (list, optional): Allowed file extensions without comma. Defaults to [].
            core (str, optional): Name of the core to be utilized. Defaults to 'DETECT'.
            search_recursively (bool): If True, scanner walks through subdirs recursively.
            dat_file (str, optional): path to dat file.
        '''
        self.name = name
        self.source = source
        self.output = output
        self.filters = filters or []
        self.core = core
        self.search_recursively = search_recursively
        self.files = self.scan_files()
        self.dat_file = dat_file
        Playlist.playlists.append(self)

    def scan_files(self):
        files = []
        try:
            if self.search_recursively:
                for root, _dirs, _files in os.walk(self.source):
                    for file_name in _files:
                        rel_dir = os.path.relpath(root, self.source)
                        rel_file = os.path.join(rel_dir, file_name)
                        if rel_file.startswith('.'):
                            rel_file = rel_file[2:]
                        files.append(rel_file)
            else:
                files = [f for f in os.listdir(self.source) if os.path.isfile(os.path.join(self.source, f))]
        except OSError:
            pass
        return files

    def create_playlist(self):
        playlist = {
            'version': '1.4',
            'default_core_path': self.core,
            'default_core_name': '',
            'label_display_mode': 0,
            'right_thumbnail_mode': 0,
            'left_thumbnail_mode': 0,
            'sort_mode': 0,
            'items': []
            }

        files = self.iterate_items()
        playlist['items'] = files
        print('[{}] {}'.format(len(files), self.name))
        self.write_to_disk(playlist)

    def iterate_items(self):
        print('mejecuto')
        files = []
        for file in self.files:
            if not self.filters or file.split('.')[-1] in self.filters:
                name = os.path.split(file)[-1]
                name = name[:name.rfind('.')]
                item = {
                    'path': os.path.join(self.source, file),
                    'label': name,
                    'core_path': 'DETECT',
                    'core_name': 'DETECT',
                    'crc32': 'DETECT',
                    'db_name': '{}.lpl'.format(self.name)
                    }
                files.append(item)
        return files

    def write_to_disk(self, playlist):
        file = os.path.join(self.output, '{}.lpl'.format(self.name))
        with open(file, 'w') as f:
            json.dump(playlist, f, indent=4)

class Arcade(Playlist):

    def __init__(self, *args, **kwargs):
        '''Class that defines an Arcade playlist.

        Args:
            *args: Inherited parameters from Playlist.
            dat_file (str, optional): path to dat file. Defaults to 'MAME 0.233 - Split.dat'.
        '''
        dat_file = kwargs.pop('dat_file', 'MAME 0.233 - Split.dat')
        super(Arcade, self).__init__(*args, dat_file=dat_file, **kwargs)

    def iterate_items(self):
        files_found = []
        files = []
        bios = ['neogeo.zip']
        with open(self.dat_file, 'r') as dat:
            lines = dat.readlines()
            for line in lines:
                if line.startswith('	rom'):
                    # file = line.split()[3]

                    cadena= line
                    # Encontrar la posición del primer carácter "
                    inicio = cadena.find('"')

                    # Encontrar la posición del último carácter .
                    fin = cadena.rfind('.zip"') + 4

                    # Extraer la subcadena desde " hasta .
                    file = cadena[inicio + 1:fin]

                    # print('found: ' + file)  # Salida: "Aladdin (Japan).zip"
                    # print(file)
                    if file in self.files and file not in bios:
                        files_found.append(file)
                        description = re.findall(r'"([^"]*)"', lines[lines.index(line)])[0].replace('.zip', '')
                        print(description)
                        item = {
                            'path': os.path.join(self.source, file),
                            'label': description,
                            'core_path': 'DETECT',
                            'core_name': 'DETECT',
                            'crc32': 'DETECT',
                            'db_name': '{}.lpl'.format(self.name)
                            }
                        files.append(item)
        missing_files = list(filter(lambda x: x not in files_found, self.files))
        if missing_files:
             print('[-{}] {} | Not found in .dat: {}'.format(len(missing_files), self.name, missing_files))
        return files

def create_everything():
    for item in Playlist.playlists:
        item.create_playlist()
    input('\n[Done] Playlist(s) successfully created or updated.\n Press [ENTER] to exit.')

# Entry examples
RETROARCH_PLAYLIST_PATH = '/storage/playlists/'

Arcade(sys.argv[1], '/storage/roms/{}/'.format(sys.argv[2]), RETROARCH_PLAYLIST_PATH, dat_file='./{}.dat'.format(sys.argv[2]))

if __name__ == '__main__':
    create_everything()
