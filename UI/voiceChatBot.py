import gradio as gr
import requests
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
url = config['server']['url']
round = 1


def enable_submit():
    return gr.update(interactive=True)


def voice_chat(audio_input):
    if audio_input is None:
        return "No file uploaded.", None, gr.update(interactive=True)
    try:
        file = {'file': open(audio_input, 'rb')}
        resp = requests.post(url=url, files=file) 
        global round
        file_path = f'result{round}.mp3'
        round += 1
        with open(file_path, 'wb') as f:
            f.write(resp.content)
        return 'Done.', file_path, gr.update(interactive=False)
    except Exception as e:
        return f"Error: {str(e)}"

# Create the Gradio interface
def create_interface():
    with gr.Blocks(title="Llama3 powered voice chat bot", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            ### Llama3 Powered Voice Chat Bot
            
            Upload your audio file with questions or do a live recording of your questions

            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                audio_input_comp = gr.Audio(
                    label="Question", 
                    sources=["upload", "microphone"], 
                    type="filepath",
                    autoplay=True)

                submit_btn = gr.Button("Submit", variant="primary")

            with gr.Column(scale=1):
                outputBox = gr.Textbox(
                    label="Status",
                    lines=2,
                    interactive=False
                )
                audio_output_comp = gr.Audio(label="Answer", autoplay=True)
            
        
        # Connect the button to the function
        submit_btn.click(
            fn=voice_chat, 
            inputs=audio_input_comp, 
            outputs=[outputBox, audio_output_comp, submit_btn])

        audio_input_comp.clear(
            fn=enable_submit,
            outputs=submit_btn
        )

        gr.Markdown(
            """
            ---
            ### About
            This web interface uses:
            - **Ollama** for local LLM inference (llama3 model)
            - **Gradio** for the web UI
            """
        )

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)