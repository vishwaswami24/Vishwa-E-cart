# Quick Reference Guide - Vishwa E-cart Improvements

## 🚀 Quick Start (3 Steps)

```bash
# 1. Navigate to project
cd vishwa

# 2. Run migrations
python manage.py makemigrations
python manage.py migrate

# 3. Start server
python manage.py runserver
```

## 📋 New Features at a Glance

| Feature | URL | User Required |
|---------|-----|---------------|
| Search Products | `/products?q=keyword` | No |
| Add Review | `/add_review/<product_id>` | Yes |
| Toggle Wishlist | `/toggle_wishlist/<product_id>` | Yes |
| View Wishlist | `/wishlist` | Yes |
| Contact Form | `/contact` (POST) | No |

## 🔑 Key Code Snippets

### Search Products (views.py)
```python
query = request.GET.get('q', '')
products = Product.objects.filter(
    Q(name__icontains=query) | 
    Q(brand__icontains=query),
    is_active=True
)
```

### Add to Wishlist (JavaScript)
```javascript
fetch('/toggle_wishlist/' + productId)
    .then(response => response.json())
    .then(data => {
        // Handle response
    });
```

### Display Ratings (Template)
```django
{% if product.average_rating > 0 %}
    <span>⭐ {{ product.average_rating|floatformat:1 }}</span>
{% endif %}
```

## 🗃️ New Models

### Review
- `product` (FK to Product)
- `user` (FK to User)
- `rating` (1-5)
- `comment` (TextField)
- `created_at` (DateTime)

### Wishlist
- `user` (FK to User)
- `product` (FK to Product)
- `added_at` (DateTime)

### ContactMessage
- `name`, `email`, `mobile`
- `message` (TextField)
- `created_at`, `is_read`

## 🎨 CSS Classes Added

```css
.spinner-overlay    /* Loading spinner */
.rating-input       /* Star rating input */
.fade-in           /* Fade in animation */
.text-gradient     /* Gradient text */
```

## 🔧 Admin Panel Access

```
URL: http://127.0.0.1:8000/admin

New Sections:
- Reviews
- Wishlists
- Contact Messages
```

## 📱 Testing URLs

```
Homepage:        http://127.0.0.1:8000/
Search:          http://127.0.0.1:8000/products?q=fan
Product Details: http://127.0.0.1:8000/product_details/1
Wishlist:        http://127.0.0.1:8000/wishlist
Contact:         http://127.0.0.1:8000/contact
```

## ⚠️ Common Issues & Fixes

### Issue: Migration errors
```bash
# Delete migrations and database
del db.sqlite3
rmdir /s vapp\migrations
mkdir vapp\migrations
echo. > vapp\migrations\__init__.py

# Recreate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Issue: Products missing stock/brand
```bash
python manage.py update_products
```

## 📊 Database Queries

### Get products with reviews
```python
Product.objects.filter(review__isnull=False).distinct()
```

### Get user's wishlist
```python
Wishlist.objects.filter(user=request.user).select_related('product')
```

### Get average rating
```python
product.review_set.aggregate(Avg('rating'))
```

## 🎯 Performance Tips

1. Use `select_related()` for foreign keys
2. Use `prefetch_related()` for reverse relations
3. Add database indexes for frequently queried fields
4. Enable caching for product listings
5. Compress images before upload

## 🔐 Security Checklist

- [x] CSRF tokens on all forms
- [x] User authentication checks
- [x] Input validation
- [x] SQL injection prevention
- [x] XSS protection

## 📝 Code Style

- Follow PEP 8 for Python
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused
- Use Django's built-in features

## 🎨 UI/UX Guidelines

- Bootstrap 5 classes
- Responsive design (mobile-first)
- Consistent color scheme
- Loading states for async operations
- User feedback for all actions

## 📞 Quick Commands

```bash
# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Check for issues
python manage.py check

# Shell access
python manage.py shell

# Update products
python manage.py update_products
```

## 🔄 Git Workflow

```bash
git add .
git commit -m "Added search, reviews, wishlist features"
git push origin main
```

---

**Need help? Check IMPROVEMENTS.md for detailed documentation!**
