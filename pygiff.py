from PIL import Image, ImageSequence, ImageTk
import tkinter as tk

def scale_and_center(image, screen_width, screen_height):
    img_width, img_height = image.size
    scale_ratio = min(screen_width / img_width, screen_height / img_height)
    new_width = int(img_width * scale_ratio)
    new_height = int(img_height * scale_ratio)
    image = image.resize((new_width, new_height), Image.LANCZOS)
    position = ((screen_width - new_width) // 2, (screen_height - new_height) // 2)
    return image, position

def display_image(filename):
    root = tk.Tk()
    root.attributes('-fullscreen', True, '-topmost', True)
    root.configure(bg='black')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    image = Image.open(filename)
    image, (position_x, position_y) = scale_and_center(image, screen_width, screen_height)
    image = ImageTk.PhotoImage(image)
    label = tk.Label(root, bd=0, highlightthickness=0, bg='black', image=image)
    label.place(x=position_x, y=position_y)
    root.update()

    def close_display():
        root.destroy()

    root.bind("<Escape>", lambda e: close_display())
    root.bind("<Key>", lambda e: close_display() if e.char.lower() == "z" else None)
    root.protocol("WM_DELETE_WINDOW", close_display)
    root.mainloop()

def display_animated_image(filename, duration=0):
    global root

    def update_image():
        nonlocal current_frame
        nonlocal elapsed_time

        img = frames[current_frame]
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo
        label.place(x=positions[current_frame][0], y=positions[current_frame][1])

        elapsed_time += frame_durations[current_frame]
        current_frame = (current_frame + 1) % len(frames)

        if duration == 0 or elapsed_time < duration * 1000:
            root.after(frame_durations[current_frame], update_image)
        else:
            root.destroy()

    root = tk.Tk()
    root.attributes('-fullscreen', True, '-topmost', True)
    root.configure(bg='black')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    img = Image.open(filename)
    frames = []
    frame_durations = []
    positions = []

    for frame in ImageSequence.Iterator(img):
        frame_durations.append(frame.info["duration"])
        frame, position = scale_and_center(frame, screen_width, screen_height)
        frames.append(frame)
        positions.append(position)

    label = tk.Label(root, bd=0, highlightthickness=0, bg='black')
    label.pack()

    current_frame = 0
    elapsed_time = 0

    def close_on_keypress(event):
        root.destroy()

    root.bind('<KeyPress>', close_on_keypress)

    update_image()
    root.mainloop()





# display_image("C:\\Users\\Luca\Desktop\\Programme\\autodarts-desktop\\autodarts-gif-images\\idle.jpg")
display_animated_image("example.gif", duration=0)
