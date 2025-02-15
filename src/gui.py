#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox
from sender import send_message
from receiver import receive_message
import matplotlib.pyplot as plt

def send_action(entry_message):
    message = entry_message.get()
    if not message:
        messagebox.showerror("Erro", "Por favor, insira uma mensagem para enviar.")
        return
    send_message(message)
    messagebox.showinfo("Sucesso", "Mensagem enviada com sucesso!")

def receive_action():
    encrypted_message, decoded_message, signal = receive_message()
    messagebox.showinfo("Sucesso", f"Mensagem recebida: {decoded_message}")
    show_signal(signal)

def show_signal(signal):
    plt.plot(signal)
    plt.title("Sinal Digital Recebido")
    plt.xlabel("Tempo")
    plt.ylabel("Amplitude")
    plt.show()

def create_gui():
    root = tk.Tk()
    root.title("2B1Q Sender/Receiver")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="Escolha uma ação:")
    label.pack(pady=5)

    send_button = tk.Button(frame, text="Enviar Mensagem", command=lambda: send_action(entry_message))
    send_button.pack(pady=5)

    receive_button = tk.Button(frame, text="Receber Mensagem", command=receive_action)
    receive_button.pack(pady=5)

    global entry_message
    entry_message = tk.Entry(frame, width=50)
    entry_message.pack(pady=5)
    entry_message.insert(0, "Digite sua mensagem aqui")

    root.mainloop()