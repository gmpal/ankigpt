import genanki
import openai
import time
import random

topic = input("Enter the topic of your Anki deck: ")

size = input("Enter the number of cards you want to add: ")

# OpenAI API key
key = input("Enter your OpenAI API key: ")
openai.api_key = key

completion = openai.ChatCompletion.create(
      model="gpt-4", 
      messages = [{"role": "system", "content" : 
                  """
                  I want to learn about """ + topic + """.
                  Condensate the topic into """ + size + """ questions and answers.
                  Then, build a python dictionary of """ + size + """ questions and answers about """ + topic + """.
                  Return only the python dictionary. No variable name, just the dictionary. 
                  Like this: {"question1": "answer1", "question2": "answer2", ...}, since I will parse the dictionary from the string.
                  """
                  
                  
                  }
      ]
    )

response = completion["choices"][0]['message']['content']
    
# Create a Model for our Anki deck
my_model = genanki.Model(
  random.randint(0,99999999),  # Some unique number
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

facts = eval(response)

# Generate Anki notes
notes = []
for q, a in facts.items():
    note = genanki.Note(
        model=my_model,
        fields=[q, a])
    notes.append(note)

# Create an Anki Deck and add the notes
my_deck = genanki.Deck(
  random.randint(0,99999999),  # Some unique number
  f'{topic} Anki Deck')

for note in notes:
    my_deck.add_note(note)

# Generate the Anki deck file
genanki.Package(my_deck).write_to_file(f'{topic}_deck.apkg')

print("Your Anki deck has been generated!")
