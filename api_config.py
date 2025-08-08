# API Configuration
# Update this URL with your actual Vercel deployment URL

# Your deployed Vercel URL (replace with your actual URL)
API_BASE_URL = "https://bajaj-hack0x6.vercel.app"  # Remove trailing slash

# API Endpoints
HEALTH_ENDPOINT = f"{API_BASE_URL}/api/v1/health"
BASIC_QUERY_ENDPOINT = f"{API_BASE_URL}/api/v1/hackrx/run"
DETAILED_QUERY_ENDPOINT = f"{API_BASE_URL}/api/v1/hackrx/run/detailed"

# Authentication
AUTH_TOKEN = "db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6"

# Headers for API requests
API_HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
