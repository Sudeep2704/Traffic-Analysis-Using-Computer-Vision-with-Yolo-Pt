# 🚦 Intelligent Traffic Monitoring and Collision Detection System

A real-time computer vision-based traffic monitoring system that detects vehicles, tracks motion, estimates speed, and identifies potential collisions using rule-based logic and deep learning.

---

## 📌 Project Overview

This project processes traffic surveillance video and performs:

- 🚗 Vehicle Detection using YOLOv8
- 🔄 Multi-Object Tracking (Centroid Tracker)
- ⚡ Speed Estimation (Pixel → km/h conversion)
- 🚨 Overspeed Detection
- 🚫 Wrong-Way Detection
- 💥 Collision Detection (Rule-Based)
- 📊 Traffic Density Estimation
- 📝 CSV-based Anomaly Logging

The system generates an annotated output video (`output.avi`) with real-time visual alerts.

---

## 🧠 System Architecture

Video Input  
↓  
YOLOv8 Vehicle Detection  
↓  
Centroid-Based Tracking  
↓  
Speed Calculation  
↓  
Anomaly Detection (Rule-Based)  
↓  
Annotated Output Video  

---

## 💥 Collision Detection Method (Current Implementation)

Collision detection in this project is implemented using **rule-based logic**.

It does NOT use a trained deep learning collision detection model.

The system detects potential collisions using:

### ❌ Rule-Based Logic
Collision detection is implemented using predefined conditions rather than learned patterns.

### ❌ Bounding Box Overlap Check
If two vehicle bounding boxes overlap significantly in a frame, the system flags:

> Possible Collision

This indicates spatial intersection between vehicles.

### ❌ Sudden Stop Logic
If a vehicle’s speed drops abruptly from high speed to near zero in a short time window, the system flags:

> Sudden Stop

This may indicate emergency braking or impact.

---

## 🤖 Deep Learning Components

The system uses:

- **YOLOv8 (Ultralytics)** for vehicle detection
- Optional: YOLOv8 Classification Model for accident detection
- Transfer learning using pretrained weights

---
