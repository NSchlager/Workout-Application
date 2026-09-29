# Workout-Application

Workout & Nutrition Tracker

A full-stack web application for logging workouts and tracking nutrition, built with a Python/Flask backend and a C extension for performance-critical data aggregation. Includes a live barcode scanner that looks up product nutrition data automatically.

Features
Workout Logging — log exercises with sets, reps, and weight, saved to CSV
Stats Dashboard — filter workout history by exercise name and rep count, with summary stats (total logs, max weight, average weight)
Calorie Tracker — log meals and calories, with a searchable day-by-day history and running totals
Barcode Scanner — scan a product barcode with your camera (or upload a photo) to automatically look up its name and calorie info via the Open Food Facts API, then log it with one click
C-powered aggregation — core numeric aggregation (sums, averages) is implemented in C and called from Python via ctypes, as a hands-on exploration of native performance vs. pure Python
Tech Stack
Backend: Python, Flask
Data processing: C (compiled to a shared library, called via ctypes)
Storage: CSV files (workouts.csv, calories.csv)
Frontend: HTML, CSS, vanilla JavaScript
Barcode scanning: html5-qrcode
Nutrition data: Open Food Facts API
