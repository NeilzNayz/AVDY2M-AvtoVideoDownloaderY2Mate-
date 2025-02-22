# AVDY2M-AvtoVideoDownloaderY2Mate (Avditom)

## What is this?

This script simplifies video downloading, especially when you need to download an entire playlist from YouTube.

## &#x2612; Do NOT

- Decrease sleep() values in the scripts.
- Run multiple instances in paralell for downloading.

Otherwise, the website may think you are DDoS'ing and block you for several hours or even days, preventing any downloads.

## Instalation

Before running the script, make sure you have Python installed and the required dependencies. Install them using:

```
pip install -r requirements.txt
```

## How to Use

After downloading the repository, run the main sript:

```
python app.py
```

When the script starts, it will display a welcome message and prompt:

```
command:
```

## 1. Setup

Before starting a download, you need to configure two required **variables**:

- path (where videos will be saved)
- url (YouTube video or playlist URL)

To set them, use the folowing format:

```
variableName = value
```

For example:

```
path = path/where/videos/will/be/downloaded
```

```
 url = https:/youtube.com/your-video-or-playlist-url
```

Once both variables are set, you can proceed.

## 2. Start Downloading

Run the script by entering:

```
run
```

If any required variable is missing, the script will notify you.

<details>
    <summary>If URL is a video</summary>
The script will automatically download the video.
</details>

<details>
    <summary>If URL is a playlist</summary>
The script will ask how you want to download the playlist. You have several options:

- press Enter &#8594; Download all videos in the playlist
- : &#8594; Download all videos in the playlist
- **form**: &#8594; Start downloading from a specific video
- :**to** &#8594; Download up to a specific video
- **from**:**to** &#8594; Download a specific range

#### Example:

We have a playlist that contains 20 videos. In **input:**, for examle, we can enter:

| command     | result                                  |
| :---------- | :-------------------------------------- |
| press Enter | Download all videos in the playlist     |
| :           | Download all videos in the playlist     |
| 10:         | Downloads from the 10th video onward    |
| :15         | Downloads from the start up to video 15 |
| 10:15       | Downloads videos 10 to 15 (inclusive)   |

</details>

## 3. Wait for Completion

If the playlist is large, downloading will take some time. While waiting, you can work on something else, but note that the script may pop up over other windows.

## Known Issues & Solutions

- Website Crashes: If the site stops responding, restart the download. Future updates will include an automatic retry feature.
- Slow Downloads: If a specific video downloads slowly, try downloading from another device or skipping that video using from:to

## To Do / Future Updates

- [] Implement automatic recovery whent the website crashes.
- [] Optimize download speed detection
- [] Improve error handling and logging

## License

This project is licensed under the MIT License. Feel free to modify and use it!

## Contributing

Pull requests and issue reports are welcome. If you find a bug or have a suggestions, open an issue in the repository
