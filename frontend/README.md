# Mushroom Classification, Identification and IoT based Cultivation

![Flutter](https://img.shields.io/badge/Flutter-%2302569B.svg?style=for-the-badge&logo=Flutter&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-00599C?style=for-the-badge&logo=onnx&logoColor=white)

A comprehensive mobile application and backend system designed for the advanced identification and classification of mushrooms, integrated with IoT-based monitoring for cultivation. This project leverages state-of-the-art Deep Learning models and modern mobile technologies to provide a seamless user experience for mushroom enthusiasts, researchers, and cultivators in Pakistan.

## 🌟 Key Features

### 🔍 Advanced Identification
- **Hierarchical Classification**: Uses a two-stage classification system (Main Class & Species) to improve accuracy.
- **215 Mushroom Species**: Trained to recognize a wide variety of mushrooms found in Pakistan and globally.
- **Real-time Camera Detection**: Scan mushrooms directly using your mobile camera for instant identification.

### 🌐 Dual Inference Modes
- **Online (FastAPI)**: High-performance cloud-based inference using an EfficientNet-B3 model.
- **Offline (ONNX Runtime)**: On-device inference support for identification in remote areas without internet connectivity.

### 🌡️ IoT Based Cultivation
- **Environmental Monitoring**: Designed to integrate with IoT sensors (DHT11/22, CO2 sensors) to monitor temperature and humidity.
- **Optimal Growth Guidance**: Providing cultivation insights based on identified species' requirements.

### 📱 User-Centric Design
- **Interactive Explore Screen**: Browse through the massive database of 215 mushroom species.
- **Saved Mushrooms**: Keep a history of your identified mushrooms for future reference.
- **Knowledge Base**: Detailed information on edible, poisonous, and medicinal mushrooms.

## 🏗️ Technical Architecture

### Frontend (Mobile App)
- **Framework**: Flutter (Dart)
- **Local Database**: SQFlite for offline data storage.
- **ML Integration**: `onnxruntime` for on-device model execution.
- **UI/UX**: Custom-designed themes with rich animations and responsive layouts.

### Backend (Model API)
- **Language**: Python
- **Framework**: FastAPI
- **Model**: EfficientNet-B3 (Transfer Learning)
- **Inference**: PyTorch

### AI Module
- **Dataset**: 3122+ images across 215 classes.
- **Hierarchy**: 
  - `Non_Poisnous_Edible`
  - `Non_Poisnous_Non_Edible`
  - `Poisnous_Non_Useable`
  - `Poisnous_Useable`

## 🚀 Getting Started

### Prerequisites
- Flutter SDK (>=3.0.0)
- Python (3.9+)
- Android Studio / VS Code

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ashir6129/Mushroom-Classification-Identification-and-IoT-based-Cultivation.git
   ```

2. **Frontend Setup**
   ```bash
   cd Main
   flutter pub get
   flutter run
   ```

3. **Backend Setup**
   ```bash
   cd model_api
   pip install -r requirements.txt
   python main.py
   ```

## 📊 Dataset Distribution
The model is trained on a diverse set of mushrooms including:
- **Edible**: Almond Mushroom, Chanterelle, Field Mushroom, Oyster Mushroom, etc.
- **Poisonous**: Deathcap, Destroying Angel, Fly Agaric, etc.
- **Medicinal**: Lions Mane, Turkey Tail, etc.

## 🛠️ Project Structure
- `lib/`: Flutter frontend source code.
- `model_api/`: FastAPI backend and model inference scripts.
- `Ai Module/`: Dataset processing notebooks and scripts.
- `Diagrams'/`: Project architecture and sequence diagrams.

---
Developed as a Final Year Project for mushroom classification and smart cultivation monitoring in Pakistan.
