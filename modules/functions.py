from youtube_transcript_api import YouTubeTranscriptApi
import PIL as Image
import pytesseract




def getCaptions(videoID, filename):
    caps = YouTubeTranscriptApi.get_transcript(videoID)
    
    with open(filename, 'w') as f:
        for cap in caps:
            f.write(cap['text'] + '\n')

def getImage(image):
    img = Image.open(image)
    return img

def getOCR(image):
    return pytesseract.image_to_string(image)
