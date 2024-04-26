from tkinter import Tk, Label, Button, Text, filedialog
from PIL import Image, ImageTk
from cryptography.fernet import Fernet, InvalidToken

class SteganographyApp:
    def __init__(self, master):
        self.master = master
        master.title("Steganography App")

        self.label = Label(master, text="Enter Text:")
        self.label.pack()

        self.text_entry = Text(master, height=4, width=50)
        self.text_entry.pack()

        self.browse_button = Button(master, text="Browse Image", command=self.browse_image)
        self.browse_button.pack()

        self.hide_button = Button(master, text="Hide Message", command=self.hide_message)
        self.hide_button.pack()

        self.show_button = Button(master, text="Show Message", command=self.show_message)
        self.show_button.pack()

        self.quit_button = Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

        self.image_path = None

    def browse_image(self):
        self.image_path = filedialog.askopenfilename()
        self.show_image()

    def show_image(self):
        if self.image_path:
            image = Image.open(self.image_path)
            photo = ImageTk.PhotoImage(image)
            label = Label(image=photo)
            label.image = photo
            label.pack()

    def hide_message(self):
        if self.image_path:
            message = self.text_entry.get("1.0", "end-1c")
            steganography_image = self.hide_text_in_image(self.image_path, message)
            steganography_image.show()

    def show_message(self):
        if self.image_path:
            hidden_message = self.extract_text_from_image(self.image_path)
            if hidden_message:
                self.text_entry.delete(1.0, "end")
                self.text_entry.insert("end", hidden_message)
            else:
                self.text_entry.delete(1.0, "end")
                self.text_entry.insert("end", "No hidden message found.")

    @staticmethod
    def hide_text_in_image(image_path, message):
        image = Image.open(image_path)
        pixels = list(image.getdata())
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        binary_message += '1111111111111110'  # Adding a delimiter

        index = 0
        for i in range(len(pixels)):
            pixel = list(pixels[i])
            for j in range(3):  # R, G, B channels
                if index < len(binary_message):
                    pixel[j] = int(format(pixel[j], '08b')[:-1] + binary_message[index], 2)
                    index += 1
            pixels[i] = tuple(pixel)

        steganography_image = Image.new(image.mode, image.size)
        steganography_image.putdata(pixels)
        return steganography_image

    @staticmethod
    def extract_text_from_image(image_path):
        image = Image.open(image_path)
        pixels = list(image.getdata())
        binary_message = ''

        for pixel in pixels:
            for value in pixel:
                binary_message += format(value, '08b')[-1]

        delimiter_index = binary_message.find('1111111111111110')
        if delimiter_index != -1:
            binary_message = binary_message[:delimiter_index]
            message = ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)])
            return message
        else:
            return None


if __name__ == "__main__":
    root = Tk()
    app = SteganographyApp(root)
    root.mainloop()
