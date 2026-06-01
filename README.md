# 🌾 Smart Agriculture Monitoring Platform

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.23-red.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 Overview

The **Smart Agriculture Monitoring Platform** is a comprehensive IoT-based solution that helps farmers optimize water usage and improve crop yield through real-time soil condition monitoring. The [...]

### 🎯 Problem Statement

Farmers often overwater or underwater crops due to lack of real-time soil condition monitoring, leading to:
- 💧 Water waste and increased costs
- 🌱 Reduced crop yield and quality
- 📉 Environmental damage from runoff
- ⏰ Inefficient use of farmer's time

### ✨ Our Solution

This platform provides data-driven irrigation decisions by:
- 📊 Continuously monitoring soil moisture, temperature, humidity, and rainfall
- 🧠 Providing intelligent, real-time irrigation recommendations
- 📈 Generating comprehensive farm health reports
- 🔌 Exposing easy-to-use REST APIs for integration with existing systems

---

## 🚀 Features

### Core Functionality
- 🌱 **Farm & Field Management** - Register multiple farms and fields with crop types
- 📊 **Sensor Simulation** - Realistic simulation of soil moisture, temperature, humidity, and rainfall
- 💧 **Smart Irrigation Recommendations** - Rule-based decisions considering soil moisture and recent rainfall
- 📈 **Farm Health Reports** - Comprehensive analytics with health scoring (0-100)
- 📉 **Analytics Dashboard** - High-level KPIs and time-series trends
- 🗄️ **Data Persistence** - All sensor readings stored in SQLite database
- 🔌 **RESTful APIs** - Well-documented endpoints for monitoring and control

### Intelligent Recommendation Logic

| Soil Moisture | Recent Rain | Recommendation | Action Required |
|---------------|-------------|----------------|-----------------|
| < 20% | Any | **Critical** | 🚨 Irrigate Immediately |
| 20-40% | < 5mm | **Dry** | ⏰ Schedule within 24h |
| 20-40% | > 5mm | **Dry but rain expected** | ⏸️ Wait & Monitor |
| 40-70% | Any | **Adequate** | ✅ No Action Needed |
| > 70% | Any | **Excessive** | 🛑 Reduce/Stop Irrigation |

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Modern web framework for building REST APIs |
| **SQLAlchemy** | ORM for database interactions |
| **SQLite** | Lightweight embedded database |
| **Pydantic** | Data validation and serialization |
| **Uvicorn** | ASGI server for high performance |
| **Pytest** | Comprehensive testing framework |

---

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step-by-Step Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/AbishekP-28/smart-agriculture-platform.git
cd smart-agriculture-platform
