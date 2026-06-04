# Inventory Management System

A web-based Inventory Management System developed using **Flask, PostgreSQL, HTML, CSS, JavaScript, and Chart.js**. The application helps organizations efficiently manage products, monitor inventory levels, track stock movements, generate reports, and visualize inventory data through an interactive dashboard.

## Features

* Add and manage products with unique SKU codes
* Real-time inventory tracking
* Stock IN and Stock OUT operations
* Transaction history management
* Low stock monitoring and alerts
* Interactive analytics dashboard
* Inventory visualization using Chart.js
* Export inventory reports as CSV
* Export transaction reports as CSV
* PostgreSQL database integration
* REST API based architecture

## Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js

### Backend

* Python
* Flask

### Database

* PostgreSQL
* pgAdmin

### Libraries

* psycopg2

## Project Architecture

```text
Frontend (HTML, CSS, JavaScript)
                │
                ▼
         Flask APIs (Python)
                │
                ▼
      PostgreSQL Database
                │
                ▼
 Dashboard, Reports & Analytics
```

## Project Modules

### Product Management Module

Allows users to add and manage products with unique SKU identifiers.

### Inventory Management Module

Tracks available stock quantities and maintains inventory records.

### Stock Update Module

Supports Stock IN and Stock OUT operations while automatically updating inventory levels.

### Transaction Management Module

Records every stock movement and maintains a complete transaction history.

### Analytics Dashboard Module

Displays inventory statistics, stock summaries, low-stock alerts, and graphical analytics using Chart.js.

### Report Generation Module

Generates downloadable CSV reports for inventory and transaction records.

## Database Structure

### Products Table

| Field | Description  |
| ----- | ------------ |
| id    | Product ID   |
| name  | Product Name |
| sku   | Product SKU  |

### Inventory Table

| Field      | Description       |
| ---------- | ----------------- |
| product_id | Product Reference |
| quantity   | Available Stock   |

### Transactions Table

| Field      | Description           |
| ---------- | --------------------- |
| id         | Transaction ID        |
| product_id | Product Reference     |
| type       | IN / OUT              |
| quantity   | Transaction Quantity  |
| created_at | Transaction Timestamp |

## APIs Implemented

| API Endpoint         | Method | Purpose                   |
| -------------------- | ------ | ------------------------- |
| /add-product         | POST   | Add a new product         |
| /update-stock        | POST   | Update inventory stock    |
| /inventory           | GET    | Fetch inventory data      |
| /transactions        | GET    | Fetch transaction history |
| /export-inventory    | GET    | Export inventory report   |
| /export-transactions | GET    | Export transaction report |
| /stats               | GET    | Dashboard statistics      |
| /reset               | POST   | Reset inventory data      |

## Key Functionalities

* Product Registration
* Inventory Tracking
* Stock Management
* Transaction Recording
* Dashboard Analytics
* Low Stock Monitoring
* CSV Report Export
* Database Integration
* REST API Communication

## Installation

### Clone Repository

```bash
git clone https://github.com/akshithagundaa/Inventory-management-system.git
cd Inventory-management-system
```

### Install Dependencies

```bash
pip install flask psycopg2
```

### Configure PostgreSQL

Create a PostgreSQL database and update credentials in:

```text
config.py
```

### Run Application

```bash
python app.py
```

### Open Browser

```text
http://127.0.0.1:5000
```

## Screenshots

* Dashboard
* Add Product Module
* Update Stock Module
* Inventory List
* Transaction History
* Inventory Analytics Chart
* Low Stock Monitoring
* Inventory CSV Report
* Transaction CSV Report
* PostgreSQL Database Tables

## Future Enhancements

* User Authentication
* Barcode Scanner Integration
* Supplier Management
* PDF Report Generation
* Email Notifications
* Inventory Forecasting
* Mobile Responsive Dashboard
* Cloud Deployment

## Learning Outcomes

This project demonstrates:

* Full Stack Web Development
* Flask API Development
* PostgreSQL Database Management
* CRUD Operations
* REST API Architecture
* Dashboard Design
* Data Visualization using Chart.js
* CSV Report Generation
* Frontend and Backend Integration

## Author

**Gunda Akshitha**

Inventory Management System built using Flask, PostgreSQL, JavaScript, and Chart.js for efficient inventory tracking, stock management, and reporting. 🚀
