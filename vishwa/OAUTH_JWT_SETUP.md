# OAuth + JWT Setup Guide for Vishwa E-cart

## Step 1: Install Required Packages
```bash
pip install -r requirements_oauth_jwt.txt
```

## Step 2: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 3: Create Site in Django Admin
1. Run server: `python manage.py runserver`
2. Go to: http://127.0.0.1:8000/admin/
3. Login with superuser credentials
4. Go to "Sites" section
5. Edit the existing site:
   - Domain name: `127.0.0.1:8000`
   - Display name: `Vishwa E-cart`
6. Save

## Step 4: Setup Google OAuth
1. Go to: https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable "Google+ API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Configure OAuth consent screen:
   - User Type: External
   - App name: Vishwa E-cart
   - User support email: your-email@gmail.com
   - Developer contact: your-email@gmail.com
6. Create OAuth Client ID:
   - Application type: Web application
   - Name: Vishwa E-cart
   - Authorized redirect URIs:
     * http://127.0.0.1:8000/accounts/google/login/callback/
     * http://localhost:8000/accounts/google/login/callback/
7. Copy Client ID and Client Secret

## Step 5: Add Google OAuth in Django Admin
1. Go to: http://127.0.0.1:8000/admin/
2. Go to "Social applications" → "Add social application"
3. Fill in:
   - Provider: Google
   - Name: Google OAuth
   - Client id: [paste from Google Console]
   - Secret key: [paste from Google Console]
   - Sites: Select "Vishwa E-cart" and move to "Chosen sites"
4. Save

## Step 6: Test OAuth Login
1. Go to login page: http://127.0.0.1:8000/login
2. Click "CONTINUE WITH GOOGLE" button
3. Login with your Google account
4. You'll be redirected to products page

## JWT API Endpoints

### Get Access Token
```bash
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token
```bash
POST http://127.0.0.1:8000/api/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Use JWT Token in API Requests
```bash
GET http://127.0.0.1:8000/api/your-endpoint/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Features Added
✅ Google OAuth Login
✅ JWT Token Authentication
✅ Access Token (1 day validity)
✅ Refresh Token (7 days validity)
✅ Automatic token rotation
✅ API-ready authentication

## Security Notes
- Keep Client ID and Secret secure
- Use HTTPS in production
- Store tokens securely on client side
- Never commit secrets to version control
- Add `.env` file for production secrets

## Production Setup
For production, update settings.py:
```python
ALLOWED_HOSTS = ['yourdomain.com']

# Update redirect URIs in Google Console:
# https://yourdomain.com/accounts/google/login/callback/
```
