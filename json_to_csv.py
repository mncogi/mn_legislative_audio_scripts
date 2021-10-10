import csv
import json
import logging
import os
from datetime import timedelta

logging.basicConfig(level=logging.INFO)


def read_json_into_memory(path):
    """
    Loads the JSON at `path` and returns the parsed object.

    :param path:
    :return:
    """
    with open(path, 'r') as json_file:
        json_data = json_file.read()

    # SPX outputs JSON in a not-quite valid format. The file contains many valid JSON objects
    # concatenated together. So, to actually parse the valid JSON, we need to modify the read
    # in data to create a valid JSON array.

    # TODO Should find a more full-proof way trim the beginning of the file and to find where the concatenated
    # objects meet, but this works well enough.
    json_array_str = f'[{json_data[json_data.find("{"):].replace("}{", "},{")}]'

    return json.loads(json_array_str)


def write_json_to_csv(json_data, path):
    """
    Writes the provided JSON into a CSV. Each row will contain:
        * The filename of the recording
        * The time index of the transcription
        * The text of the transcription

    :param json_data:
    :param path:
    :return:
    """

    with open(path, 'w', newline='') as csvfile:
        fieldnames = ['audio_id', 'time_index', 'text']

        preped_for_csv_data = [{'audio_id': transcript['audio.input.id'],
                                'time_index': timedelta(milliseconds=(int(transcript['recognizer.recognized.result.offset'][transcript_index])/10000)),
                                'text': transcript['recognizer.recognized.result.text'][transcript_index]}
                               for transcript in json_data
                               for transcript_index in range(len(transcript['recognizer.recognized.result.text']))
                               ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for transcription in preped_for_csv_data:
            writer.writerow(transcription)


if __name__ == '__main__':
    logging.info("Loading JSON file")
    filepath = os.path.expanduser("~/leg_audio/output-all-continuous.json")  # TODO Make this a script argument
    transcriptions = read_json_into_memory(filepath)

    logging.info("Writing CSV")
    write_json_to_csv(transcriptions, os.path.splitext(filepath)[0] + '.csv')
