✍️ Handwritten Equation Solver using Deep Learning

A Streamlit Web App for Solving Handwritten Math Equations

📌 Overview

This project is an end-to-end handwritten equation solver built using a Convolutional Neural Network (CNN) and an interactive Streamlit web UI.
Users draw equations directly on a canvas, and the system:

Segments characters

Classifies them using the trained CNN

Reconstructs the equation

Computes the final result instantly

🚀 Features

✏️ Interactive drawing canvas

🧠 CNN model recognizing digits (0–9) + operators (+ − × ÷)

🔍 Contour-based character segmentation

🧮 Solves equations like: 23+7, 9-4, 7×8, 56÷7

⚡ Real-time prediction with bounding boxes

🌐 Clean, lightweight Streamlit UI

📂 Project Structure
app.py              # Streamlit UI  
predict.py          # Segmentation + CNN prediction  
cnn_model.h5        # Trained model  
Notebook.ipynb      # Training workflow  
requirements.txt    # Dependencies  
launch_app.bat      # Windows launcher  

🧠 How It Works
1️⃣ Character Segmentation

The app processes the drawn image by:

Converting to grayscale

Thresholding to binary

Finding contours

Sorting left → right

Cropping individual characters

Resizing to 32×32 for the model

(Implemented in predict.py)

2️⃣ CNN Classification

Each cropped character is classified as:

0–9, +, -, *, /

3️⃣ Equation Reconstruction

Characters are concatenated in order, e.g.:

Input → "2 3 + 8"
Output → "23+8"

4️⃣ Evaluation

The final equation is safely evaluated and returned to the user.

🖥️ Running the Web App
🔧 Install Dependencies
pip install -r requirements.txt

▶️ Start the App
streamlit run app.py


Windows users may also run:

launch_app.bat

📦 Requirements
tensorflow==2.20.0  
streamlit  
streamlit-drawable-canvas==0.9.3  
opencv-python  
numpy  
pandas  
matplotlib  
scikit-learn  
seaborn  

🏆 Model Performance
Model	Accuracy
CNN	~97.57%
RNN (experimental)	~76.32%
🙌 Acknowledgements

Dataset: Handwritten math symbol datasets (Kaggle + public sources)

Frameworks: TensorFlow • OpenCV • Streamlit

✨ Author

Shreyas Srivastava