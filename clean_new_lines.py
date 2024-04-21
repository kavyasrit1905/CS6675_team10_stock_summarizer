def clean_file(input_file, output_file):
    with open(input_file, 'r') as file:
        text = file.read()

    # Remove newline characters
    cleaned_text = text.replace('\n', '')

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

# Input and output file paths
input_file_path = 'text_old.txt'
output_file_path = 'text_new.txt'

# Clean the file
clean_file(input_file_path, output_file_path)
