def foo(to_print):
	print(f"Ciao, {to_print}!")

# Define the function to transform CoNLL-U to the specified format
def transform_conllu_to_vert(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        sentence_id = None  # initialise sentence tracking

        # Write the opening <doc> tag
        outfile.write("<doc>\n")

        for line in infile:  # iterate over each line in the file, stripping whitespace from each line to prep it for transformation
            line = line.strip()

            # Check if the line indicates a new sentence
            if line.startswith("# sent_id"):
                sentence_id = line.split('=')[1].strip()  # Extract the sentence ID
                outfile.write(f'<s id="{sentence_id}">\n')

            elif line.startswith("#"):
                # Skip all other lines starting with '#'
                continue

            elif line:
                # Process each word line (non-empty, non-comment line)
                fields = line.split('\t')
                word_data = [
                    fields[0],       # ID
                    fields[1],       # FORM
                    fields[2],       # LEMMA
                    fields[3],       # UPOS
                    fields[5],       # FEATS
                    fields[6],       # HEAD
                    fields[7]        # DEPREL
                ]
                outfile.write("\t".join(word_data) + "\n")

            else:
                # End of the sentence
                if sentence_id:
                    outfile.write("</s>\n")
                    sentence_id = None  # Reset for the next sentence

        # Ensure the last sentence is closed if it was opened
        if sentence_id:
            outfile.write("</s>\n")

        # Write the closing </doc> tag
        outfile.write("</doc>\n")