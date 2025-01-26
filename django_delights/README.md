# Django Delights

## Overview
Django Delights is a comprehensive inventory and sales management system designed specifically for restaurant operations. It empowers restaurant owners to efficiently manage ingredients, menu items, recipes, and track purchases. With built-in reporting and analytics, Django Delights simplifies decision-making and streamlines daily operations.

---

## Features
- **Inventory Management:**
  - Add, update, and delete ingredients.
  - Monitor ingredient quantities and costs.
- **Menu Management:**
  - Add, update, and delete menu items.
  - Associate recipes with menu items.
- **Recipe Management:**
  - Link ingredients to menu items with specified quantities.
  - Automatically calculate the cost of menu items based on recipes.
- **Sales Tracking:**
  - Record customer purchases.
  - Display sales in a paginated table with total sales calculations.
- **Dashboard:**
  - View financial summaries (revenue, cost, and profit).
  - Identify top-selling menu items with quantities sold.
  - Analyze financial performance with interactive charts.
- **Authentication:**
  - Secure login and logout for staff.
  - Role-based access control for internal pages.

---

## How It Works
1. **Ingredients:**
   - Add ingredients with details such as name, unit, price per unit, and available quantity.
2. **Menu Items:**
   - Define menu items with titles and prices.
3. **Recipes:**
   - Link ingredients and their quantities to menu items to define recipes.
   - Automatically calculate menu item costs based on associated recipes.
4. **Purchases:**
   - Record customer purchases along with quantities.
   - Deduct ingredient quantities based on the associated recipes.
5. **Dashboard:**
   - Gain insights into revenue, costs, and profits.
   - View top-selling menu items.
   - Analyze financial data using an interactive bar chart.

---

## Installation
### Prerequisites
- Python 3.9+
- Django 4.2+
- SQLite (default database) or any other supported database

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/django-delights.git
   cd django-delights
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
6. Access the application:
   Open `http://127.0.0.1:8000` in your browser.

---

## Usage
### Adding Ingredients
1. Navigate to the **Inventory** page.
2. Add new ingredients with details such as name, unit, price per unit, and quantity.

### Creating Menu Items
1. Navigate to the **Recipes** page.
2. Add a new menu item and define its recipe by linking ingredients.

### Recording Purchases
1. Use the **Home** page to place orders as a customer.
2. Enter the customer’s name and purchase quantities.

### Viewing Insights
1. Access the **Dashboard** to view:
   - Revenue, costs, and profit.
   - Top-selling menu items.
   - Financial summaries in an interactive chart.

---

## Licensing
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Push to your branch and submit a pull request.

---

## Contact
For questions or support, please contact:
- **Name:** Your Name
- **Email:** your.email@example.com
- **GitHub:** [your-username](https://github.com/your-username)
