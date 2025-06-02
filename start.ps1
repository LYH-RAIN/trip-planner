# Check if Docker is installed
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker is not installed. Please install Docker first."
    exit 1
}

if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
}

# Create necessary directories
New-Item -ItemType Directory -Force -Path "logs"
New-Item -ItemType Directory -Force -Path "static"

# Check if .env file exists
if (!(Test-Path .env)) {
    Write-Host "No .env file found, using default configuration"
    @"
# MySQL Configuration
MYSQL_ROOT_PASSWORD=password
MYSQL_DATABASE=trip_planner
MYSQL_USER=trip_user
MYSQL_PASSWORD=trip_password
MYSQL_PORT=3306

# Nginx Configuration
NGINX_PORT=80

# Application Configuration
FLASK_ENV=production
SECRET_KEY=default_secret_key
JWT_SECRET_KEY=default_jwt_secret_key
AMAP_KEY=your_amap_key
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "Default .env file created. Please modify as needed."
}

# Start services
Write-Host "Starting Trip Planning System..."
docker-compose up -d

# Wait for services to start
Write-Host "Waiting for services to start..."
Start-Sleep -Seconds 10

# Check service status
Write-Host "Checking service status..."
docker-compose ps

Write-Host "Trip Planning System is now running!"
Write-Host "API access: http://localhost:$(if ($env:NGINX_PORT) { $env:NGINX_PORT } else { '80' })/api"
Write-Host "View logs: docker-compose logs -f" 