import cv2
from pyzbar import pyzbar
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import sys
from PIL import Image

def open_link(url):
    webbrowser.open(url)

# Function for read qr codes
def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)

        # Prompt user in a message box
        choice = messagebox.askyesno("Open Link", "Do you want to open this link?")
        if choice:
            open_link(barcode_info)

        with open("barcode_result.txt", mode='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
    return frame

#Function to handle the "Open from gallery" button click
def open_from_gallery():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image = cv2.imread(file_path)
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            read_barcodes(image)
        else:
            messagebox.showerror("Error", "Failed to load image!")

def convert_to_ico(input_path, output_path):
    image = Image.open(input_path)
    image.save(output_path)

def main():
   
    root = tk.Tk()
    root.title("QR Code Scanner")

     # Convert JPEG to ICO
    jpeg_path = "C:/MachineLearningProject/qrScanner/qrIcon.jpg"
    ico_path = "qrIcon.ico"
    convert_to_ico(jpeg_path, ico_path)

    root.iconbitmap(ico_path)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()


    window_width = int(screen_width * 0.2)  
    window_height = int(screen_height * 0.2)  
    window_x = (screen_width - window_width) // 2  
    window_y = (screen_height - window_height) // 2  

    root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    window_closed = False


    camera_window_closed = False

    # Function to handle the "Scan" button click
    def scan():
        camera = cv2.VideoCapture(0)
        nonlocal camera_window_closed
        while True:
            ret, frame = camera.read()
            if not ret:
                break

            frame = read_barcodes(frame)
            cv2.imshow('QR code reader', frame)

            key = cv2.waitKey(1)
            if key == 27 or cv2.getWindowProperty('Barcode/QR code reader', cv2.WND_PROP_VISIBLE) < 1:
                camera_window_closed = True
                break

        camera.release()
        cv2.destroyAllWindows()

    # Function to handle the main window close event
    def on_closing():
        nonlocal window_closed
        window_closed = True
        if not (camera_window_closed and not root.winfo_exists()):
            sys.exit()

    # GUI setup
    label = tk.Label(root, text="Choose an option:")
    label.pack(pady=10)

    button_upload = tk.Button(root, text="Upload from Gallery", command=open_from_gallery)
    button_upload.pack(pady=5)

    button_scan = tk.Button(root, text="Scan", command=scan)
    button_scan.pack(pady=5)

    # Bind the main window close event to on_closing function
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


if __name__ == '__main__':
    main()

