# 🖼️ InnoVarsity: Poster AI Evaluator Module

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![Tesseract OCR](https://img.shields.io/badge/Tesseract-OCR-orange.svg)

## 📌 Overview
This repository contains the **Poster Analysis Module** for **InnoVarsity** (an AI-driven Science Fair Online Exhibition platform). 

Traditional academic posters are usually evaluated manually, which is prone to human bias and inconsistency. This Python-based AI module autonomously evaluates research posters (Panaflex) out of **30 Marks** based on three core dimensions: Visual Aesthetics, Structural Layout, and Academic Depth.

<img width="1918" height="1000" alt="image" src="https://github.com/user-attachments/assets/093f5928-ff67-4c42-a3d1-aad6748e4c51" />


## 📌 Output
<img width="1846" height="505" alt="image" src="https://github.com/user-attachments/assets/e7e2a8e1-8192-4d58-b3bf-c80da32014c2" />


## 🧠 Core Evaluation Metrics (The 3 Dimensions)

1. **Aesthetics & UI (10 Marks):**
   * **Blur Detection:** Uses `cv2.Laplacian` variance to ensure the poster is sharp and readable.
   * **Contrast Analysis:** Uses Standard Deviation (`np.std`) to check the color harmony between text and background.
   * **Information Crowding:** Uses Canny Edge Density to ensure a perfect balance between text, diagrams, and whitespace.

2. **Structural Layout (10 Marks):**
   * Instead of basic color thresholding, this module uses **Canny Edge Detection combined with Morphological Transformations (Dilation/Closing)**.
   * It dynamically calculates the area of the poster and counts distinct academic blocks (e.g., Abstract, Methodology, Results) regardless of the background color or gradient.

3. **Academic Depth & NLP (10 Marks):**
   * Uses **Tesseract OCR** to extract raw text from the image.
   * Calculates **Lexical Density** (ratio of unique words to total words) to evaluate the complexity of the English used.
   * Matches extracted text against a custom Computer Science/Engineering vocabulary dictionary to reject irrelevant or fake images.

## 📂 Project Structure
```text
POSTER_AI_MODULE/
│
├── poster_evaluator.py      # The main AI evaluation class and logic
├── sample_poster.jpg        # Sample academic poster for testing
├── poster3.jpg              # Additional test image
└── README.md                # Project documentation
