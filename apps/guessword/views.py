import pandas as pd
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.encoding import smart_str
import unicodedata

# Load the dataset from the CSV file
def load_dataset():
    file_path = 'data/english_word_dataset.csv' 
    df = pd.read_csv(file_path, header=None)
    df.columns = ["mot_anglais", "mot_francais"]
    return df

# Return a random English word with possible translations
def get_random_word():
    df = load_dataset()
    random_row = df.sample(n=1).iloc[0]
    english_word = random_row["mot_anglais"]
    correct_translation = random_row["mot_francais"]
    
    # Choose 2 incorrect translations
    other_translations = df[df["mot_francais"] != correct_translation]["mot_francais"].sample(n=2).tolist()
    
    # Shuffle the translations to randomize the order
    all_choices = [correct_translation] + other_translations
    random.shuffle(all_choices)
    
    return english_word, all_choices, correct_translation

# Helper function to normalize text (remove accents, lowercase, etc.)
def normalize_text(text):
    # Remove accents and convert to lowercase
    text = unicodedata.normalize('NFD', text)  # Decompose characters to separate base and accent
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])  # Remove accents
    return text.lower().strip()

# API to fetch a word and its choices (via DRF)
class GetWordDataView(APIView):
    def get(self, request):
        english_word, choices, correct_translation = get_random_word()
        return Response({
            'english_word': english_word,
            'choices': choices,
            'correct_translation': correct_translation  
        }, status=status.HTTP_200_OK)


