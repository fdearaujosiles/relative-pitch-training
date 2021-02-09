import numpy as np
import simpleaudio as sa
import json
from math import ceil, floor
from random import randint
import os

notes = []
note_list = ["C", "D", "E", "F", "G", "A", "B"]
with open('notes.json') as json_file: 
    notes = json.load(json_file)

def play_note(note, octave, duration=1, fs = 44100):
    
    if note == "Cb": octave -= 1
    try:
        frequency = floor(
            next(item for item in notes if 
                note in item["note"].split('/') and 
                item["octave"] == octave
            )['frequency']
        )
    except StopIteration:
        raise Exception(f'Note "{note}{octave}" was not found')

    ###################################################################
    ####     simple_audio tutorial, didn't understand a thing      ####
    ####         but tweaked it a little to make it better         ####
    ###################################################################

    # Generate array with duration*sample_rate steps, ranging between 0 and duration
    t = np.linspace(0, ceil(duration), ceil(duration * fs), False)
    # Generate a 440 Hz sine wave
    note = np.sin(frequency * t * 2 * np.pi)
    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)
    # Start playback
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    # Wait for playback to finish before exiting
    play_obj.wait_done()

def play():
    # fancy 80's header 
    os.system('cls')
    print("/////////////////////////////////////////////////")
    print("///                                           ///")
    print("///            music_teacher.py               ///")
    print("///           por Fernando Siles              ///")
    print("///                                           ///")
    print("/////////////////////////////////////////////////\n\n")
    second_note = {}
    # pick a random note in the scale
    second_note["note"] = note_list[randint(0,6)]
    # it sorts out if it wil be in the same octave or one lower (or one above if it's an 8th)
    second_note["octave"] = ([4,5] if second_note["note"] != "C" else [4,5,6])[randint(0,2)]

    interval = note_list.index(second_note["note"]) + 1
    if interval == 1:
        interval = 8 if second_note["octave"] == 6 else 1 if second_note["octave"] == 5 else 1
    elif second_note["octave"] == 4:
        interval *= -1

    play_note("C", 5)
    play_note(second_note["note"], second_note["octave"])
    
    def question(a):
        if a == "play again":
            play_note("C", 5)
            play_note(second_note["note"], second_note["octave"])
            return question(input("What's the interval between the two notes? (numbers only)\n"))
        return a

    ans = question(input("What's the interval between the two notes? (numbers only)\n"))

    if str(ans) == str(interval):
        print("Correct!\n")
    else:
        print("Wrong!", f"The correct answer would be {interval}\n")
        print(second_note)

    play_again = input("Play again?\n")
    if play_again == "y":
        play()

play()