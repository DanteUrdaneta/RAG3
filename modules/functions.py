from youtube_transcript_api import YouTubeTranscriptApi
import json




def getCaptions(videoID, filename):
    caps = YouTubeTranscriptApi.get_transcript(videoID)
    
    with open(filename, 'w') as f:
        for cap in caps:
            f.write(cap['text'] + '\n')


getCaptions("sVcwVQRHIc8?si=cnUDn7H2k8p3s-6L", 'test.txt')