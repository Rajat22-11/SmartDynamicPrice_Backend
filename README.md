# Tekron 
## Part - 1 : Synthetic Product Dataset Generation 🚀


Welcome to the **Synthetic Product Dataset Generator**! This repository contains a Python script that creates a synthetic dataset simulating realistic product order data. Use this dataset for testing, analysis, or demonstration purposes.

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)

## Table of Contents

- [Overview](#overview)
- [Dataset Features](#dataset-features)
- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Repository Structure](#repository-structure)
- [Contributing](#contributing)

## Overview

This project generates a synthetic dataset with **10,000 entries**. Each entry represents an individual product order, complete with details such as pricing, discounts, margins, shelf life, stock levels, customer sentiment, and order timestamps.

## Dataset Features

Each record in the dataset includes the following fields:

- **Product Name**: e.g., "Sugar (1kg)", "Saffola Oil (1L)"
- **Category**: e.g., Grocery, Vegetables, Dairy, Fruits, Snacks, Biscuits
- **Location**: Randomly selected (e.g., Baner, Aundh, Kothrud, Viman Nagar, Wakad)
- **MRP**: Fixed Maximum Retail Price per product
- **Blinkit Price, Zepto Price, Instamart Price**: Prices generated around a discounted price (always below MRP)
- **Discount (%)**: A randomly applied discount (5% to 20%) on the MRP
- **Margin (%)**: A randomly generated margin (10% to 30%)
- **Festive/Seasonal Impact**: Seasonal effects (e.g., Diwali, Holi, Summer)
- **Delivery Distance (km)**: Randomly generated between 1.0 and 5.0 km
- **Shelf Life (days)**: Estimated based on product category (e.g., Grocery: 180-365 days)
- **Min Stock** and **Max Stock**: Realistic stock levels with Max Stock always greater than Min Stock
- **Final Price**: Calculated as the average of the three platform prices
- **Customer Sentiment**: Sentiment indicator (Positive, Negative, Neutral)
- **Time of Ordering**: Randomly generated order timestamp (`YYYY-MM-DD HH:MM:SS`)

## How It Works

- **Fixed MRP per Product:**  
  Each product has a constant MRP throughout the dataset.

- **Dynamic Pricing:**  
  Prices for Blinkit, Zepto, and Instamart are computed by applying a discount to the MRP, ensuring all platform prices remain below the MRP.

- **Additional Realistic Attributes:**  
  The script includes fields for product margin, shelf life (derived from the product category), stock levels, and a random order timestamp to enhance the realism of the dataset.

- **Randomized Data:**  
  Details such as location, festive impact, delivery distance, and customer sentiment are randomized to simulate real-world variability.

## Prerequisites

Make sure you have the following installed:

- **Python 3.x**
- **pandas** library  
  Install via:
  ```bash
  pip install pandas
