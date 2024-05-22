from pytube import YouTube
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio
import librosa
import torch


def descargar_audio(url):
    youtube = YouTube(url)
    video= youtube.streams.filter(only_audio=True).first()
    video.download(output_path="/mnt/c/Users/marti/Desktop/", filename= "audio.mp3")

#URL del video de Youtube
url= 'https://www.youtube.com/watch?v=3hOP7qPDyI4'

#Descarga el audio del video de Youtube
descargar_audio(url)

# Load audio
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
(audio, _) = librosa.core.load('/mnt/c/Users/marti/Desktop/audio.mp3', sr=sample_rate, mono=True);
#(audio, _) = load_audio('/mnt/c/Users/marti/Desktop/audio.mp3', sr=sample_rate, mono=True)

# Transcriptor
transcriptor = PianoTranscription(device=device)    # 'cuda' | 'cpu'

# Transcribe and write out to MIDI file
transcribed_dict = transcriptor.transcribe(audio, '/mnt/c/Users/marti/Desktop/piano_roll.midi')