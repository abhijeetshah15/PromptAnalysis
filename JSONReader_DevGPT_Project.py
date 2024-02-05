import json
import pprint as pp
import pandas as pd

def check_if_developer_issue(title):
    # Define a list of keywords indicative of developer-related conversations
    developer_keywords = [
    'developer', 'coding', 'programming', 'software', 'bug', 'code',
    'java', 'python', 'javascript', 'c++', 'ruby', 'php', 'html', 'css',
    'openai', 'google', 'machine learning', 'artificial intelligence', 'neural network',
    'framework', 'algorithm', 'backend', 'frontend', 'api', 'cloud', 'database',
    'git', 'version control', 'docker', 'containerization', 'web development',
    'framework', 'library', 'data science', 'tensorflow', 'pytorch', 'natural language processing',
    'deep learning', 'api', 'automation', 'devops', 'agile', 'scrum', 'kanban',
    'android', 'ios', 'mobile development', 'react', 'vue', 'angular', 'node.js',
    'kotlin', 'swift', 'scala', 'typescript', 'jenkins', 'continuous integration',
    'angularjs', 'vue.js', 'reactjs', 'wordpress', 'drupal', 'phpstorm', 'visual studio code',
    'intellij', 'eclipse', 'amazon web services', 'azure', 'google cloud platform',
    'linux', 'unix', 'windows', 'macos', 'server', 'network', 'security', 'privacy',
    'chatbot', 'virtual reality', 'augmented reality', 'blockchain', 'cryptocurrency',
    'ethereum', 'solidity', 'crypto', 'java ee', 'spring framework', 'enterprise',
    'jquery', 'bootstrap', 'sass', 'less', 'agile methodology', 'startup', 'productivity',
    'api design', 'microservices', 'graphql', 'rest', 'soap', 'graphql', 'postman',
    'swagger', 'api gateway', 'serverless', 'microfrontend', 'microfrontend architecture',
    'frontend architecture', 'backend architecture', 'data architecture', 'server architecture',
    'full stack development', 'web server', 'load balancing', 'caching', 'monitoring',
    'logging', 'analytics', 'big data', 'data warehouse', 'data lake', 'etl', 'elasticsearch',
    'kibana', 'logstash', 'bash', 'shell scripting', 'python scripting', 'scripting language',
    'command line', 'command line interface', 'scripting', 'script', 'automation testing',
    'unit testing', 'integration testing', 'system testing', 'user acceptance testing',
    'performance testing', 'security testing', 'test-driven development', 'behavior-driven development',
    'software development life cycle', 'sdlc', 'agile manifesto', 'kanban board', 'scrum master',
    'product owner', 'sprint planning', 'retrospective', 'user story', 'epic', 'acceptance criteria',
    'continuous delivery', 'continuous deployment', 'feature toggle', 'dark launch', 'blue-green deployment',
    'canary release', 'ab testing', 'feature branch', 'main branch', 'master branch', 'versioning',
    'semantic versioning', 'release management', 'changelog', 'code review', 'pull request',
    'code refactoring', 'technical debt', 'code quality', 'code smells', 'clean code', 'design patterns',
    'object-oriented programming', 'functional programming', 'imperative programming',
    'declarative programming', 'software architecture', 'architectural patterns', 'mvc', 'mvvm',
    'dependency injection', 'singleton', 'factory pattern', 'observer pattern', 'command pattern',
    'proxy pattern', 'adapter pattern', 'strategy pattern', 'template method pattern', 'composite pattern',
    'iterator pattern', 'builder pattern', 'prototype pattern', 'abstract factory pattern',
    'state pattern', 'visitor pattern', 'chain of responsibility pattern', 'interpreter pattern',
    'mediator pattern', 'flyweight pattern', 'memento pattern', 'domain-driven design', 'ddd',
    'event sourcing', 'cqrs', 'hexagonal architecture', 'clean architecture', 'onion architecture',
    'scalability', 'high availability', 'fault tolerance', 'resilience', 'distributed systems',
    'microservices architecture', 'monolith', 'legacy code', 'legacy system', 'legacy application',
    'refactoring techniques', 'code organization', 'code documentation', 'software documentation',
    'technical documentation', 'api documentation', 'database design', 'data modeling', 'er diagram',
    'uml', 'unified modeling language', 'design document', 'software specification', 'requirement analysis',
    'use case', 'user experience', 'user interface', 'ux design', 'ui design', 'wireframe',
    'mockup', 'prototyping', 'user persona', 'customer journey map', 'user research',
    'usability testing', 'a/b testing', 'design thinking', 'agile ux', 'responsive design',
    'mobile-first design', 'cross-browser compatibility', 'web accessibility', 'color theory',
    'typography', 'layout design', 'grid system', 'responsive web design', 'user interface patterns',
    'material design', 'flat design', 'skeuomorphic design', 'dark mode', 'user engagement',
    'conversion rate optimization', 'seo', 'search engine optimization', 'google analytics',
    'data analytics', 'data visualization', 'dashboard', 'chart', 'graph', 'heatmap', 'pie chart',
    'bar chart', 'line chart', 'scatter plot', 'bubble chart', 'treemap', 'd3.js', 'plotly', 'matplotib', 'ChatGPT']

    # Check if any keyword is present in either the prompt or answer
    is_developer_issue = any(keyword.lower() in title or keyword.upper() in title or keyword.title() in title for keyword in developer_keywords)

    return is_developer_issue


JSON_FILE_FOLDER = "snapshot_20230727"
JSON_FILE_NAME = "20230727_195927_pr_sharings"
with open(f"DevGPT/{JSON_FILE_FOLDER}/{JSON_FILE_NAME}.json") as file:
    data = json.load(file)

data_dict = {
    "Titles": [],
    "Prompts": [],
    "Answers": []
}


for i in range(len(data["Sources"])):
    
    title = data['Sources'][i]["Title"]
    
    try:
        for j in range(len(data["Sources"][i]["ChatgptSharing"][0]["Conversations"])):
            
            prompt = data['Sources'][i]['ChatgptSharing'][0]['Conversations'][j]['Prompt']
            answer = data['Sources'][i]['ChatgptSharing'][0]['Conversations'][j]['Answer']

            
            if check_if_developer_issue(data['Sources'][i]["Title"]):
                data_dict["Titles"].append(f"{title} | {j:02}, {i+1}")  
                data_dict["Prompts"].append(prompt)
                data_dict["Answers"].append(answer)
                
    except:
        pass
   

df = pd.DataFrame.from_dict(data_dict)

sample_size = 100

random_sampling_data = df.sample(n=min(sample_size, len(df)), random_state=42)
random_sampling_data.to_csv(f"DevGPT/{JSON_FILE_FOLDER}/{JSON_FILE_NAME}.csv", index=False)