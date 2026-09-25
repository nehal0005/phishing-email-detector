# 🛡️ PHISHGUARD: AI-Powered Email Phishing Detector

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-red.svg" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/ML-Scikit--Learn-orange.svg" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/OCR-EasyOCR-green.svg" alt="EasyOCR">
  <img src="https://img.shields.io/badge/License-MIT-brightgreen.svg" alt="License">
</p>

**PhishGuard** is a desktop application that helps users analyze emails and screenshot images for phishing attempts, credentials harvest attacks, and malicious links in real-time.

Built with an intuitive **Crimson Red & Modern White** dashboard interface, it combines Machine Learning text classification with optical character recognition (OCR) to inspect both raw email text and image screenshots.

---

## 📸 User Interface Preview

<p align="center">
  <img src="gui_preview.png" alt="PhishGuard Interface" width="750">
</p>

---

## ✨ Key Features

* 📩 **Multi-Format Input:** Paste raw email text, upload screenshot images, or directly analyze clipboard screenshots.
* 👁️ **Built-in OCR Engine:** Automatically extracts and analyzes text from uploaded email screenshots using **EasyOCR**.
* 🤖 **Machine Learning Classifier:** Uses a **Random Forest Classifier** with TF-IDF Vectorization to identify malicious patterns.
* 📊 **Threat Confidence & Risk Breakdown:** Visual progress bar and detailed risk factors highlight specific suspicious keywords (`verify`, `suspended`, `password`, etc.) and malicious links.
* 🎨 **Modern Minimalist UI:** Clean light mode interface designed with **CustomTkinter** for an executive-grade experience.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **GUI Framework:** CustomTkinter
* **Machine Learning:** Scikit-Learn (RandomForestClassifier, TF-IDF Vectorizer)
* **Data Processing:** Pandas, NumPy
* **Image OCR:** EasyOCR, Pillow (PIL)

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/phishing-detector.git](https://github.com/your-username/phishing-detector.git)
cd phishing-detector
