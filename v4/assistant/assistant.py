from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI()

functions = []


# Function to read the prompt from the file
def read_prompt_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        print(f"File {file_path} does not exist.")
        return ""


# Path to the prompt file
prompt_file_path = "prompt.txt"

while True:
    # Prompt the user for input
    user_input = input(
        "Choose an option: Create Assistants (1), List Assistants (2), Delete Assistants (3), Quit (4): ")

    # Convert the input to an integer
    try:
        choice = int(user_input)
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 4.")
        continue

    # Execute different actions based on the user's choice
    if choice == 1:
        print("Create Assistants selected")

        # Read instructions from the prompt file
        instructions = read_prompt_from_file(prompt_file_path)

        assistant = client.beta.assistants.create(
            instructions=instructions,
            name="Luna",
            tools=functions,
            model="gpt-4o-mini",
        )
        print(assistant)

    elif choice == 2:
        print("List Assistants selected")
        # Example of listing assistants (implement the actual API call and processing)
        assistants = client.beta.assistants.list()
        print(assistants)
    elif choice == 3:
        print("Delete Assistants selected")
        # Example of deleting an assistant (implement the actual API call and processing)
        assistant_id = input("Enter the ID of the assistant to delete: ")
        response = client.beta.assistants.delete(assistant_id)
        print(response)
    elif choice == 4:
        print("Quit selected. Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
