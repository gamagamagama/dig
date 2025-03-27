import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import time

class ImageVisualizer:
    def __init__(self, image_path, box_size=50):
        self.root = tk.Tk()
        self.root.title("Matching Visualizer")

        self.img = Image.open(image_path)
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas = tk.Canvas(self.root, width=self.img.width, height=self.img.height)
        self.canvas.pack()

        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        self.rect = None
        self.box_size = box_size
        
        self.root.update()

    def update_rectangle(self, x, y, color="red"):
        self.canvas.delete("match_rect")  # delete all previous rectangles with this tag
        self.rect = self.canvas.create_rectangle(
            x, y, x + self.box_size, y + self.box_size,
            outline=color, width=2,
            tags="match_rect"  # assign a tag to easily delete next time
        )
         # ~10ms delay for smoother redraw
        self.root.update()

        # time.sleep(0.00000001)  # adjust speed here

    def highlight_final(self, x, y):
        self.update_rectangle(x, y, color="green")
        time.sleep(0.5)

    def close(self):
        self.canvas.delete("all")
        self.root.destroy()
