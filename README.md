# POE Tracker

A Path of Exile economy tracker that monitors currency and divination card prices using live poe.ninja data. Built to help players identify price spikes and market trends in the current league.

## Features

- Live currency and divination card price tracking via poe.ninja API
- Spike detection comparing poe.ninja data against historical data
- Price history graphs for individual items
- Searchable item table with collapsible categories
- Email notifications for price alerts

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML
- **Data:** poe.ninja API
- **Deployed on:** Render

## How to Run Locally

1. Clone the repo
   git clone https://github.com/Dyceodeh101/POE-Tracker.git

2. Install dependencies
   pip install -r requirements.txt

3. Create a .env file in the root directory and add your email credentials
   EMAIL=your_email_here
   PASSWORD=your_password_here

4. Run the app
   app.py

5. Open your browser and go to http://localhost:5000

## Live Demo

https://poe-tracker.onrender.com