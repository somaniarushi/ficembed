
def data_extractor():
    """
    Extracts data from 'input.txt'. For every consecutive pair of dialogue,
    create a dictionary with "speaker 1", "speaker 2" and "dialogue" as keys.
    Append the dictionary to a list.
    """
    with open("input.txt", "r") as f:
        data = f.readlines()
    # Create a data array with every block of text, breaking at every new line.
    data = [x.strip() for x in data]
    # print(data[:100])

    cumulative = []
    cleaned_data = []
    for elem in data:
        if elem != '':
            cumulative += [elem]
        else:
            cleaned_data.append(cumulative)
            cumulative = []

    paired_data = []
    for i in range(0, len(cleaned_data) - 1, 2):
        dialog1 = cleaned_data[i]
        dialog2 = cleaned_data[i + 1]
        paired_data.append((dialog1, dialog2))

    dictionary = []
    characters = set()
    for pair in paired_data:
        # Skip ill-structured data.
        if (len(pair) < 2 or len(pair[0]) < 2 or len(pair[1]) < 2):
            continue
        # First, we extract both speakers
        speaker1 = pair[0][0].split(":")[0]
        speaker2 = pair[1][0].split(":")[0]

        characters.add(speaker1)
        characters.add(speaker2)

        # Then we extract each of their dialogues.
        # In case the dialogue spans multiple strings, we combine them
        # Remove any leading or trailing spaces
        dialog1 = "".join(pair[0][1:]).strip()
        dialog2 = "".join(pair[1][1:]).strip()

        dictionary.append(dict(
            speaker=speaker1,
            listener=speaker2,
            dialog=dialog1
        ))
        dictionary.append(dict(
            speaker=speaker2,
            listener=speaker1,
            dialog=dialog2
        ))
    print(len(dictionary))
    # Save the dictionary to a json file
    import json
    with open("data.json", "w") as f:
        json.dump(dictionary, f)

    # Save the characters in characters.txt
    with open('characters.txt', 'w') as f:
        f.write("\n".join(characters))
if __name__ == "__main__":
    data_extractor()