# pdf_ocr_gui.py  (White / Light UI Version)

import os
import io
import sys
import time
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# OCR libs
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

# Set your Tesseract path here
if getattr(sys, 'frozen', False):
    # Running from .exe
    base_path = sys._MEIPASS
    TESSERACT_PATH = os.path.join(base_path, "tesseract", "tesseract.exe")
    TESSDATA_PREFIX = os.path.join(base_path, "tesseract", "tessdata")
else:
    # Running normally
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR\tessdata"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
os.environ["TESSDATA_PREFIX"] = TESSDATA_PREFIX


# Try to import tkinterdnd2 for drag & drop
HAS_DND = False
DND_FILES = None
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES as _DND_FILES
    HAS_DND = True
    DND_FILES = _DND_FILES
except Exception:
    HAS_DND = False
    DND_FILES = None


cancel_flag = threading.Event()


class OCRGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("OCR Searchable PDF Maker")
        root.geometry("420x300")          # Reduced height (-5cm approx)
        root.configure(bg="#ffffff")      # WHITE UI
        root.resizable(False, False)

        self.pdf_path = None
        self.output_pdf = None
        self.start_time = None
        self.total_pages = 0

        # Header
        title = tk.Label(root, text="OCR Searchable PDF Maker",
                         fg="#000000", bg="#ffffff", font=("Segoe UI", 18, "bold"))
        title.pack(pady=(10, 4))

        # Select Area
        frame = tk.Frame(root, bg="#f2f2f2", bd=1, relief="solid", padx=10, pady=10)
        frame.pack(padx=12, fill="x")

        self.select_btn = tk.Button(frame, text="📄 Click to Browse",
                                    command=self.choose_file,
                                    font=("Segoe UI", 11),
                                    bg="#e6e6e6", fg="black", relief="flat")
        self.select_btn.grid(row=0, column=0, sticky="w", padx=(0, 6))

        self.path_label = tk.Label(frame, text="No file selected",
                                   fg="#555555", bg="#f2f2f2", anchor="w")
        self.path_label.grid(row=0, column=1, sticky="w")

        # Drag & drop hint
        dnd_text = "Drag & Drop supported" if HAS_DND else "Drag & Drop not available"
        self.dnd_label = tk.Label(root, text=dnd_text,
                                  fg="#555555", bg="#ffffff", font=("Segoe UI", 9))
        self.dnd_label.pack(pady=(4, 6))

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal",
                                        length=560, mode="determinate")
        self.progress.pack(pady=(6, 2))

        self.info_label = tk.Label(root,
                                   text="Progress: 0%   |   Time: 00:00 | Remaining: --:--",
                                   fg="#000000", bg="#ffffff", font=("Segoe UI", 10))
        self.info_label.pack(pady=(4, 2))

        # Buttons
        btn_frame = tk.Frame(root, bg="#ffffff")
        btn_frame.pack(pady=(4, 4))

        self.start_btn = tk.Button(btn_frame, text=" Start OCR ",
                                   bg="#0078ff", fg="white",
                                   font=("Segoe UI", 11), relief="flat",
                                   command=self.run_ocr_thread)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.cancel_btn = tk.Button(btn_frame, text=" Cancel ",
                                    bg="#ff3333", fg="white",
                                    font=("Segoe UI", 11), relief="flat",
                                    command=self.cancel_process)
        self.cancel_btn.grid(row=0, column=1, padx=10)

        # Footer
        self.footer = tk.Label(root,
                               text="Output will be saved in the same folder \n Designed By: Sunil Prajapati | Python Developer",
                               fg="#666666", bg="#ffffff", font=("Segoe UI", 9))
        self.footer.pack(side="bottom", pady=6)

        # Drag & Drop registration
        if HAS_DND:
            try:
                root.drop_target_register(DND_FILES)
                root.dnd_bind("<<Drop>>", self.drop_file)
            except Exception:
                pass

    # File dialog
    def choose_file(self):
        f = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if f:
            self.set_pdf_path(f)

    def drop_file(self, event):
        path = event.data.strip("{}")
        if path.lower().endswith(".pdf") and os.path.isfile(path):
            self.set_pdf_path(path)
        else:
            messagebox.showerror("Invalid", "Please drop a valid PDF.")

    def set_pdf_path(self, path):
        self.pdf_path = path
        self.path_label.config(text=os.path.basename(path), fg="black")
        folder = os.path.dirname(path)
        self.output_pdf = os.path.join(folder, "searchable_output.pdf")
        self.footer.config(text=f"Output: {os.path.basename(self.output_pdf)}")

    def cancel_process(self):
        cancel_flag.set()
        self.info_label.config(text="Cancel requested...")

    def run_ocr_thread(self):
        if not self.pdf_path:
            messagebox.showerror("Error", "Select PDF first.")
            return

        cancel_flag.clear()
        self.start_btn.config(state="disabled")
        self.progress["value"] = 0
        self.start_time = time.time()

        threading.Thread(target=self.start_ocr, daemon=True).start()

    def start_ocr(self):
        try:
            doc = fitz.open(self.pdf_path)
            searchable = fitz.open()
            total = len(doc)
            self.total_pages = total

            for i in range(total):
                if cancel_flag.is_set():
                    searchable.save(self.output_pdf)
                    self.post_done(True, self.output_pdf)
                    return

                page = doc.load_page(i)
                pix = page.get_pixmap(dpi=150)
                png_data = pix.tobytes("png")

                pil_img = Image.open(io.BytesIO(png_data)).convert("RGB")
                jpeg_buffer = io.BytesIO()
                pil_img.save(jpeg_buffer, format="JPEG", quality=60)
                jpeg_bytes = jpeg_buffer.getvalue()

                text_pdf = pytesseract.image_to_pdf_or_hocr(
                    Image.open(io.BytesIO(jpeg_bytes)), extension="pdf"
                )
                ocr_doc = fitz.open("pdf", text_pdf)
                ocr_page = ocr_doc.load_page(0)
                ocr_page.insert_image(ocr_page.rect, stream=jpeg_bytes)

                searchable.insert_pdf(ocr_doc)

                pct = int((i + 1) / total * 100)
                elapsed = int(time.time() - self.start_time)
                remaining = int(elapsed / (i + 1) * (total - i - 1)) if i > 0 else 0

                self.root.after(0, self._update_progress, pct, elapsed, remaining)

            searchable.save(self.output_pdf, deflate=True, clean=True)
            self.post_done(False, self.output_pdf)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))

    def _update_progress(self, pct, elapsed, remaining):
        self.progress["value"] = pct
        self.info_label.config(
            text=f"Progress: {pct}% | Time: {elapsed//60:02d}:{elapsed%60:02d} | Remaining: {remaining//60:02d}:{remaining%60:02d}"
        )

    def post_done(self, canceled, output_path):
        if not canceled:
            try:
                folder = os.path.dirname(output_path)
                if sys.platform.startswith("win"):
                    os.startfile(folder)
                elif sys.platform.startswith("darwin"):
                    subprocess.Popen(["open", folder])
                else:
                    subprocess.Popen(["xdg-open", folder])
            except:
                pass

            self.root.after(0, lambda: messagebox.showinfo("Done", f"Created:\n{output_path}"))
        else:
            self.root.after(0, lambda: messagebox.showinfo("Canceled",
                                                           f"Partial file saved:\n{output_path}"))

        self.root.after(1000, self.root.destroy)


def main():
    if HAS_DND:
        try:
            root = TkinterDnD.Tk()
        except:
            root = tk.Tk()
    else:
        root = tk.Tk()

    OCRGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
