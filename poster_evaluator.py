import cv2
import pytesseract
import numpy as np
import os
import re

class CompetitionPosterJudge:
    def __init__(self, tesseract_cmd_path=None):
        if tesseract_cmd_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
            
        # Comprehensive CS & Engineering Dictionary
        self.academic_vocab = {
            "abstract", "introduction", "methodology", "architecture", "algorithm", 
            "database", "accuracy", "model", "hardware", "software", "flowchart", 
            "conclusion", "future", "results", "system", "data", "analysis",
            "implementation", "performance", "network", "machine", "learning", "ai",
            "interface", "user", "testing", "proposed", "design", "framework",
            "optimization", "integration", "module", "backend", "frontend", "api",
            "objective", "purpose", "overview", "procedure", "simulation"
        }

    def evaluate_aesthetics(self, gray_image):
        """Dimension 1: Visual Clarity & Crowding (Max 10 Marks)"""
        score = 0
        feedback = []

        # 1. Blur Check (Laplacian)
        variance = cv2.Laplacian(gray_image, cv2.CV_64F).var()
        if variance > 100:
            score += 4
            feedback.append("Excellent sharpness.")
        elif variance > 50:
            score += 2
            feedback.append("Slightly blurry but readable.")
        else:
            feedback.append("Poor sharpness (Blurry).")

        # 2. Contrast Check (Std Dev)
        std_dev = np.std(gray_image)
        if std_dev > 40:
            score += 3
            feedback.append("High contrast (Easy to read).")
        elif std_dev > 20:
            score += 1
            feedback.append("Average contrast.")

        # 3. Information Crowding (Edge Density)
        edges = cv2.Canny(gray_image, 50, 150)
        edge_density = (np.count_nonzero(edges) / edges.size) * 100
        
        if 5 <= edge_density <= 20: 
            score += 3
            feedback.append("Perfect UI/UX balance (Good whitespace).")
        else:
            feedback.append("Poster looks cluttered or too empty.")

        return score, " | ".join(feedback)

    def evaluate_structure(self, gray_image):
        """Dimension 2: Layout & Blocks Detection (Max 10 Marks) - SMART FIX"""
        score = 0
        
        # 1. Get image dimensions for dynamic scaling
        height, width = gray_image.shape
        total_area = height * width
        
        # 2. Mild blur to remove background noise
        blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
        
        # 3. Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # 4. SMALLER Kernel to prevent merging everything! (The Fix)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)) 
        dilated = cv2.dilate(edges, kernel, iterations=1) 
        
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 5. Dynamic Area Threshold (Block must be at least 0.5% of the poster)
        min_block_area = total_area * 0.005 
        
        valid_blocks = []
        for c in contours:
            area = cv2.contourArea(c)
            if area > min_block_area:
                valid_blocks.append(c)
                
        block_count = len(valid_blocks)

        # A standard academic poster has Title, Abstract, Intro, Methodology, Results, Conclusion, + Figures
        if 5 <= block_count <= 20:
            score = 10
            status = f"Excellent Structure ({block_count} distinct sections detected)."
        elif block_count > 20:
            score = 7
            status = f"Over-fragmented Structure ({block_count} sections - might be messy)."
        elif block_count >= 3:
            score = 5
            status = f"Basic Structure ({block_count} sections detected)."
        else:
            score = 2
            status = f"Poor Structure (Only {block_count} sections found)."

        return score, status

    def evaluate_academic_depth(self, gray_image):
        """Dimension 3: NLP & Lexical Density (Max 10 Marks)"""
        text = pytesseract.image_to_string(gray_image).lower()
        
        # Clean text (remove punctuation)
        words = re.findall(r'\b[a-z]{3,}\b', text) 
        total_words = len(words)
        
        if total_words < 50:
            return 0, "Insufficient text for academic evaluation."

        score = 0
        feedback = []

        # 1. Lexical Density
        unique_words = set(words)
        lexical_density = (len(unique_words) / total_words) * 100
        
        if lexical_density > 45:
            score += 5
            feedback.append(f"High Lexical Density ({lexical_density:.1f}%).")
        elif lexical_density > 30:
            score += 3
            feedback.append(f"Average Lexical Density ({lexical_density:.1f}%).")
        else:
            feedback.append(f"Low Lexical Density (Repetitive text).")

        # 2. Technical Vocabulary Match
        tech_words_used = [w for w in unique_words if w in self.academic_vocab]
        tech_count = len(tech_words_used)

        if tech_count >= 10:
            score += 5
            feedback.append(f"Strong Technical Vocabulary ({tech_count} keywords).")
        elif tech_count >= 5:
            score += 3
            feedback.append(f"Moderate Technical Vocabulary ({tech_count} keywords).")
        else:
            feedback.append(f"Weak Technical Vocabulary.")

        return score, " | ".join(feedback)

    def evaluate_poster(self, image_path):
        if not os.path.exists(image_path):
            return {"Error": "Image file not found!"}

        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Run the 3 Dimensions
        aes_score, aes_feed = self.evaluate_aesthetics(gray)
        str_score, str_feed = self.evaluate_structure(gray)
        acad_score, acad_feed = self.evaluate_academic_depth(gray)

        total_score = aes_score + str_score + acad_score

        # Generate the Official Juror Report
        report = {
            "Project File": os.path.basename(image_path),
            "-----------------------------------": "-----------------------------------",
            "1. Aesthetics & UI (10 Marks)": f"{aes_score}/10 -> {aes_feed}",
            "2. Structural Layout (10 Marks)": f"{str_score}/10 -> {str_feed}",
            "3. Academic Depth (10 Marks)": f"{acad_score}/10 -> {acad_feed}",
            "----------------------------------- ": "-----------------------------------",
            "FINAL POSTER SCORE": f"{total_score} / 30 Marks"
        }
        return report

# ==========================================
# RUN THE AI JUROR
# ==========================================
if __name__ == "__main__":
    # Aap ka exact Tesseract path
    windows_tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe\tesseract.exe' 
    
    judge = CompetitionPosterJudge(tesseract_cmd_path=windows_tesseract_path)
    
    # Yahan apni image ka naam likhein
    test_image = "sample_poster.jpg" 
    
    print("\n[AI JUROR] Analyzing Exhibition Poster... Please wait...\n")
    results = judge.evaluate_poster(test_image)
    
    print("=== INNOVARSITY OFFICIAL EVALUATION REPORT ===")
    for key, value in results.items():
        print(f"{key}: {value}")