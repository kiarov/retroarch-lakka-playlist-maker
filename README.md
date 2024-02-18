
# RetroArch/Lakka playlists in 1-click! 👾
## The orignal project
[retroarch-lakka-playlist-maker](https://github.com/parklez/retroarch-lakka-playlist-maker) by parklez
## Why This fork?
I needed a faster way to create playlists for a cheap tv box (MXQ PRO 4k - Amlogic S805) running lakka 4.4 so I converted the original project from python 3 to python 2 and added a modified script to create playlists by just passing parameters to the python function. 

## Requirements 🐍

- Python 2

- Some programming and linux knowledge

  

## Download & Setup⚡

 1. Ssh into your lakka tv box and go to the storage root:

```bash
    cd /storage/
```
 2. Next download this repository
```bash
    wget https://github.com/kiarov/retroarch-lakka-playlist-maker/archive/refs/heads/master.zip
```
3. unzip everything
 ```bash
  unzip master.zip
```
4. Copy the two scripts to the root of the storage
 ```bash
  cp /storage/retroarch-lakka-playlist-maker-master/create_arcade_playlist.py /storage/ && cp /storage/retroarch-lakka-playlist-maker-master/create_playlist.py /storage/
```

## Examples of use 🐕‍🦺

You need to name your target roms folder the same as your libreelec db file i.e:

> ~/roms/genesis/{files}
> ~/genesis.db

### create_playlist.py usage

The script receives 2 parameters **{playlist name}** and **{db file name / target folder}**
Being the first the name you'll se in your playlists inside retroarch and the second the name of the db file and the folder containing the roms inside ~/roms folder.

   ```bash
    python create_playlist.py "Sega - Genesis" genesis
   ```

If you had no errors, you now should see a file named **Sega - Genesis.lpl** inside your ~/playlists folder containing all the found games.
### create_arcade_playlist.py usage
This one receives no parameters and expects that you already have a file named **FBneo.dat** at the root of your /storage/ folder and a **fbneo** folder inside ~/roms. 
For more information about this script I suggest you read parkles's original [documentation](https://github.com/parklez/retroarch-lakka-playlist-maker?tab=readme-ov-file#documentation-).


### Thanks
Thank you parkles for your original code in which this project is heavily based.
