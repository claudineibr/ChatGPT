from revChatGPT.revChatGPT import Chatbot
import json

def get_input(prompt):
  # prompt for input
  lines = []
  print(prompt,end="")
  while True:
      line = input()
      if line == "":
          break
      lines.append(line)

  # Join the lines, separated by newlines, and print the result
  user_input = "\n".join(lines)
  #print(user_input)
  return user_input

if __name__ == "__main__":
    print("""
    ChatGPT - A command-line interface to OpenAI's ChatGPT (https://chat.openai.com/chat)
    Repo: github.com/acheong08/ChatGPT
    """)
    print("Type '!help' to show commands")
    print("Press enter twice to submit your question.\n")
    with open("config.json", "r") as f:
            config = json.load(f)
    chatbot = Chatbot(config)
    if 'session_token' in config:
        chatbot.refresh_session()
    
    from subprocess import Popen
    import sys

    while True:
        prompt = get_input("\nYou:\n")
        if prompt.startswith("!"):
            if prompt == "!help":
                print("""
                !help - Show this message
                !reset - Forget the current conversation
                !refresh - Refresh the session authentication
                !exit - Exit the program
                """)
                continue
            elif prompt == "!reset":
                chatbot.reset_chat()
                print("Chat session reset.")
                continue
            elif prompt == "!refresh":
                chatbot.refresh_session()
                print("Session refreshed.\n")
                # Save the new config
                with open("config.json", "w") as f:
                    json.dump(chatbot.config, f)
                continue
            elif prompt == "!exit":
                break
        import textwrap

        messages = []
        lines_printed=0

        try:
            print("Chatbot: ")
            for message in chatbot.get_chat_response(prompt, output="stream"):
                # Split the message by newlines
                message_parts = message.split('\n')

                # Wrap each part separately
                formatted_parts = []
                for part in message_parts:
                    formatted_parts.extend(textwrap.wrap(part, width=80))
                    for formatted_line in formatted_parts:
                        if (len(formatted_parts) > lines_printed+1):
                            print(formatted_parts[lines_printed])
                            lines_printed+=1
            print(formatted_parts[lines_printed])
        except Exception as e:
            print("Something went wrong!")
            print(e)
            continue


        arguments=list(sys.argv)
        del arguments[0]

        if len(arguments)>2:
            try:
                process.terminate()
            except NameError:
                print("")

            # Use `python3 ./revChatGPT.py say -v Samantha -r 600` to make a Mac speak the output
            # using the Samantha voice at 600 words per minute (about 3x)
            # or `python3 ./revChatGPT.py espeak -v en -s 600` to do something similar using espeak (untested)
            arguments.append('"' + response['message'] + '"')
            process = Popen(arguments)