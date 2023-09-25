from libraries import *
from api_key import *

def get_video_id(url):
    parsed_url = urllib.parse.urlparse(url)
    video_id = urllib.parse.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    return None

def generate_note_making(summary_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a note-making assistant."},
            {"role": "user", "content": summary_text},
        ],
        max_tokens=150,
        temperature=0.7,
        stop=None
    )
    return response.choices[0].message["content"].strip()

languages = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Telugu': 'te',
    'Marathi': 'mr',
    'Tamil': 'ta',
    'Urdu': 'ur',
    'Gujarati': 'gu',
    'Kannada': 'kn',
    'Odia': 'or',
    'Malayalam': 'ml',
    'Punjabi': 'pa',
}

st.title("YouTube Video Summarizer")

yt_video = st.text_input("Enter YouTube Video URL: [ex: https://www.youtube.com/watch?v=MS5UjNKw_1M]")

if yt_video:
    yt_vid = get_video_id(yt_video)

    if yt_vid is not None:
        st.video(yt_video)

        transcript = YouTubeTranscriptApi.get_transcript(yt_vid)

        result = ""
        for i in transcript:
            result += ' ' + i['text']

        summarizer = pipeline('summarization')

        cleaned_text = re.sub(r'[^A-Za-z\s]+', '', result)
        max_allowed_length = min(len(cleaned_text), 500)
        min_allowed_length = min(30, max_allowed_length - 1)

        num_iters = int(len(result) / 1000)
        sum_text = []
        for i in range(0, num_iters + 1):
            start = i * 1000
            end = (i + 1) * 1000
            out = summarizer(result[start:end], max_length=max_allowed_length, min_length=min_allowed_length,
                             do_sample=False)
            out = out[0]
            out = out['summary_text']
            sum_text.append(out)

        cleaned_text = re.sub(r'[^A-Za-z\s]+', '', str(sum_text))
        st.header("CC Text:")
        st.write(cleaned_text)

        text = cleaned_text

        max_allowed_length = min(len(text), 500)
        min_allowed_length = min(30, max_allowed_length - 1)

        summary = summarizer(text, max_length=max_allowed_length, min_length=min_allowed_length, do_sample=False)

        st.header("Summerized Text (Original):")
        st.write(summary[0]["summary_text"])

        selected_language = st.selectbox("Select Language for Translation", list(languages.keys()))

        selected_language_code = languages[selected_language]
        translator = GoogleTranslator(source='auto', target=selected_language_code)
        translation = translator.translate(summary[0]["summary_text"])

        st.header(f"Translated Summerized Text ({selected_language}):")
        st.write(translation)

        note_making = generate_note_making(summary[0]["summary_text"])

        st.header("Note-Making:")
        st.write(note_making)
    else:
        st.error("Invalid YouTube Video URL. Please provide a valid URL.")