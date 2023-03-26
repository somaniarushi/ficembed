import os
import tqdm
import json

def data_breakdown(input_file, output_file, character_file):
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            data.append(line)

    # A piece of dialogue looks like this:
    # BERTRAM.
    # And I in going, madam, weep o’er my father’s death anew; but I must
    # attend his majesty’s command, to whom I am now in ward, evermore in
    # subjection.

    # We want to extract the name of the speaker and the dialogue.
    # We want to ignore extraneous details like stage directions. Some extraneous details look like the following:
    # SCENE: Partly in France, and partly in Tuscany.
    # ACT II
    # Scene I. Paris. A room in the King’s palace.
    # Scene II. Rossillon. A room in the Countess’s palace.
    # Scene III. Paris. The King’s palace.
    # Scene IV. Paris. The King’s palace.
    # Scene V. Another room in the same.


    forbidden_words = ["ACT", "SCENE", "ENTER", "EXIT", "EXUENT", "FLOURISH"]
    cleaned_data = []
    chunk = []
    character_set = set()
    for i in tqdm.tqdm(range(len(data))):
        data_point = data[i]
        # print(data_point)
        if data_point == "\n":
            if len(chunk) >= 2:
                # Trim the datapoint
                chunk = [data_point.strip() for data_point in chunk]
                speaker = chunk[0]
                if any([word in speaker.upper() for word in forbidden_words]):
                    chunk = []
                    continue
                # Check if the first character is a capital letter and the last character is a period.
                if speaker[0].isupper() and speaker[-1] == ".":
                    dialogue = " ".join(chunk[1:])
                    cleaned_speaker = speaker[:-1].strip().upper()
                    character_set.add(cleaned_speaker)
                    cleaned_data.append(dict(
                        speaker=cleaned_speaker,
                        dialogue=dialogue
                    ))
            chunk = []
        else:
            chunk.append(data_point)

    print(len(cleaned_data))
    data_combine(cleaned_data, 'shakespeare_cleaned_combined.json')
    # Dump all of cleaned_data into a json file
    with open(output_file, 'w') as f:
        json.dump(cleaned_data, f)

    with open(character_file, 'w') as f:
        for character in character_set:
            f.write(character + "\n")

def data_combine(data, output_file):
    """
    For every consecutive pairs of speaker and dialogue, combine them into two dictionaries with speaker/listener/dialogue keys.
    Write these to the output file.
    """

    combined_data = []
    for i in tqdm.tqdm(range(len(data) - 1)):
        speaker = data[i]['speaker']
        dialog1 = data[i]['dialogue']
        dialog2 = data[i + 1]['dialogue']
        listener = data[i + 1]['speaker']
        combined_data.append(dict(
            speaker=speaker,
            listener=listener,
            dialogue=dialog1
        ))
        combined_data.append(dict(
            speaker=listener,
            listener=speaker,
            dialogue=dialog2
        ))

    with open(output_file, 'w') as f:
        json.dump(combined_data, f)

def data_cleaning(input_file, output_file):

    # Open the file in read mode
    with open(input_file, "r") as file:
        # Read the contents of the file
        contents = file.read()


    contents = contents[:100000]
    # Find all instances of the text to delete
    start_indices = []
    end_indices = []
    for i in tqdm.tqdm(range(len(contents))):
        if contents.upper().startswith("DRAMATIS PERSONAE", i):
            start_indices.append(i)
        if contents.upper().startswith("SCENE:", i):
            end_indices.append(i)

    # Iterate over the start indices and find the corresponding end index
    for start in tqdm.tqdm(start_indices):
        for end in end_indices:
            if end > start:
                # Delete the text between the starting and ending positions
                contents = contents[:start] + contents[end:]
                # Update the end_indices list to only include indices after the current end index
                end_indices = [i for i in end_indices if i > end]
                break

    # Save the updated contents to the file
    with open(output_file, "w") as file:
        file.write(contents)

if __name__ == "__main__":
    data_breakdown('shakespeare.txt', 'shakespeare_cleaned.json', 'characters.txt')
    # data_combine('shakespeare_cleaned.json', 'shakespeare_cleaned_combined.json')