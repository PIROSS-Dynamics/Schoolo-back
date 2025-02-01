import pandas as pd
import random
from django.http import JsonResponse
from django.shortcuts import render

# load csv with dataset
def load_dataset():
    file_path = 'data/english_word_dataset.csv' 
    df = pd.read_csv(file_path, header=None)
    df.columns = ["mot_anglais", "mot_francais"]
    return df

# return a random word from the data set with random et correct traduction
def get_random_word():
    df = load_dataset()
    random_row = df.sample(n=1).iloc[0]  
    english_word = random_row["mot_anglais"]
    correct_translation = random_row["mot_francais"]
    
    # take two other mis translation
    other_translations = df[df["mot_francais"] != correct_translation]["mot_francais"].sample(n=2).tolist()
    
    # randomize the order
    all_choices = [correct_translation] + other_translations
    random.shuffle(all_choices)
    
    return english_word, all_choices, correct_translation

# get a word and choices
def get_word_data(request):
    english_word, choices, correct_translation = get_random_word()
    return JsonResponse({
        'english_word': english_word,
        'choices': choices
    })


# verify the user choice
def check_translation(request):
    user_translation = request.GET.get('translation')
    _, _, correct_translation = get_random_word()  # On récupère la traduction correcte
    result = "correct" if user_translation == correct_translation else "incorrect"
    return JsonResponse({"result": result})
