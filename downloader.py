import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from pytube import YouTube
import moviepy.editor as mp
import os
from PIL import Image, ImageTk
import threading

def download_video(url, path, convert_to, resolution, progress_var):
    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress = (bytes_downloaded / total_size) * 100
        progress_var.set(progress)

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        
        if convert_to == 'mp4':
            if resolution == "720p":
                stream = yt.streams.filter(file_extension='mp4', res='720p').first()
            else:
                stream = yt.streams.filter(file_extension='mp4', res='1080p').first()
        else:
            stream = yt.streams.filter(only_audio=True).first()
        
        video_path = stream.download(output_path=path)
        
        if convert_to == 'mp3':
            audio_path = os.path.splitext(video_path)[0] + '.mp3'
            video_clip = mp.AudioFileClip(video_path)
            video_clip.write_audiofile(audio_path, codec='libmp3lame')
            video_clip.close()
            os.remove(video_path)
            return audio_path
        else:
            return video_path
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def start_download():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Alerta", "Entre com um URL do YouTube.")
        return
    
    convert_to = format_var.get()
    resolution = resolution_var.get() if convert_to == 'mp4' else None
    path = filedialog.askdirectory()
    
    if not path:
        messagebox.showwarning("Alerta", "Favor selecionar uma pasta.")
        return
    
    progress_var.set(0)
    download_button.config(state=tk.DISABLED)
    
    def run():
        result = download_video(url, path, convert_to, resolution, progress_var)
        download_button.config(state=tk.NORMAL)
        if result:
            messagebox.showinfo("Sucesso", f"Arquivo baixado e convertido com sucesso!\nLocal: {result}")
    
    threading.Thread(target=run).start()

def on_format_change(*args):
    if format_var.get() == 'mp4':
        resolution_frame.place(relx=0.5, rely=0.45, relwidth=0.75, relheight=0.1, anchor='n')
    else:
        resolution_frame.place_forget()

# Configurando a janela principal do aplicativo
root = tk.Tk()
root.title("YouTube Downloader by GleAlves")
root.geometry("700x400")

# Definindo imagem de fundo
image_path = "D:/Projetos_Python/down-youtube/IA-Image.jpg"
bg_image = Image.open(image_path)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Adicionar widgets
frame = tk.Frame(root, bg='white', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

url_label = tk.Label(frame, text="YouTube URL:", font=('Arial', 12))
url_label.place(relwidth=0.3, relheight=1)

url_entry = tk.Entry(frame, font=('Arial', 12))
url_entry.place(relx=0.31, relwidth=0.69, relheight=1)

format_var = tk.StringVar(value='mp4')
format_var.trace('w', on_format_change)

format_frame = tk.Frame(root, bg='white', bd=5)
format_frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.1, anchor='n')

audio_radio = ttk.Radiobutton(format_frame, text="Audio (MP3)", variable=format_var, value='mp3')
audio_radio.place(relwidth=0.5, relheight=1)

video_radio = ttk.Radiobutton(format_frame, text="Video (MP4)", variable=format_var, value='mp4')
video_radio.place(relx=0.5, relwidth=0.5, relheight=1)

resolution_var = tk.StringVar(value='720p')
resolution_frame = tk.Frame(root, bg='white', bd=5)

resolution_label = tk.Label(resolution_frame, text="Resolução:", font=('Arial', 12))
resolution_label.place(relwidth=0.3, relheight=1)

resolution_option = ttk.Combobox(resolution_frame, textvariable=resolution_var, values=["720p", "1080p"], state='readonly')
resolution_option.place(relx=0.31, relwidth=0.69, relheight=1)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.place(relx=0.5, rely=0.6, relwidth=0.75, relheight=0.05, anchor='n')

download_button = tk.Button(root, text="Download", font=('Arial', 14), command=start_download)
download_button.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.1, anchor='n')

# Acionando a alteração do formato inicial para definir o estado inicial correto
on_format_change()

root.mainloop()