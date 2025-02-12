import SonarqubeClient
import ExcelHandlers
import os

if __name__ == "__main__":
    # Example lists
    app_ids = ['books-test']
    metrics = ['coverage', 'bugs', 'code_smells', 'vulnerabilities', 'security_hotspots']
    
    # Your SonarQube instance URL
    sonarqube_url = os.getEnv("SONAR_URL", "http://localhost:9000")
    auth_token = os.getEnv("SONAR_TOKEN")
    
    sonarqube_client = SonarqubeClient(sonarqube_url, auth_token)
    # Get the metrics
    results = sonarqube_client.get_sonarqube_metrics(app_ids, metrics)
    
    # Print results
    for app_id, metrics_data in results.items():
        print(f"\nMetrics for {app_id}:")
        for project_name, measures in metrics_data.items():
            print(f"\nProject: {project_name}")
            for metric, value in measures.items():
                print(f"  {metric}: {value}")
    
    # Export to Excel using static method
    ExcelHandlers.export_to_excel(results, metrics, "output.xlsx")