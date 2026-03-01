@echo off
echo ========================================
echo Vishwa E-cart - Setup Improvements
echo ========================================
echo.

echo Step 1: Creating migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo Error creating migrations!
    pause
    exit /b %errorlevel%
)
echo.

echo Step 2: Applying migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error applying migrations!
    pause
    exit /b %errorlevel%
)
echo.

echo Step 3: Collecting static files...
python manage.py collectstatic --noinput
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo New features added:
echo - Product Search
echo - Reviews and Ratings
echo - Wishlist
echo - Stock Management
echo - Contact Form Backend
echo - Performance Improvements
echo.
echo Next steps:
echo 1. Update existing products with stock and brand info
echo 2. Access admin panel to manage new features
echo 3. Test the new functionality
echo.
echo Run 'python manage.py runserver' to start the server
echo.
pause
