import tkinter as tk
from tkinter import messagebox

# Caesar Cipher Functions
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            result += chr(shifted)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Playfair Cipher Functions
def prepare_text(text):
    return ''.join(filter(str.isalpha, text)).upper().replace("J", "I")

def generate_playfair_matrix(key):
    key = prepare_text(key)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = ''.join(dict.fromkeys(key + alphabet))
    matrix = [key[i:i+5] for i in range(0, 25, 5)]
    return matrix

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

def playfair_encrypt(plaintext, key):
    matrix = generate_playfair_matrix(key)
    encrypted_text = ""
    plaintext = prepare_text(plaintext)
    for i in range(0, len(plaintext), 2):
        pair = plaintext[i:i+2]
        if len(pair) == 1:
            pair += 'X'
        row1, col1 = find_position(matrix, pair[0])
        row2, col2 = find_position(matrix, pair[1])
        if row1 == row2:
            encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            encrypted_text += matrix[row1][col2] + matrix[row2][col1]
    return encrypted_text

def playfair_decrypt(ciphertext, key):
    matrix = generate_playfair_matrix(key)
    decrypted_text = ""
    for i in range(0, len(ciphertext), 2):
        pair = ciphertext[i:i+2]
        row1, col1 = find_position(matrix, pair[0])
        row2, col2 = find_position(matrix, pair[1])
        if row1 == row2:
            decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            decrypted_text += matrix[row1][col2] + matrix[row2][col1]
    return decrypted_text

# GUI
def process():
    mode = mode_var.get()
    if mode == "Encrypt":
        if cipher_var.get() == "Caesar":
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, caesar_encrypt(text_entry.get(), shift_var.get()))
        elif cipher_var.get() == "Playfair":
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, playfair_encrypt(text_entry.get(), key_entry.get()))
    elif mode == "Decrypt":
        if cipher_var.get() == "Caesar":
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, caesar_decrypt(text_entry.get(), shift_var.get()))
        elif cipher_var.get() == "Playfair":
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, playfair_decrypt(text_entry.get(), key_entry.get()))

root = tk.Tk()
root.title("Cipher GUI")

# Text Entry
text_label = tk.Label(root, text="Enter Text:")
text_label.grid(row=0, column=0, padx=5, pady=5)
text_entry = tk.Entry(root, width=50)
text_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

# Mode Selection
mode_var = tk.StringVar(value="Encrypt")
mode_label = tk.Label(root, text="Mode:")
mode_label.grid(row=1, column=0, padx=5, pady=5)
mode_menu = tk.OptionMenu(root, mode_var, "Encrypt", "Decrypt")
mode_menu.grid(row=1, column=1, padx=5, pady=5)

# Cipher Selection
cipher_var = tk.StringVar(value="Caesar")
cipher_label = tk.Label(root, text="Cipher:").grid(row=1, column=2, padx=5, pady=5)
cipher_menu = tk.OptionMenu(root, cipher_var, "Caesar", "Playfair")
cipher_menu.grid(row=1, column=3, padx=5, pady=5)

# Key Entry (For Playfair Cipher)
key_label = tk.Label(root, text="Key (Playfair only):")
key_label.grid(row=2, column=0, padx=5, pady=5)
key_entry = tk.Entry(root, width=50)
key_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

# Shift Entry (For Caesar Cipher)
shift_label = tk.Label(root, text="Shift (Caesar only):")
shift_label.grid(row=3, column=0, padx=5, pady=5)
shift_var = tk.IntVar(value=3)
shift_entry = tk.Entry(root, textvariable=shift_var)
shift_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

# Process Button
process_button = tk.Button(root, text="Process", command=process)
process_button.grid(row=4, column=1, padx=5, pady=5)

# Result Display
result_text = tk.Text(root, width=50, height=5)
result_text.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()

