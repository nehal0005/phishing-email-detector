import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from PIL import Image, ImageGrab
import customtkinter as ctk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Import EasyOCR safely
import easyocr

# ---------------------------------------------------------
# 1. PHISHING MODEL & EASYOCR ENGINE
# ---------------------------------------------------------
class PhishingDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=2000, stop_words='english')
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.reader = None  # Lazy loads EasyOCR when an image is uploaded
        self._train_model()

    def _train_model(self):
        data = [
            ("URGENT: Your account has been suspended! Verify your password now.", 1),
            ("Dear customer, update your banking details immediately to avoid fees.", 1),
            ("Congratulations! You won a $1000 gift card. Claim here.", 1),
            ("Security Alert: Unusual login attempt detected. Reset credentials.", 1),
            ("Final notice: Action required on your unpaid invoice.", 1),
            ("Are we still meeting for lunch today at 1 PM?", 0),
            ("Please review the project file attached for our meeting tomorrow.", 0),
            ("Here is the weekly report for your team.", 0),
            ("Thanks for sending the document. Talk to you later.", 0),
            ("Hi mom, I will be coming home around 7 PM.", 0)
        ]
        df = pd.DataFrame(data, columns=['text', 'label'])
        X = self.vectorizer.fit_transform(df['text'].str.lower())
        self.model.fit(X, df['label'])

    def predict(self, text):
        clean_text = text.lower()
        vec = self.vectorizer.transform([clean_text])
        prediction = self.model.predict(vec)[0]
        probs = self.model.predict_proba(vec)[0]
        confidence = probs[1] if prediction == 1 else probs[0]

        keywords = ['urgent', 'verify', 'suspended', 'banking', 'claim', 'password', 'login', 'invoice']
        found_words = [w for w in keywords if w in clean_text]
        
        if len(found_words) >= 2 and prediction == 0:
            prediction = 1
            confidence = 0.85

        return prediction, confidence, found_words

    def ocr_image(self, pil_img):
        if self.reader is None:
            self.reader = easyocr.Reader(['en'], gpu=False)

        temp_filename = "temp_uploaded_img.png"
        pil_img.save(temp_filename)
        
        try:
            results = self.reader.readtext(temp_filename, detail=0)
            return " ".join(results).strip()
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)


# ---------------------------------------------------------
# 2. WHITE & CRIMSON RED GUI
# ---------------------------------------------------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Light")
        self.COLOR_BG = "#F8F9FA"
        self.COLOR_PANEL = "#FFFFFF"
        self.COLOR_RED = "#D32F2F"         # Crimson Red
        self.COLOR_RED_HOVER = "#B71C1C"
        self.COLOR_GREEN = "#2E7D32"       # Safe Green
        self.COLOR_TEXT = "#212529"
        self.COLOR_MUTED = "#6C757D"
        self.COLOR_BORDER = "#DEE2E6"

        self.title("Phishing Email Detector")
        self.geometry("880 x 620")
        self.configure(fg_color=self.COLOR_BG)
        self.resizable(False, False)

        self.detector = PhishingDetector()
        self._create_ui()

    def _create_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=self.COLOR_PANEL, height=70, corner_radius=0, border_width=1, border_color=self.COLOR_BORDER)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title = ctk.CTkLabel(header, text="🛡️ PHISHGUARD", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.COLOR_RED)
        title.pack(side="left", padx=20, pady=15)

        subtitle = ctk.CTkLabel(header, text="Email Phishing & Threat Detector", font=ctk.CTkFont(size=12), text_color=self.COLOR_MUTED)
        subtitle.pack(side="left", pady=15)

        # Main Layout
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Left Frame
        left = ctk.CTkFrame(main, fg_color=self.COLOR_PANEL, corner_radius=10, border_width=1, border_color=self.COLOR_BORDER)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        lbl_input = ctk.CTkLabel(left, text="Input Email Content / Image", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.COLOR_TEXT)
        lbl_input.pack(anchor="w", padx=15, pady=(15, 5))

        # Buttons Bar
        btn_bar = ctk.CTkFrame(left, fg_color="transparent")
        btn_bar.pack(fill="x", padx=15, pady=5)

        upload_btn = ctk.CTkButton(btn_bar, text="📁 Upload Image", fg_color="#E9ECEF", hover_color="#CED4DA", text_color=self.COLOR_TEXT, width=120, command=self.upload_img)
        upload_btn.pack(side="left", padx=(0, 10))

        paste_btn = ctk.CTkButton(btn_bar, text="📋 Paste Image", fg_color="#E9ECEF", hover_color="#CED4DA", text_color=self.COLOR_TEXT, width=120, command=self.paste_img)
        paste_btn.pack(side="left")

        # Text Area
        self.txt_area = ctk.CTkTextbox(left, fg_color="#FAFAFA", text_color=self.COLOR_TEXT, border_width=1, border_color=self.COLOR_BORDER, corner_radius=6)
        self.txt_area.pack(fill="both", expand=True, padx=15, pady=10)

        # FIXED LINE BELOW: Changed italic=True to slant="italic"
        self.status_bar = ctk.CTkLabel(left, text="Upload an image or paste text to analyze.", font=ctk.CTkFont(size=11, slant="italic"), text_color=self.COLOR_MUTED)
        self.status_bar.pack(anchor="w", padx=15, pady=(0, 5))

        # Action Buttons
        act_bar = ctk.CTkFrame(left, fg_color="transparent")
        act_bar.pack(fill="x", padx=15, pady=(0, 15))

        btn_analyze = ctk.CTkButton(act_bar, text="ANALYZE", fg_color=self.COLOR_RED, hover_color=self.COLOR_RED_HOVER, text_color="white", font=ctk.CTkFont(weight="bold"), height=38, command=self.analyze)
        btn_analyze.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_clear = ctk.CTkButton(act_bar, text="Clear", fg_color="#E9ECEF", hover_color="#CED4DA", text_color=self.COLOR_TEXT, width=70, height=38, command=self.clear)
        btn_clear.pack(side="right")

        # Right Frame: Results
        right = ctk.CTkFrame(main, fg_color=self.COLOR_PANEL, width=300, corner_radius=10, border_width=1, border_color=self.COLOR_BORDER)
        right.pack(side="right", fill="both", padx=(10, 0))
        right.pack_propagate(False)

        lbl_res = ctk.CTkLabel(right, text="Detection Results", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.COLOR_TEXT)
        lbl_res.pack(anchor="w", padx=15, pady=(15, 10))

        # Status Card
        self.card = ctk.CTkFrame(right, fg_color="#FAFAFA", corner_radius=8, border_width=1, border_color=self.COLOR_BORDER)
        self.card.pack(fill="x", padx=15, pady=5)

        self.icon_lbl = ctk.CTkLabel(self.card, text="🔍", font=ctk.CTkFont(size=32))
        self.icon_lbl.pack(pady=(10, 2))

        self.status_lbl = ctk.CTkLabel(self.card, text="Awaiting Input", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.COLOR_MUTED)
        self.status_lbl.pack(pady=(0, 10))

        # Progress
        lbl_conf = ctk.CTkLabel(right, text="Threat Confidence", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.COLOR_TEXT)
        lbl_conf.pack(anchor="w", padx=15, pady=(15, 5))

        self.progress = ctk.CTkProgressBar(right, fg_color="#E9ECEF", progress_color=self.COLOR_RED, height=10)
        self.progress.pack(fill="x", padx=15)
        self.progress.set(0)

        self.conf_lbl = ctk.CTkLabel(right, text="0%", font=ctk.CTkFont(size=11), text_color=self.COLOR_MUTED)
        self.conf_lbl.pack(anchor="e", padx=15)

        # Risk Box
        lbl_risk = ctk.CTkLabel(right, text="Risk Factors", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.COLOR_TEXT)
        lbl_risk.pack(anchor="w", padx=15, pady=(15, 5))

        self.risk_box = ctk.CTkTextbox(right, fg_color="#FAFAFA", text_color=self.COLOR_MUTED, border_width=1, border_color=self.COLOR_BORDER, corner_radius=6, height=120)
        self.risk_box.pack(fill="x", padx=15, pady=(0, 15))
        self.risk_box.insert("1.0", "• Threat keywords and suspicious findings will show here.")
        self.risk_box.configure(state="disabled")

    def upload_img(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            try:
                img = Image.open(path)
                self._process_image(img)
            except Exception as e:
                messagebox.showerror("Image Error", f"Unable to open file: {e}")

    def paste_img(self):
        try:
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                self._process_image(img)
            else:
                messagebox.showinfo("Clipboard", "No image found in clipboard. Copy an image screenshot first.")
        except Exception as e:
            messagebox.showerror("Error", f"Clipboard error: {e}")

    def _process_image(self, img):
        self.status_bar.configure(text="⏳ Extracting text from image...", text_color=self.COLOR_RED)
        self.update_idletasks()

        extracted_text = self.detector.ocr_image(img)

        if extracted_text:
            self.txt_area.delete("1.0", "end")
            self.txt_area.insert("1.0", extracted_text)
            self.status_bar.configure(text="✅ Image text extracted successfully!", text_color=self.COLOR_GREEN)
            self.analyze()
        else:
            self.status_bar.configure(text="❌ No readable text found in image.", text_color=self.COLOR_RED)
            messagebox.showwarning("OCR Alert", "No clear text could be detected in this image.")

    def analyze(self):
        content = self.txt_area.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showwarning("Warning", "Please enter text or upload an image.")
            return

        is_phishing, conf, keywords = self.detector.predict(content)

        self.progress.set(conf)
        self.conf_lbl.configure(text=f"{int(conf * 100)}%")

        risks = []
        if "http" in content.lower() or "www." in content.lower():
            risks.append("• External Link Detected")
        if keywords:
            risks.append(f"• Suspicious Words: {', '.join(keywords)}")
        if not risks:
            risks.append("• No critical indicators found.")

        self.risk_box.configure(state="normal")
        self.risk_box.delete("1.0", "end")
        self.risk_box.insert("1.0", "\n".join(risks))
        self.risk_box.configure(state="disabled")

        if is_phishing == 1:
            self.card.configure(fg_color="#FFEBEE", border_color=self.COLOR_RED)
            self.icon_lbl.configure(text="⚠️")
            self.status_lbl.configure(text="PHISHING DETECTED", text_color=self.COLOR_RED)
            self.progress.configure(progress_color=self.COLOR_RED)
        else:
            self.card.configure(fg_color="#E8F5E9", border_color=self.COLOR_GREEN)
            self.icon_lbl.configure(text="✅")
            self.status_lbl.configure(text="LEGITIMATE EMAIL", text_color=self.COLOR_GREEN)
            self.progress.configure(progress_color=self.COLOR_GREEN)

    def clear(self):
        self.txt_area.delete("1.0", "end")
        self.progress.set(0)
        self.conf_lbl.configure(text="0%")
        self.card.configure(fg_color="#FAFAFA", border_color=self.COLOR_BORDER)
        self.icon_lbl.configure(text="🔍")
        self.status_lbl.configure(text="Awaiting Input", text_color=self.COLOR_MUTED)
        self.status_bar.configure(text="Upload an image or paste text to analyze.", text_color=self.COLOR_MUTED)
        
        self.risk_box.configure(state="normal")
        self.risk_box.delete("1.0", "end")
        self.risk_box.insert("1.0", "• Threat keywords and suspicious findings will show here.")
        self.risk_box.configure(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()