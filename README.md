# My Piano Rank

# Overview
In the domain of music, the notion of difficulty in piano performance is multidimensional and personalized, varying greatly 
based on individual skill levels and experience. What may be challenging to one pianist could be easier for another, highlighting 
the subjectivity in assessing difficulty. To address this variability, we present our solution: A Personalized Piano Score Rating System.

# Project Description
This project aims to develop a web-based tool that allows users to input YouTube link of a piano piece, along with their subjective difficulty ratings.
Utilizing machine learning algorithms, our system will select some piano scores that align precisely with each user's specified criteria.
By integrating technology with musical exploration, our goal is to empower users in discovering piano pieces and enriching their music education experience.

# Data Source
We have utilized the Giant MIDI dataset for our generated rankings. GiantMIDI-Piano is a classical piano MIDI dataset contains 10,855 MIDI files of 2,786 composers. The curated subset by constraining composer surnames contains 7,236 MIDI files of 1,787 composers. GiantMIDI-Piano are transcribed from live recordings with a high-resolution piano transcription system.
(https://github.com/bytedance/GiantMIDI-Piano)

# Start Application
-Go to .\certs 

- Double click to pianomusic.com and install certificate.

- Run notepad as administrator.

- Navigate to route C:\Windows\System32\drivers\etc

- Set view to "All files" and open hosts.

- And write on the bottom of the file: 127.0.0.1 www.pianomusic.com, and save.

-Create a file named config.py in .\BackEnd\api and introduce: 
  
  import os
  GOOGLE_CLIENT_ID = 'ID_USER'
  GOOGLE_CLIENT_SECRET = 'PASSWORD'
  class Config:
      SECRET_KEY = os.environ.get('SECRET_KEY', '$\x14\x03#Rxa6\xc0\x90j\xd7p\t}\xc3r\xa3_\x11\xa6\xcd;\xff')
      SESSION_TYPE = 'filesystem'
      SESSION_FILE_DIR = '/api/sessions'
      SESSION_PERMANENT = False
      SESSION_USE_SIGNER = True


  /*************************************/

If error {exec entrypoint.sh doesn't exist} change entrypoint file format from CRLF to LF

To run the app:
    
    $ docker-compose build
    $ docker-compose up

URL: https://www.pianomusic.com:3000/

/*************************************/





