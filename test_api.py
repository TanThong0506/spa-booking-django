"""
API Testing Script
Tests all API endpoints to verify they are working correctly
"""
import requests

api_url = 'http://localhost:8000/api'
timeout = 5

def test_endpoint(name, method='GET', url_path='', data=None):
    """Test an API endpoint and print results"""
    try:
        url = f'{api_url}{url_path}'
        if method.upper() == 'GET':
            response = requests.get(url, timeout=timeout)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, timeout=timeout)
        
        status = '✅' if 200 <= response.status_code < 300 else '❌'
        print(f'{status} {name}: {response.status_code}')
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                payload = response.json()
                if isinstance(payload, dict):
                    print(f'   Keys: {list(payload.keys())[:5]}')
                elif isinstance(payload, list):
                    print(f'   Count: {len(payload)}')
            else:
                print('   Content-Type:', content_type)
        elif response.status_code == 401:
            print('   Requires authentication token/session')
        return response.status_code
    except Exception as e:
        print(f'❌ {name}: {str(e)}')
        return None

def main():
    print('=' * 60)
    print('SPA BOOKING API TEST SUITE')
    print('=' * 60)
    print()

    print('📚 API Documentation:')
    test_endpoint('OpenAPI Schema', url_path='/docs/schema/')
    test_endpoint('Swagger UI', url_path='/docs/swagger/')
    test_endpoint('ReDoc', url_path='/docs/redoc/')
    print()

    print('🔐 Authentication:')
    test_endpoint('Token Auth', url_path='/auth/token/', method='POST', data={'username': 'test', 'password': 'test'})
    print()

    print('👥 Profiles:')
    test_endpoint('List Profiles', url_path='/profiles/')
    test_endpoint('Get Current User Profile', url_path='/profiles/me/')
    test_endpoint('Get Employees', url_path='/profiles/employees/')
    print()

    print('💅 Services:')
    test_endpoint('List All Services', url_path='/services/')
    test_endpoint('List Active Services', url_path='/services/active/')
    test_endpoint('List Inactive Services', url_path='/services/inactive/')
    print()

    print('📅 Appointments:')
    test_endpoint('List Appointments', url_path='/appointments/')
    test_endpoint('My Appointments', url_path='/appointments/my_appointments/')
    test_endpoint('Statistics', url_path='/appointments/statistics/')
    test_endpoint('Today Appointments', url_path='/appointments/today/')
    test_endpoint('Upcoming Appointments', url_path='/appointments/upcoming/')
    test_endpoint('Pending Appointments', url_path='/appointments/pending/')
    print()

    print('=' * 60)
    print('TEST COMPLETE')
    print('=' * 60)


if __name__ == '__main__':
    main()
