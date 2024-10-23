# 👱 Installation and run the app

All you need to install and run the app is placed under `assets` at our [releases section](https://github.com/AntonioMrtz/SpotifyElectron/releases). Choose the latest version for the most improved user experience.

## 🪟 Windows (.exe)

- Go to the [latest release](https://github.com/AntonioMrtz/SpotifyElectron/releases)
- In `assets` section download the file named `SpotifyElectron.exe`
- Once download, double click on the app icon and select accept
- Now you have the app installed, access it with the Desktop icon or searching the installed app in Windows Search

## 🐧 Linux (AppImage)

- Go to the [latest release](https://github.com/AntonioMrtz/SpotifyElectron/releases)
- In `assets` section download the file named `SpotifyElectron.AppImage`
- Once downloaded, give permissions to the `.AppImage` file with `chmod +x SpotifyElectron.AppImage`
- Then run with `./SpotifyElectron.AppImage --no-sandbox`

### Create Desktop icon

#### 1. Download needed assets

- In `assets` section download the file named `SpotifyElectron.AppImage`. The exectuable AppImage.
- In `assets` section download the file named `spotify-electron.desktop`. The desktop entry template.
- In `assets` section download the file named `logo.png`. The app logo for desktop entry.

#### 2. AppImage and assets placing

```console
cd ~/Downloads # go into downloads folder
mkdir ~/SpotifyElectron # create app directory, if it exists skip this command
chmod +x SpotifyElectron.AppImage # give permissions to AppImage
cp  SpotifyElectron.AppImage ~/SpotifyElectron/ # copy AppImage to app directory
```

#### 3. Desktop entry set up and permissions

```console
cd ~/Downloads # go into downloads folder
mv spotify-electron.desktop.download spotify-electron.desktop # rename .desktop file, if it doesn't end in .dowload skip this step
chmod +x spotify-electron.desktop # give execution permissions
cp spotify-electron.desktop ~/.local/share/applications/ # move .desktop file where other .desktop are
mv logo.png spotify-electron-logo.png # rename icon name to fit xdg standars
xdg-icon-resource install spotify-electron-logo.png --size 64 # install icon
update-desktop-database ~/.local/share/applications # refresh .desktop entries
```

#### 4. Search for Spotify Electron with the app explorer -> Log out or restart if you don't see the entry

#### 5. Select the app and run it

### Debian/Ubuntu troubleshoot

The package `libfuse2` could not be installed. Install it with `sudo apt install libfuse2`
