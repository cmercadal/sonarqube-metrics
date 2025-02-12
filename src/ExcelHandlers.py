from typing import Dict, List
import pandas as pd
import openpyxl

class ExcelHandlers:
    @staticmethod
    def export_to_excel(results: Dict, metrics: List[str], output_file: str = "sonarqube_metrics.xlsx"):
        """
        Export SonarQube metrics to Excel file, aggregating results by appId
        
        Args:
            results: Dictionary containing the metrics data
            metrics: List of metric names
            output_file: Name of the output Excel file
        """
        rows = []
        for app_id, projects_data in results.items():
            if isinstance(projects_data, list):  # Add type check
                print(f"Warning: Unexpected list for app_id {app_id}")
                continue
                
            if 'error' in projects_data:
                # Handle error cases
                row = {'appId': app_id}
                for metric in metrics:
                    row[metric] = 'N/A'
                rows.append(row)
            else:
                # Initialize aggregated metrics
                aggregated_metrics = {
                    'appId': app_id,
                    'sme': '',
                    'coverage': [],  # Will store all coverage values for averaging
                    'bugs': 0,
                    'code_smells': 0,
                    'vulnerabilities': 0,
                    'security_hotspots': 0
                }
                
                # Sum up all metrics across projects
                for project_name, metrics_data in projects_data.items():
                    for metric, value in metrics_data.items():
                        try:
                            if metric == 'coverage':
                                # Store coverage for averaging
                                aggregated_metrics[metric].append(float(value))
                            else:
                                # Sum up other metrics
                                aggregated_metrics[metric] += int(value)
                        except (ValueError, TypeError):
                            print(f"Warning: Could not process value '{value}' for metric '{metric}' in project '{project_name}'")
                
                # Calculate average for coverage
                if aggregated_metrics['coverage']:
                    aggregated_metrics['coverage'] = sum(aggregated_metrics['coverage']) / len(aggregated_metrics['coverage'])
                else:
                    aggregated_metrics['coverage'] = 'N/A'
                
                rows.append(aggregated_metrics)
        
        # Create DataFrame
        df = pd.DataFrame(rows)
        
        # Ensure columns are in the correct order
        columns = ['appId', 'sme'] + metrics
        df = df[columns]
        
        # Export to Excel
        df.to_excel(output_file, index=False)
        print(f"Data exported to {output_file}")