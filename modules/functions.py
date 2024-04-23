from youtube_transcript_api import YouTubeTranscriptApi
import json




def getCaptions(videoID, filename):
    caps = YouTubeTranscriptApi.get_transcript(videoID)
    
    with open(filename, 'w') as f:
        for cap in caps:
            f.write(cap['text'] + '\n')


getCaptions("TATblk1LUQI?si=8Sy84UdCCleDkiZV", 'test.txt')
