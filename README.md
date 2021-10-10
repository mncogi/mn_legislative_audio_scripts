MN Legislative Reference Audio scripts
======================================

A small set of scripts to help in downloading all of the audio files from a search result of
https://www.lrl.mn.gov/media/index and turning Azure transcriptions into searchable CSVs.

## Scripts

### fetch_audio.py

This will visit a provided search result page from the MN Legislative Reference Library site and download audio
from all of the results on the page. 

    # View help and arguments
    python fetch_audio.py -h

    # Example
    python fetch_audio.py --uri https://www.lrl.mn.gov/media/index?body=house&sess=91&comm=all&d1=&d2=&y=&video=y&audio=y --dest ~/leg_audio

### json_to_csv.py

Converts the JSON that the below Azure SPX Speech to Text command produces into a CSV.

    # View help and arguments
    python json_to_csv.py -h

    # Example
    python json_to_csv.py --json_path ~/leg_audio/transcriptions.json

## Using SPX and Azure Speech to Text service

Azure Speech to Text can be used to get a rough transcription of audio files for a cost of $1 per hour of audio.
SPX is a CLI for using Azure's Speech services.

### Dependencies

 * [Azure Account with Speech to Text service](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/overview#try-the-speech-service-for-free)
   * A free tier can be used to become familiar with the Speech to Text service, but only will transcribe 5 hours of audio.
 * [SPX Installed](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-speech-to-text?tabs=linuxinstall&pivots=programmer-tool-spx)
   * Note that on Linux GStreamer must be installed to transcribe non-wav audio.
 
### Getting Transcriptions

This will request a transcription of every `.mp3` in the current directory and save the result in `transcriptions.json.
This JSON will include the transcribed text and the audio index within the file of when the transcribed audio occurred.

Transcription rate is approximately real-time. `--threads` sets the number of audio files to transcribe in parallel.

    spx recognize \
        --threads 20 \
        --continuous \
        --profanity raw \
        --output all recognized result offset \
        --output all file type json \
        --files "*.mp3" --format mp3 \
        --output all file transcriptions.json

#### Batch Transcriptions

For very large amounts of audio that are available via publicly accessible URLs or Azure storage, Batch transcriptions
can also be performed via SPX. See `spx help batch transcription` and
https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/batch-transcription .

### SPX Help

The best documentation I've found for SPX is `spx help`. Most commands and many arguments have help entries.

`spx help find --text "something"` can be used to search the SPX help entries.