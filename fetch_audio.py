import argparse
import logging
import datetime
import os

from bs4 import BeautifulSoup
from leg_audio_scrapping.lib.requests import web_get

logging.basicConfig(level=logging.INFO)


parser = argparse.ArgumentParser()
parser.add_argument('--uri', help='URI to a MN Legislative Media Archive page with audio. http(s):// and file:// URIs are supported.', required=True)
parser.add_argument('--dest', help='Path to a folder to save audio in. This folder must already exist.', required=True)


def get_file_page_uris(uri):
    """
    Fetches HTML of a page of links to File pages and returns an array of URIs to those File pages

    :param uri: URI to a page full of links to File pages
    :return: A list of URIs to pages with media files
    """

    page_response = web_get(uri)
    soup = BeautifulSoup(page_response.text, features='html.parser')
    return [link.get('href') for link in soup.select('div#audio_results table a')]


def get_audio_uris(uri):
    """
        Fetches HTML of a File page and returns an array of URIs to the audio files on that page

        :param uri: URI to a File page full of audio players
        :return: A list of dictionaries with the date, index, and URI of audio files
        """

    page_response = web_get(uri)
    soup = BeautifulSoup(page_response.text, features='html.parser')

    # Assuming the first h2 of the page is always the date in MM/DD/YYYY format
    page_date = datetime.datetime.strptime(soup.find('h2').text, '%m/%d/%Y').date()

    return [{"date": page_date, "index": idx, "uri": audio.get('src')}
            for idx, audio in enumerate(soup.select('#ctl00_Main_Panel_audio audio'))]


def get_audio(audio_uri, dest_path):
    """
        Fetches the audio file referenced in the provided dictionary and saves it at the provided path.

    :param audio_uri:
    :param dest_path
    :return:
    """

    response = web_get(audio_uri)
    if response.status_code == 200:
        with open(dest_path, 'wb') as f:
            f.write(response.content)


def audio_dest_path(audio_date, date_index, dest_folder):
    """
    Constructs the full path to a destination file based on the provided date, index, and destination folder.

    E.g
            audio_dest_path(date(2021, 10, 09), 1, "~/files")
            "/home/USER/files/2021-10-09_1.mp3"

    :param audio_date:
    :param date_count:
    :param dest_folder:
    :return:
    """
    full_dest_folder = os.path.expanduser(dest_folder)
    filename = f'{audio_date.strftime("%Y-%m-%d")}_{date_index}.mp3'
    return os.path.join(full_dest_folder, filename)


if __name__ == '__main__':
    args = parser.parse_args()

    file_page_uris = get_file_page_uris(args.uri)
    # Create a flat array of audio URIs with dates
    audio_uris = [
        audio_uri
        for file_page_uri in file_page_uris
        for audio_uri in get_audio_uris(file_page_uri)
    ]

    total_audio_uris = len(audio_uris)
    logging.info(f'Audio files to download: {total_audio_uris}')

    for i, audio_dict in enumerate(audio_uris):
        logging.info(f'Getting file {i+1}/{total_audio_uris}')
        audio_file_dest = audio_dest_path(audio_dict['date'], audio_dict['index'] + 1, args.dest)
        get_audio(audio_dict['uri'], audio_file_dest)
