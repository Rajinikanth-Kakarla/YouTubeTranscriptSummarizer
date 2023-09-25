import streamlit as st
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import re
from deep_translator import GoogleTranslator
import urllib.parse