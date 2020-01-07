
import bandcamp_crawler as bcc
import saver as s
import urllib3
import certifi
import json
import requests

import numpy as np

# imports for librosa
import matplotlib.pyplot as plt
import librosa
import librosa.display


def main():
    seed_url = 'https://menitrust.bandcamp.com/album/oncle-jazz'
    num_to_crawl = 10
    save_file = 'album_data_file'
    save = s.FileSaver(save_file)
    graph, scraped_data = bcc.general_crawl(seed_url=seed_url, num_to_crawl=num_to_crawl, saver=save)

    data = load_json_data(save_file)
    artist = data[0]['author']
    song_name = data[0]['album_data']['songs'][0][0]
    song = data[0]['album_data']['songs'][0][1]['mp3-128']
    print(song)
    download_song_mp3(song, song_name, artist)

    #audio_path = librosa.util.example_audio_file()
    #y, sr = librosa.load(audio_path)


    y, sr = librosa.load(song_label(song_name, artist))
    print(sr)

    # Let's make and display a mel-scaled power (energy-squared) spectrogram
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
    # Convert to log scale (dB). We'll use the peak power (max) as reference.
    log_S = librosa.power_to_db(S, ref=np.max)
    # Make a new figure
    plt.figure(figsize=(12, 4))
    # Display the spectrogram on a mel scale
    # sample rate and hop length parameters are used to render the time axis
    librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
    # Put a descriptive title on the plot
    plt.title('mel power spectrogram')
    # draw a color bar
    plt.colorbar(format='%+02.0f dB')
    # Make the figure layout compact
    plt.tight_layout()
    plt.show()


def load_json_data(file_name):
    """
    Loads a file with multiple json objects that are separated by a new-line
    """
    with open(file_name, 'r') as f:
        data = []
        for json_obj_string in f.read().strip().split('\n'):
            data.append(json.loads(json_obj_string))
        return data


def song_label(song_name, artist):
    return '_'.join((song_name + '-by-' + artist).split()) + '.mp3'


def download_song_mp3(song_url, song_name, artist):
    """
    downloads mp3 to a file with name of the form song_name-by-artist_name
    """
    song_file_name = song_label(song_name, artist)
    with open(song_file_name, 'wb') as f:
        response = requests.get(song_url)
        f.write(response.content)

    #http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
    #                           ca_certs=certifi.where())
    #resp = http.request('GET', song_url, timeout=2.5)
    #song_file_name = song_label(song_name, artist)
    ## replace spaces with underscores
    #with open(song_file_name, 'wb+') as f:
    #    f.write(resp.data)
    #resp.release_conn()



if __name__ == '__main__':
    main()