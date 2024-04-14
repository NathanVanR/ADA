import customtkinter as ctk
import cohere
import uuid
import os

# conversation_id is for conversation history to help with context
conversation_id = str(uuid.uuid4())

# call model co with api key
api_key = os.environ.get('COHERE_API_KEY')
co = cohere.Client(api_key=api_key)

# preamble is to help with better responses
preamble = "You are my AI assistant, ADA. You are named after the famous computer scientist, Ada Lovelace."

# this is the chat function
def chat(co, preamble, conversation_id, user_input):    # user input is a CTKEntry field
    message=user_input.get()    # .get() method receives text from CTKEntry field
    response = co.chat(message=message,
                    preamble=preamble,
                    conversation_id=conversation_id,
                    model="command-r")
    answer_text.configure(state="normal") # TextBox field is set to normal to allow changes to be made
    answer_text.insert(ctk.END,"User: {}\n".format(message)) 
    answer_text.insert(ctk.END,"ADA: {}\n\n".format(response.text))
    answer_text.configure(state="disabled") # reset TextBox state to "disabled" to disallow changes
    user_input.delete(0,'end')

# enables the 'enter' key to trigger chat function
def enter(event):
    chat(co, preamble, conversation_id, user_input)
    
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.geometry("600x600")
root.title("ADA") 

frame = ctk.CTkFrame(master=root)
frame.pack(pady=12, padx=10,fill="both", expand=True)

input_label = ctk.CTkLabel(master=frame, text="Hi, I'm ADA! Feel free to ask me anything.", font=("font3", 16))
input_label.pack(pady=6, padx=10)

user_input = ctk.CTkEntry(master=frame,placeholder_text="Question", font=("font3", 16), width=500)
user_input.pack(pady=6, padx=5)
user_input.bind('<Return>',enter)

submit_button = ctk.CTkButton(master=frame, text="Submit", font=("font3", 16), width=500, command=lambda: chat(co, preamble, conversation_id,user_input=user_input))
submit_button.pack(pady=12,padx=5)

answer_text = ctk.CTkTextbox(master=frame, width=500,corner_radius=10,wrap='word')
answer_text.configure(state="disabled") # set state to disabled to disallow users to edit output
answer_text.pack(pady=6,padx=5)

user_input.focus()

root.mainloop()