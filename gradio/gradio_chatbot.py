import gradio as gr
import requests


def send_message_to_api(message, chat_history):
    # Call your API endpoint with the user's message
    print("Sending message to chatbot:",message)
    payload = {"question": message}
    response = requests.post(f"http://127.0.0.1:8000/chat",json=payload,headers={"Content-Type": "application/json"})
    print(response)

    api_reply = response.text if response.status_code == 200 else "API Error"

    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": api_reply})

    return "", chat_history


with gr.Blocks() as demo:
    gr.Markdown("Federal Chatbot")
    chatbot = gr.Chatbot(
        label="Chat",
        type="messages",
        show_copy_button=True,
        avatar_images=(
            None,
            "https://static.langfuse.com/cookbooks/gradio/hf-logo.png",
        ),
    )
    prompt = gr.Textbox(
        max_lines=1,
        label="Chat message",
        placeholder="Enter your message"
    )
    prompt.submit(
        fn=send_message_to_api,
        inputs=[prompt, chatbot],
        outputs=[prompt, chatbot]
    )

if __name__ == "__main__":
    demo.launch(share=True, debug=True)