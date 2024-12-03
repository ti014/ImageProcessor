import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from processing.image_processor import ImageProcessor
from utils.file_utils import list_image_files
import os


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ImgProcessor")
        self.root.geometry("780x420")  # Increased height for better layout

        self.processor = ImageProcessor()
        self.cancelled = False  # Flag to track if the operation was cancelled

        self.create_widgets()

    def create_widgets(self):
        padding_options = {"padx": 10, "pady": 5}

        # Input folder
        tk.Label(self.root, text="Input Folder:").grid(
            row=0, column=0, sticky="e", **padding_options
        )
        self.input_entry = tk.Entry(self.root, width=50)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self.root, text="Browse", command=self.browse_input).grid(
            row=0, column=2, padx=5, pady=5
        )

        # Output folder
        tk.Label(self.root, text="Output Folder:").grid(
            row=1, column=0, sticky="e", **padding_options
        )
        self.output_entry = tk.Entry(self.root, width=50)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self.root, text="Browse", command=self.browse_output).grid(
            row=1, column=2, padx=5, pady=5
        )

        # Resize or Crop
        self.action_var = tk.StringVar(value="resize")
        tk.Radiobutton(
            self.root, text="Resize", variable=self.action_var, value="resize"
        ).grid(row=2, column=1, sticky="w")
        tk.Radiobutton(
            self.root, text="Crop", variable=self.action_var, value="crop"
        ).grid(row=2, column=2, sticky="w")

        # Target dimensions
        tk.Label(self.root, text="Target Size (Height x Width):").grid(
            row=3, column=0, sticky="w", **padding_options
        )
        self.width_entry = tk.Entry(self.root, width=10)
        self.width_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.width_entry.insert(0, "640")

        tk.Label(self.root, text="x").grid(
            row=3, column=1, padx=(100, 5), pady=5, sticky="w"
        )

        self.height_entry = tk.Entry(self.root, width=10)
        self.height_entry.grid(row=3, column=1, sticky="e", padx=5, pady=5)
        self.height_entry.insert(0, "640")

        # Checkbuttons
        self.rename_var = tk.BooleanVar()
        self.auto_rename_cb = tk.Checkbutton(
            self.root, text="Auto rename", variable=self.rename_var
        )
        self.auto_rename_cb.grid(row=4, column=2, sticky="w", padx=5, pady=10)

        # Detect Face checkbox
        self.detect_face_var = tk.BooleanVar()
        self.detect_face_check = tk.Checkbutton(
            self.root, text="Detect Face", variable=self.detect_face_var
        )
        self.detect_face_check.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Flip Image checkbox and entry
        self.flip_var = tk.BooleanVar()
        self.flip_check = tk.Checkbutton(
            self.root, text="Flip Image", variable=self.flip_var
        )
        self.flip_check.grid(row=5, column=1, sticky="w", padx=10, pady=5)

        tk.Label(self.root, text="Flip Axis (0: Vertical, 1: Horizontal):").grid(
            row=5, column=2, sticky="w", **padding_options
        )
        self.flip_axis_entry = tk.Entry(self.root, width=10)
        self.flip_axis_entry.grid(row=5, column=3, sticky="w", padx=5, pady=5)
        self.flip_axis_entry.insert(0, "1")

        # Rotate Image checkbox and entry
        self.rotate_var = tk.BooleanVar()
        self.rotate_check = tk.Checkbutton(
            self.root, text="Rotate Image", variable=self.rotate_var
        )
        self.rotate_check.grid(row=6, column=1, sticky="w", padx=10, pady=5)

        tk.Label(self.root, text="Rotate Angle (degrees):").grid(
            row=6, column=2, sticky="w", **padding_options
        )
        self.rotate_angle_entry = tk.Entry(self.root, width=10)
        self.rotate_angle_entry.grid(row=6, column=3, sticky="w", padx=5, pady=5)
        self.rotate_angle_entry.insert(0, "5")

        # Add Noise checkbox and entry
        self.noise_var = tk.BooleanVar()
        self.noise_check = tk.Checkbutton(
            self.root, text="Add Noise", variable=self.noise_var
        )
        self.noise_check.grid(row=7, column=1, sticky="w", padx=10, pady=5)

        tk.Label(self.root, text="Noise Level (0-100):").grid(
            row=7, column=2, sticky="w", **padding_options
        )
        self.noise_level_entry = tk.Entry(self.root, width=10)
        self.noise_level_entry.grid(row=7, column=3, sticky="w", padx=5, pady=5)
        self.noise_level_entry.insert(0, "2")

        # Process button
        self.process_button = tk.Button(
            self.root,
            text="Process Images",
            command=self.process_images,
            bg="blue",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        self.process_button.grid(row=8, column=1, columnspan=1, pady=20)

        # Cancel button
        self.cancel_button = tk.Button(
            self.root,
            text="Cancel",
            command=self.cancel_processing,
            bg="red",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        self.cancel_button.grid(row=8, column=2, pady=20)

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.root, orient="horizontal", length=400, mode="determinate"
        )
        self.progress_bar.grid(row=9, column=0, columnspan=3, pady=10, padx=10)

        # Status label
        self.status_label = tk.Label(self.root, text="", anchor="w", justify="left")
        self.status_label.grid(
            row=10, column=0, columnspan=3, sticky="w", padx=10, pady=5
        )

    def browse_input(self):
        path = filedialog.askdirectory()
        if path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)

    def process_images(self):
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter valid numeric values for dimensions."
            )
            return

        action = self.action_var.get()  # Whether to "crop" or "resize"
        rename_files = self.rename_var.get()
        detect_face = self.detect_face_var.get()
        flip_image = self.flip_var.get()
        rotate_image = self.rotate_var.get()
        add_noise = self.noise_var.get()

        try:
            flip_axis = int(self.flip_axis_entry.get())
            rotate_angle = int(self.rotate_angle_entry.get())
            noise_level = int(self.noise_level_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numeric values for flip axis, rotate angle, and noise level.",
            )
            return

        if not input_path or not output_path:
            messagebox.showerror(
                "Error", "Please select both input and output folders."
            )
            return

        image_files = list_image_files(input_path)
        if not image_files:
            messagebox.showerror(
                "No Images", "No image files found in the input directory."
            )
            return

        # Disable the process button to prevent multiple clicks
        self.process_button.config(state="disabled")
        self.status_label.config(text="Starting processing...")

        # Reset cancel flag
        self.cancelled = False

        # Start the processing in a separate thread
        threading.Thread(
            target=self.process_images_thread,
            args=(
                input_path,
                output_path,
                width,
                height,
                action,
                rename_files,
                detect_face,
                flip_image,
                flip_axis,
                rotate_image,
                rotate_angle,
                add_noise,
                noise_level,
                image_files,
            ),
            daemon=True,
        ).start()

    def cancel_processing(self):
        # Set the flag to True to signal cancellation
        self.cancelled = True
        self.status_label.config(text="Cancelling...")
        self.process_button.config(state="normal")

    def process_images_thread(
        self,
        input_path,
        output_path,
        width,
        height,
        action,
        rename_files,
        detect_face,
        flip_image,
        flip_axis,
        rotate_image,
        rotate_angle,
        add_noise,
        noise_level,
        image_files,
    ):
        total_files = len(image_files)
        self.progress_bar["maximum"] = total_files
        self.progress_bar["value"] = 0

        for i, file in enumerate(image_files):
            if self.cancelled:
                self.update_status("Processing cancelled.")
                break

            image_path = os.path.join(input_path, file)
            result = self.processor.process_image(
                image_path,
                output_path,
                width,
                height,
                action,
                rename_files,
                detect_face,
                flip_image,
                flip_axis,
                rotate_image,
                rotate_angle,
                add_noise,
                noise_level,
            )
            self.update_status(result)
            self.progress_bar["value"] = i + 1

        if not self.cancelled:
            self.update_status("Processing complete.")
        self.process_button.config(state="normal")

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
