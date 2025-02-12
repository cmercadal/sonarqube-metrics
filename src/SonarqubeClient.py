import requests
from typing import List, Dict
from Utilities import Utilities

class SonarqubeClient:
    def __init__(self, base_url, auth_token):
        if not base_url:
            raise ValueError("base_url cannot be empty")
        if not auth_token:
            raise ValueError("auth_token cannot be empty")
        self.base_url = base_url
        self.auth_token = auth_token

    def get_sonarqube_metrics(self, app_ids: List[str], metrics: List[str]) -> Dict:
        results = {}
        
        headers = {
            'Authorization': f'Basic {Utilities.token_to_base64(self.auth_token)}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        metrics_param = ','.join(metrics)
        
        for app_id in app_ids:
            search_url = f"{self.base_url}/api/components/search"
            search_params = {
                'q': app_id,
                'qualifiers': 'TRK'
            }
            
            search_response = requests.get(search_url, headers=headers, params=search_params)
            search_data = search_response.json()
            
            project_metrics = {}
            for project in search_data['components']:
                project_key = project['key']
                project_name = project['name']
                
                api_url = f"{self.base_url}/api/measures/component"
                params = {
                    'component': project_key,
                    'metricKeys': metrics_param
                }
                
                response = requests.get(api_url, headers=headers, params=params)
                data = response.json()
                
                measures = {}
                if 'component' in data and 'measures' in data['component']:
                    for measure in data['component']['measures']:
                        measures[measure['metric']] = measure['value']
                
                project_metrics[project_name] = measures
            
            results[app_id] = project_metrics

        return results

# Example usage:


    
