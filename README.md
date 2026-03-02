# 🛒 Vishwa E-cart

<p align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

Vishwa E-cart is a **Django-based e-commerce platform** designed for selling electrical products such as fans, bulbs, and tubelights. It features user authentication, product browsing, shopping cart management, order placement, and secure payment processing via Razorpay.

---

<img width="1899" height="922" alt="Screenshot 2026-03-02 153207" src="https://github.com/user-attachments/assets/08f12e9d-7b7c-4e98-8e58-503a730fc0e9" />


## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **User Authentication** | Registration, login, logout, and profile management |
| 📦 **Product Catalog** | Browse products by category (Tubelight, Fan, Bulb) from top brands |
| 🔍 **Advanced Search** | Real-time search by product name, brand, and description |
| ⭐ **Reviews & Ratings** | Customers can rate and review products with 1-5 star ratings |
| ❤️ **Wishlist** | Save favorite products for later purchase |
| 🛒 **Shopping Cart** | Add, update quantity, and remove items from the cart |
| 📊 **Stock Management** | Real-time stock tracking and out-of-stock indicators |
| 📋 **Order Management** | Place orders, view order details, and track order history |
| 💳 **Payment Integration** | Secure payments using Razorpay |
| 📧 **Email Notifications** | Automated emails for order confirmations |
| 📝 **Contact Form** | Functional contact form with database storage |
| 📱 **Responsive Design** | Built with Bootstrap for mobile-friendly interface |
| ⚡ **Performance Optimized** | Lazy loading images, smooth animations, and optimized queries |

---

## 🛠️ Technologies Used

- **Backend**: Django (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Payment Gateway**: Razorpay
- **Email**: Django's built-in email system
- **Authentication**: Session-based (Django auth) + JWT (for REST API)

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Git

### Steps

1. **Clone the repository**
   
```
bash
   git clone https://github.com/vishwaswami24/Vishwa-E-cart.git
   cd Vishwa-E-cart/vishwa
   
```

2. **Create a virtual environment**
   
```
bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On Mac/Linux: source venv/bin/activate
   
```

3. **Install dependencies**
   
```
bash
   pip install -r requirements.txt
   
```

4. **Run migrations**
   
```
bash
   python manage.py makemigrations
   python manage.py migrate
   
```

5. **Create a superuser** (optional)
   
```
bash
   python manage.py createsuperuser
   
```

6. **Run the server**
   
```
bash
   python manage.py runserver
   
```

7. **Access the application**
   Open your browser and go to `http://127.0.0.1:8000/`

---

## 📁 Project Structure

```
Vishwa-E-cart/
├── vishwa/                 # Main Django project directory
│   ├── vishwa/            # Project settings
│   └── manage.py          # Django management script
├── vapp/                  # Django app
│   ├── models.py         # Database models
│   ├── views.py          # Views
│   ├── urls.py           # URLs
│   └── admin.py          # Admin configuration
├── templates/             # HTML templates
├── static/               # CSS, JS, and image files
├── media/                # Uploaded product images
└── README.md             # This file
```

---

## 📸 Screenshots

The application features a modern, responsive design with:
- Clean homepage with hero section
- Product grid with cards
- Shopping cart functionality
- User profile and order management

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">Vishwaswami</p>
