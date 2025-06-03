# Hand_Classification_project
# Hand_Classification_project

"""
## 📌 Overview

This project is a simple hand detection system using *Python, **OpenCV, and **Mediapipe*.
It captures real-time video from the webcam and detects the hand landmarks such as fingers, palm center,
and calculates distance between specific landmarks.

It's useful for gesture recognition and can be extended to more complex applications like controlling UI with hand gestures
or sign language recognition.

---

## ⚙ Requirements

Before running the project, make sure to install the required libraries:
---

## ▶ How to Run

1. Open the notebook hand project.ipynb.
2. Run the cells step by step.
3. Make sure your webcam is working properly.
4. You’ll see a window showing the webcam feed with detected hand landmarks.

---

## 🛠 Problems Faced

While working on this project, I faced some *issues with the Mediapipe library*:

- *Laggy detection*: Sometimes, the hand detection was slow or unresponsive.  
  🔧 Solution: Reduced the frame resolution to improve performance.
  
- *Multiple hands not always detected*:  
  🔧 Solution: Set max_num_hands=2 explicitly and adjusted detection confidence.

- *Mediapipe installation issues* on some environments.  
  🔧 Solution: Created a virtual environment with compatible Python version (3.8–3.10 works best).

These problems were common but solvable with tweaking the model parameters and proper environment setup.

---

## 💡 Benefits & Applications

This project can be useful for:

- *Learning computer vision basics* with Python and OpenCV.
- Building *gesture-controlled applications*.
- Developing *assistive technologies* for people with disabilities.
- Experimenting with *AI-powered interactions* without needing physical buttons or touchscreens.

It's a good starting point for anyone interested in *Human-Computer Interaction (HCI)* or *AI in computer vision*.
"""


