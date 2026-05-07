# EggTrack - Hen Egg Production Tracker

A comprehensive Django application for tracking egg production from your laying hens.

## Features

- **Password Protection**: Secure login required for all access
- **Daily Egg Logging**: Input quantity for each hen (default 1)
- **Edit History**: Review and modify past entries with filters
- **Categorical Breeds/Colors**: Manage predefined characteristics
- **Enhanced Statistics**: Filterable stats by date range, hen, breed, and color
- **Hen Photos**: Upload and manage photos for each hen
- **Beautiful UI**: Custom SVG graphics and modern design

## Quick Start

### Using Docker Compose

```bash
# Start the application
docker-compose up -d

# Create a superuser for admin access
docker-compose exec web python manage.py createsuperuser

# Access the app at http://localhost:8000
```

### Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## Usage

### 1. Set Up Breeds and Colors
- Go to "Breeds" or "Colors" pages
- Add your flock's characteristics categorically

### 2. Add Hens with Photos
- Go to "Hens" page
- Click "Add New Hen"
- Enter name, select breed and color
- Upload a photo (recommended: 500x500px, JPG/PNG/GIF)

### 3. Update Hen Photos
- Go to "Hens" page
- Click on a hen's photo to upload/update

### 4. Daily Logging
- Go to "Daily Log" page
- Enter quantity for each hen (default is 1, editable 0-100)
- Click "Save Daily Log"

### 5. Edit History
- Go to "Edit History" page
- Filter by date, hen, breed, or color
- Update quantities or delete entries

### 6. Statistics
- Go to "Stats" page
- Select date range (7, 30, 90, or 365 days)
- Filter by specific hens, breeds, or colors
- View total eggs, days laid, and daily averages

## Admin Panel

Access `/admin/` with superuser credentials to manage all data, including users.

## Security

- All pages require authentication
- Password validators enforced
- CSRF protection enabled
- SQLite database for local storage

## File Uploads

- Photos are stored in `media/hens/`
- Supported formats: JPG, PNG, GIF
- Recommended size: 500x500 pixels
