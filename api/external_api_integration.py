from odoo import http
from odoo.http import request
import requests
import json

class ExternalAPIIntegration(http.Controller):

    @http.route('/api/get_component_prices', type='json', auth='public', methods=['POST'], csrf=False)
    def get_component_prices(self, **post):
        # This method should be implemented to interact with external APIs to fetch real-time prices.
        # The actual API endpoint, credentials, and parameters would depend on the third-party service provider.
        # Below is a mock implementation assuming a JSON-based REST API.

        # Replace 'api_endpoint' and 'api_key' with actual values provided by the component vendor.
        api_endpoint = "https://vendorapi.example.com/get_prices"
        api_key = "your_api_key_here"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        try:
            response = requests.post(api_endpoint, headers=headers, json=post)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': 'Unable to fetch component prices', 'status_code': response.status_code}
        except Exception as e:
            return {'error': str(e)}

    @http.route('/api/check_component_availability', type='json', auth='public', methods=['POST'], csrf=False)
    def check_component_availability(self, **post):
        # This method should be implemented to interact with external APIs to check the availability of components.
        # The actual API endpoint, credentials, and parameters would depend on the third-party service provider.
        # Below is a mock implementation assuming a JSON-based REST API.

        # Replace 'api_endpoint' and 'api_key' with actual values provided by the component vendor.
        api_endpoint = "https://vendorapi.example.com/check_availability"
        api_key = "your_api_key_here"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        try:
            response = requests.post(api_endpoint, headers=headers, json=post)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': 'Unable to check component availability', 'status_code': response.status_code}
        except Exception as e:
            return {'error': str(e)}