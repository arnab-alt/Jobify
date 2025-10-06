import requests
from config import RAPIDAPI_KEY
import time

def search_external_jobs(query, location, limit=20):
    """Search jobs from external API (JSearch) - LinkedIn, Indeed, Glassdoor, etc."""
    if not RAPIDAPI_KEY:
        return []
    
    url = "https://jsearch.p.rapidapi.com/search"
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    # Enhanced search query construction
    search_query = construct_search_query(query, location)
    
    params = {
        "query": search_query,
        "page": "1",
        "num_pages": "1",
        "date_posted": "all",
        "remote_jobs_only": "false"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        jobs = []
        for job in data.get('data', [])[:limit]:
            processed_job = process_job_data(job)
            if processed_job:
                jobs.append(processed_job)
        
        return jobs
    except requests.exceptions.Timeout:
        print(f"External API timeout for query: {query}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"External API error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error processing external jobs: {e}")
        return []

def construct_search_query(query, location):
    """Construct optimized search query for better results"""
    # Clean and optimize the query
    query_clean = query.strip()
    
    # Build search string
    if location and location != "All Countries":
        search_string = f"{query_clean} in {location}"
    else:
        search_string = query_clean
    
    return search_string

def process_job_data(job):
    """Process and standardize job data from API"""
    try:
        # Determine job source
        employer_name = job.get('employer_name', 'N/A')
        job_source = determine_job_source(job)
        
        # Build location string
        job_location = build_location_string(job)
        
        # Extract salary info
        salary_min = job.get('job_min_salary', 0)
        salary_max = job.get('job_max_salary', 0)
        
        # Handle salary conversion (if needed)
        if salary_min and salary_max:
            # Ensure reasonable salary range
            if salary_min > 1000000 or salary_max > 1000000:
                # Likely incorrect data
                salary_min = 0
                salary_max = 0
            
            # Convert hourly to annual if needed
            if salary_max < 500:  # Likely hourly rate
                salary_min = int(salary_min * 2080) if salary_min else 0
                salary_max = int(salary_max * 2080) if salary_max else 0
        
        # Extract skills from job description or highlights
        skills_required = extract_skills_from_job(job)
        
        # Get job description
        description = job.get('job_description', '')
        if not description:
            # Fallback to highlights if description is empty
            highlights = job.get('job_highlights', {})
            qualifications = highlights.get('Qualifications', [])
            responsibilities = highlights.get('Responsibilities', [])
            
            desc_parts = []
            if qualifications:
                desc_parts.append("Qualifications: " + "; ".join(qualifications[:3]))
            if responsibilities:
                desc_parts.append("Responsibilities: " + "; ".join(responsibilities[:3]))
            
            description = " ".join(desc_parts) if desc_parts else "No description available"
        
        # Truncate description
        if len(description) > 500:
            description = description[:500] + "..."
        
        return {
            'title': job.get('job_title', 'N/A'),
            'company': employer_name,
            'location': job_location,
            'description': description,
            'source': 'external',
            'job_source': job_source,
            'apply_link': job.get('job_apply_link', '#'),
            'salary_min': int(salary_min) if salary_min else 0,
            'salary_max': int(salary_max) if salary_max else 0,
            'employment_type': job.get('job_employment_type', 'Full-time'),
            'skills_required': skills_required
        }
    except Exception as e:
        print(f"Error processing job data: {e}")
        return None

def determine_job_source(job):
    """Determine the job board source"""
    job_apply_link = job.get('job_apply_link', '')
    
    # Check apply link for source
    source_mapping = {
        'linkedin.com': 'LinkedIn',
        'indeed.com': 'Indeed',
        'glassdoor.com': 'Glassdoor',
        'monster.com': 'Monster',
        'dice.com': 'Dice',
        'ziprecruiter.com': 'ZipRecruiter',
        'careerbuilder.com': 'CareerBuilder',
        'simplyhired.com': 'SimplyHired',
    }
    
    for domain, source_name in source_mapping.items():
        if domain in job_apply_link:
            return source_name
    
    # Fallback to job_publisher
    return job.get('job_publisher', 'JSearch')

def build_location_string(job):
    """Build location string from job data"""
    location_parts = []
    
    # Add city
    if job.get('job_city'):
        location_parts.append(job.get('job_city'))
    
    # Add state
    if job.get('job_state'):
        location_parts.append(job.get('job_state'))
    
    # Add country
    if job.get('job_country'):
        country = job.get('job_country')
        # Convert country codes to full names if needed
        country_map = {
            'US': 'USA',
            'GB': 'UK',
            'IN': 'India',
            'CA': 'Canada',
            'DE': 'Germany',
            'AU': 'Australia',
            'SG': 'Singapore',
            'AE': 'UAE',
            'NL': 'Netherlands',
            'FR': 'France',
            'JP': 'Japan',
            'CN': 'China',
            'ES': 'Spain',
            'IT': 'Italy',
            'BR': 'Brazil',
            'MX': 'Mexico',
            'CH': 'Switzerland',
            'SE': 'Sweden',
            'NO': 'Norway',
            'DK': 'Denmark'
        }
        country = country_map.get(country, country)
        location_parts.append(country)
    
    # Check for remote
    if job.get('job_is_remote'):
        location_parts.append('Remote')
    
    return ', '.join(location_parts) if location_parts else 'Location Not Specified'

def extract_skills_from_job(job):
    """Extract skills from job data with enhanced detection"""
    skills = []
    
    # Check if required_skills field exists
    if job.get('job_required_skills'):
        skills.extend(job.get('job_required_skills', []))
    
    # Extract from highlights
    highlights = job.get('job_highlights', {})
    qualifications = highlights.get('Qualifications', [])
    
    # Comprehensive skill patterns
    skill_keywords = [
        # Programming Languages
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Ruby', 'PHP',
        'Swift', 'Kotlin', 'Rust', 'Scala', 'Perl', 'R', 'MATLAB', 'Objective-C',
        
        # Frontend Frameworks
        'React', 'ReactJS', 'React.js', 'Angular', 'Vue', 'Vue.js', 'Svelte', 'Next.js',
        'Nuxt', 'Ember', 'Backbone', 'jQuery',
        
        # Backend Frameworks
        'Node.js', 'Django', 'Flask', 'Express', 'Spring', 'Spring Boot',
        'Laravel', 'Rails', 'Ruby on Rails', 'ASP.NET', '.NET', 'FastAPI',
        
        # Mobile
        'React Native', 'Flutter', 'Xamarin', 'Ionic', 'Android', 'iOS',
        
        # Cloud & DevOps
        'AWS', 'Azure', 'GCP', 'Google Cloud', 'Docker', 'Kubernetes', 'K8s',
        'Jenkins', 'CI/CD', 'Terraform', 'Ansible', 'CircleCI', 'GitLab CI',
        
        # Databases
        'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch',
        'Oracle', 'DynamoDB', 'Cassandra', 'Neo4j',
        
        # ML & Data
        'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Keras',
        'Scikit-learn', 'Pandas', 'NumPy', 'Spark', 'Hadoop', 'Tableau', 'Power BI',
        
        # Design Tools
        'Figma', 'Sketch', 'Adobe XD', 'Photoshop', 'Illustrator', 'InVision',
        
        # Other Tools
        'Git', 'GitHub', 'GitLab', 'Jira', 'Confluence', 'Slack',
        'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum',
        'HTML', 'CSS', 'Tailwind', 'Bootstrap', 'Sass', 'LESS'
    ]
    
    # Search in job title
    job_title = job.get('job_title', '')
    for keyword in skill_keywords:
        if keyword.lower() in job_title.lower() and keyword not in skills:
            skills.append(keyword)
    
    # Search in qualifications
    for qualification in qualifications:
        for keyword in skill_keywords:
            if keyword.lower() in qualification.lower() and keyword not in skills:
                skills.append(keyword)
    
    # Search in description (if available and not too long)
    description = job.get('job_description', '')
    if description and len(description) < 5000:  # Only search short descriptions
        for keyword in skill_keywords:
            # Use word boundary to avoid partial matches
            if f' {keyword.lower()} ' in f' {description.lower()} ' and keyword not in skills:
                skills.append(keyword)
    
    # Limit to 10 skills for better display
    return skills[:10]

def search_multiple_sources(query, location, max_results=50):
    """
    Search with multiple strategies to get maximum results
    """
    all_jobs = []
    
    # Strategy 1: Direct search
    jobs = search_external_jobs(query, location, limit=max_results)
    all_jobs.extend(jobs)
    
    # If not enough results, try variations
    if len(all_jobs) < max_results // 2:
        # Add variations like "engineer" -> "developer"
        query_variations = get_query_variations(query)
        
        for variation in query_variations:
            if len(all_jobs) >= max_results:
                break
            
            time.sleep(0.5)  # Rate limiting
            jobs = search_external_jobs(variation, location, limit=20)
            all_jobs.extend(jobs)
    
    return all_jobs[:max_results]

def get_query_variations(query):
    """Get query variations for better search coverage"""
    variations = []
    query_lower = query.lower()
    
    # Role variations
    if 'engineer' in query_lower:
        variations.append(query.replace('Engineer', 'Developer').replace('engineer', 'developer'))
    elif 'developer' in query_lower:
        variations.append(query.replace('Developer', 'Engineer').replace('developer', 'engineer'))
    
    # Level variations
    if 'senior' in query_lower:
        variations.append(query.replace('Senior ', '').replace('senior ', ''))
    elif 'junior' in query_lower:
        variations.append(query.replace('Junior ', '').replace('junior ', ''))
    
    # Abbreviations
    if 'machine learning' in query_lower:
        variations.append(query.replace('Machine Learning', 'ML').replace('machine learning', 'ML'))
    
    if 'artificial intelligence' in query_lower:
        variations.append(query.replace('Artificial Intelligence', 'AI').replace('artificial intelligence', 'AI'))
    
    # Full Stack variations
    if 'full stack' in query_lower:
        variations.extend([
            query.replace('Full Stack', 'Full-Stack').replace('full stack', 'full-stack'),
            query.replace('Full Stack', 'Fullstack').replace('full stack', 'fullstack')
        ])
    
    return variations[:3]  # Limit to 3 variations