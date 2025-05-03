Project 9: AI-Powered CRM for Real-World Networking (Personal CRM)

In today’s fast-paced professional world, remembering who you meet, where you met them, and what they do is a growing challenge—especially for networking-heavy environments like conferences, career fairs, and meetups. Project 9 solves this with a powerful AI-powered Personal CRM that turns your networking chaos into clarity.

The problem: People often leave events with dozens of business cards, LinkedIn profiles, and mental notes, only to forget names, roles, or connections a few days later. Manual tracking is inefficient, and existing CRMs are too bulky or impersonal for individual users.

The solution: This lightweight CRM lets users upload a screenshot of a video call, event attendee list, or even handwritten notes. An AI pipeline extracts names, predicts likely affiliations (e.g., MIT, Google), and dynamically generates contextual LinkedIn profiles—all visualized in a beautiful Streamlit frontend. For real-world accuracy, it even integrates SerpAPI to fetch live LinkedIn URLs, not just fake placeholders.

What works:

Dynamic text extraction and name parsing with deep learning (OCR + heuristics)

Smart organization guesser (e.g., “MIT” from domain or email)

Real-time LinkedIn URL lookup via Google Search API

Elegant Streamlit UI for fast CRM generation from any screenshot

Exportable records for follow-ups or future contact

Technologies used: Python, Streamlit, OpenCV, PyTesseract, SerpAPI, regex NLP heuristics, Torch, Docker.

## to run the application after requirements installation

``` Streamlit run frontend.py```
