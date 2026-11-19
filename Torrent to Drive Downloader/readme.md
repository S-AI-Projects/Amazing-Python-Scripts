
# Automatic Torrent to Drive Downloader

BY running *leech.ipynb* in google-colab you can manage to download any torrent file with upto 70 GB without any interruption.

**Steps to be followed**
1. run colab cells sequentially.
2. Allow google colab access to your Google Drive.
3. Convert your torrent to magnet.
4. paste it in output of input cells.
5. Have patience until it donwloads completely.

**Things to remember** 

* colab runs upto 3 hours even you close it.
* iit can run upto 12 hours max if you keep it open and answer its capacha.

***Thank you***

## Elapsed-time display

After the download finishes, the notebook formats its elapsed duration as whole minutes and remaining seconds. The formatting calculation is isolated in `format_elapsed(seconds)` in the download cell: `divmod(int(seconds), 60)` returns the minute count and the remainder. For example, 0 seconds displays as `0 min : 0 sec`, and 125.9 seconds displays as `2 min : 5 sec`. The notebook keeps the `Elapsed Time: ` label and output format.

Run `python3 work/R29-T046/check.py` to verify these examples without connecting to Google Drive or a torrent network.
