# from config import JOB_CATEGORIES
# import re

# def get_related_job_profiles(search_term):
#     """
#     Get related job profiles based on search term
#     Returns a list of job profiles that match the category or are related
#     """
#     search_term_lower = search_term.lower()
#     related_profiles = []
    
#     # If search term is a category, return all subcategories
#     for category, subcategories in JOB_CATEGORIES.items():
#         if search_term_lower in category.lower():
#             related_profiles.extend(subcategories)
#             return related_profiles
    
#     # If search term is a subcategory, find its category and return related ones
#     for category, subcategories in JOB_CATEGORIES.items():
#         for subcategory in subcategories:
#             if search_term_lower in subcategory.lower():
#                 # Add the exact match first
#                 related_profiles.append(subcategory)
#                 # Add other profiles from the same category
#                 related_profiles.extend([s for s in subcategories if s != subcategory])
#                 return related_profiles[:10]
    
#     # If no exact match, do fuzzy matching based on keywords
#     keyword_mapping = {
#         'software': JOB_CATEGORIES['Software Engineering'],
#         'developer': JOB_CATEGORIES['Software Engineering'],
#         'engineer': JOB_CATEGORIES['Software Engineering'] + JOB_CATEGORIES['DevOps & Cloud'],
#         'data': JOB_CATEGORIES['Data Science & Analytics'],
#         'analyst': JOB_CATEGORIES['Data Science & Analytics'],
#         'scientist': JOB_CATEGORIES['Data Science & Analytics'],
#         'machine learning': JOB_CATEGORIES['AI & Machine Learning'],
#         'ai': JOB_CATEGORIES['AI & Machine Learning'],
#         'ml': JOB_CATEGORIES['AI & Machine Learning'],
#         'devops': JOB_CATEGORIES['DevOps & Cloud'],
#         'cloud': JOB_CATEGORIES['DevOps & Cloud'],
#         'design': JOB_CATEGORIES['Design & Creative'],
#         'ui': JOB_CATEGORIES['Design & Creative'],
#         'ux': JOB_CATEGORIES['Design & Creative'],
#         'product': JOB_CATEGORIES['Product & Management'],
#         'manager': JOB_CATEGORIES['Product & Management'],
#         'qa': JOB_CATEGORIES['Quality & Testing'],
#         'test': JOB_CATEGORIES['Quality & Testing'],
#         'security': JOB_CATEGORIES['Cybersecurity'],
#         'database': JOB_CATEGORIES['Database'],
#         'react': ['React Developer', 'Frontend Developer', 'Full Stack Developer'],
#         'angular': ['Angular Developer', 'Frontend Developer', 'Full Stack Developer'],
#         'vue': ['Vue.js Developer', 'Frontend Developer', 'Full Stack Developer'],
#         'python': ['Python Developer', 'Backend Developer', 'Data Scientist', 'Machine Learning Engineer'],
#         'java': ['Java Developer', 'Backend Developer', 'Full Stack Developer'],
#         'javascript': ['Frontend Developer', 'Full Stack Developer', 'Node.js Developer'],
#         'node': ['Node.js Developer', 'Backend Developer', 'Full Stack Developer'],
#         'django': ['Django Developer', 'Python Developer', 'Backend Developer'],
#         'flask': ['Flask Developer', 'Python Developer', 'Backend Developer'],
#         'mobile': ['Mobile App Developer', 'iOS Developer', 'Android Developer'],
#         'ios': ['iOS Developer', 'Mobile App Developer'],
#         'android': ['Android Developer', 'Mobile App Developer'],
#         'web': ['Full Stack Developer', 'Frontend Developer', 'Backend Developer', 'Web Designer'],
#         'frontend': ['Frontend Developer', 'React Developer', 'Angular Developer', 'Vue.js Developer'],
#         'backend': ['Backend Developer', 'Node.js Developer', 'Python Developer', 'Java Developer'],
#         'fullstack': ['Full Stack Developer', 'Frontend Developer', 'Backend Developer'],
#         'full stack': ['Full Stack Developer', 'Frontend Developer', 'Backend Developer'],
#     }
    
#     # Check keywords
#     for keyword, profiles in keyword_mapping.items():
#         if keyword in search_term_lower:
#             related_profiles.extend(profiles)
#             return list(set(related_profiles))[:10]
    
#     # If still no match, return the search term itself
#     return [search_term]

# def extract_keywords_from_query(query):
#     """
#     Extract keywords from job query for better search matching
#     Returns list of keywords that can be used for additional searches
#     """
#     if query == "All Job Types":
#         return []
    
#     query_lower = query.lower()
#     keywords = []
    
#     # Technology keywords mapping
#     tech_keywords = {
#         'react': ['React', 'ReactJS', 'React.js', 'Frontend'],
#         'angular': ['Angular', 'AngularJS', 'Frontend'],
#         'vue': ['Vue', 'Vue.js', 'VueJS', 'Frontend'],
#         'python': ['Python', 'Django', 'Flask', 'Backend'],
#         'java': ['Java', 'Spring', 'Backend'],
#         'javascript': ['JavaScript', 'JS', 'Node', 'Frontend'],
#         'node': ['Node.js', 'NodeJS', 'Backend', 'JavaScript'],
#         'full stack': ['Full Stack', 'Fullstack', 'Software Engineer'],
#         'frontend': ['Frontend', 'Front-end', 'UI Developer'],
#         'backend': ['Backend', 'Back-end', 'Server'],
#         'mobile': ['Mobile', 'App Developer', 'iOS', 'Android'],
#         'data scientist': ['Data Science', 'Machine Learning', 'Analytics'],
#         'data analyst': ['Data Analysis', 'Business Intelligence', 'Analytics'],
#         'data engineer': ['Data Engineering', 'ETL', 'Big Data'],
#         'machine learning': ['ML', 'AI', 'Deep Learning'],
#         'devops': ['DevOps', 'Cloud', 'AWS', 'Azure'],
#         'cloud': ['AWS', 'Azure', 'GCP', 'Cloud Engineer'],
#         'ui/ux': ['UI', 'UX', 'Designer', 'Product Designer'],
#         'product manager': ['PM', 'Product', 'Management'],
#         'qa': ['QA', 'Quality Assurance', 'Testing', 'SDET'],
#         'security': ['Cybersecurity', 'InfoSec', 'Security Engineer'],
#         'database': ['DBA', 'SQL', 'Database Administrator'],
#     }
    
#     # Extract keywords based on query
#     for key, values in tech_keywords.items():
#         if key in query_lower:
#             keywords.extend(values)
    
#     # Add role-level keywords
#     role_keywords = {
#         'senior': ['Senior', 'Lead', 'Principal'],
#         'junior': ['Junior', 'Entry Level', 'Associate'],
#         'lead': ['Lead', 'Principal', 'Senior'],
#         'principal': ['Principal', 'Lead', 'Staff'],
#     }
    
#     for key, values in role_keywords.items():
#         if key in query_lower:
#             # Don't add role keywords to avoid over-filtering
#             pass
    
#     # Remove duplicates and return
#     return list(set(keywords))

# def match_user_skills_to_jobs(user_skills, job_skills_required):
#     """
#     Calculate match percentage between user skills and job requirements
#     Returns percentage (0-100)
#     """
#     if not user_skills or not job_skills_required:
#         return 0
    
#     user_skills_lower = [skill.lower().strip() for skill in user_skills]
#     job_skills_lower = [skill.lower().strip() for skill in job_skills_required]
    
#     matched_skills = len(set(user_skills_lower) & set(job_skills_lower))
#     total_required = len(job_skills_lower)
    
#     if total_required == 0:
#         return 0
    
#     return int((matched_skills / total_required) * 100)

# def normalize_job_title(title):
#     """
#     Normalize job title for better matching
#     """
#     title_lower = title.lower().strip()
    
#     # Remove common prefixes/suffixes
#     patterns_to_remove = [
#         r'\b(senior|sr|junior|jr|lead|principal|staff|entry level|mid level)\b',
#         r'\b(i|ii|iii|iv|v|1|2|3|4|5)\b',
#         r'\([^)]*\)',  # Remove parentheses content
#     ]
    
#     for pattern in patterns_to_remove:
#         title_lower = re.sub(pattern, '', title_lower)
    
#     # Clean up extra spaces
#     title_lower = ' '.join(title_lower.split())
    
#     return title_lower

# def get_skill_variations(skill):
#     """
#     Get variations of a skill name for better matching
#     """
#     skill_lower = skill.lower().strip()
    
#     variations = {
#         'javascript': ['js', 'javascript', 'java script'],
#         'typescript': ['ts', 'typescript'],
#         'reactjs': ['react', 'reactjs', 'react.js'],
#         'angular': ['angular', 'angularjs', 'angular.js'],
#         'vuejs': ['vue', 'vuejs', 'vue.js'],
#         'nodejs': ['node', 'nodejs', 'node.js'],
#         'python': ['python', 'py'],
#         'machine learning': ['ml', 'machine learning', 'machinelearning'],
#         'artificial intelligence': ['ai', 'artificial intelligence'],
#         'amazon web services': ['aws', 'amazon web services'],
#         'google cloud platform': ['gcp', 'google cloud'],
#         'microsoft azure': ['azure', 'microsoft azure'],
#     }
    
#     for key, values in variations.items():
#         if skill_lower in values:
#             return values
    
#     return [skill_lower]

from config import JOB_CATEGORIES
import re

def generate_comprehensive_search_terms(job_category, user):
    """
    Generate comprehensive search terms based on category and user profile
    """
    search_terms = []
    
    if job_category == "All Categories":
        # Strategy 1: Top roles from each category (prioritize variety)
        for category, subcategories in JOB_CATEGORIES.items():
            search_terms.extend(subcategories[:2])  # Top 2 from each category
        
        # Strategy 2: Add user's skills as search terms if available
        if user.get('skills'):
            skill_based_roles = map_skills_to_roles(user['skills'][:5])
            search_terms.extend(skill_based_roles)
        
        # Strategy 3: Add generic high-demand roles
        search_terms.extend([
            "Software Engineer", "Developer", "Engineer",
            "Data Scientist", "Product Manager", "Designer"
        ])
    
    else:
        # Strategy 1: All subcategories from selected category
        subcategories = JOB_CATEGORIES.get(job_category, [])
        search_terms.extend(subcategories)
        
        # Strategy 2: Add variations and related terms
        variations = generate_role_variations(subcategories[:8])
        search_terms.extend(variations)
        
        # Strategy 3: Add skill-matched terms if relevant to category
        if user.get('skills'):
            category_skills = filter_skills_by_category(user['skills'], job_category)
            skill_roles = map_skills_to_roles(category_skills)
            search_terms.extend(skill_roles)
        
        # Strategy 4: Add generic category term
        search_terms.append(job_category.replace(" & ", " ").replace("  ", " "))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_terms = []
    for term in search_terms:
        term_lower = term.lower()
        if term_lower not in seen:
            seen.add(term_lower)
            unique_terms.append(term)
    
    # Limit to reasonable number (API rate limiting)
    return unique_terms[:25]


def generate_role_variations(roles):
    """
    Generate variations of role names for broader search coverage
    """
    variations = []
    
    for role in roles:
        role_lower = role.lower()
        
        # Remove level prefixes for broader search
        base_role = role
        for prefix in ['Senior ', 'Junior ', 'Lead ', 'Principal ', 'Staff ']:
            if role.startswith(prefix):
                base_role = role.replace(prefix, '')
                variations.append(base_role)
        
        # Add common variations
        if 'developer' in role_lower:
            variations.append(role.replace('Developer', 'Engineer'))
        elif 'engineer' in role_lower:
            variations.append(role.replace('Engineer', 'Developer'))
        
        # Technology-specific variations
        if 'full stack' in role_lower:
            variations.extend(['Full-Stack Developer', 'Fullstack Engineer', 'Full Stack Engineer'])
        
        if 'frontend' in role_lower or 'front-end' in role_lower:
            variations.extend(['Front-end Developer', 'Front End Engineer', 'Frontend Engineer'])
        
        if 'backend' in role_lower or 'back-end' in role_lower:
            variations.extend(['Back-end Developer', 'Back End Engineer', 'Backend Engineer'])
        
        # Framework-specific expansions
        if 'react' in role_lower:
            variations.extend(['ReactJS Developer', 'React.js Engineer', 'Frontend Developer'])
        
        if 'node' in role_lower:
            variations.extend(['NodeJS Developer', 'Node.js Engineer', 'Backend Developer'])
        
        if 'python' in role_lower:
            variations.extend(['Python Engineer', 'Backend Developer'])
        
        if 'java' in role_lower and 'javascript' not in role_lower:
            variations.extend(['Java Engineer', 'Backend Developer'])
        
        # Data roles
        if 'data scientist' in role_lower:
            variations.extend(['Data Science', 'ML Engineer'])
        
        if 'data analyst' in role_lower:
            variations.extend(['Data Analysis', 'Business Analyst'])
        
        if 'data engineer' in role_lower:
            variations.extend(['Data Engineering', 'ETL Developer'])
    
    return list(set(variations))[:15]  # Limit variations


def map_skills_to_roles(skills):
    """
    Map user skills to relevant job roles
    """
    skill_to_role_map = {
        # Frontend
        'react': ['React Developer', 'Frontend Developer', 'Full Stack Developer'],
        'reactjs': ['React Developer', 'Frontend Developer'],
        'angular': ['Angular Developer', 'Frontend Developer', 'Full Stack Developer'],
        'vue': ['Vue Developer', 'Frontend Developer', 'Full Stack Developer'],
        'vue.js': ['Vue Developer', 'Frontend Developer'],
        'javascript': ['JavaScript Developer', 'Frontend Developer', 'Full Stack Developer'],
        'typescript': ['TypeScript Developer', 'Frontend Developer', 'Full Stack Developer'],
        'html': ['Frontend Developer', 'Web Developer'],
        'css': ['Frontend Developer', 'Web Developer'],
        'tailwind': ['Frontend Developer', 'UI Developer'],
        'bootstrap': ['Frontend Developer', 'Web Developer'],
        'next.js': ['Next.js Developer', 'React Developer', 'Full Stack Developer'],
        'nuxt': ['Nuxt Developer', 'Vue Developer'],
        
        # Backend
        'python': ['Python Developer', 'Backend Developer', 'Full Stack Developer'],
        'java': ['Java Developer', 'Backend Developer', 'Full Stack Developer'],
        'node.js': ['Node.js Developer', 'Backend Developer', 'Full Stack Developer'],
        'nodejs': ['Node.js Developer', 'Backend Developer'],
        'express': ['Node.js Developer', 'Backend Developer'],
        'django': ['Django Developer', 'Python Developer', 'Backend Developer'],
        'flask': ['Flask Developer', 'Python Developer', 'Backend Developer'],
        'spring': ['Java Developer', 'Spring Developer', 'Backend Developer'],
        'spring boot': ['Java Developer', 'Spring Developer'],
        'php': ['PHP Developer', 'Backend Developer'],
        'laravel': ['Laravel Developer', 'PHP Developer'],
        'ruby': ['Ruby Developer', 'Backend Developer'],
        'rails': ['Ruby on Rails Developer', 'Backend Developer'],
        'go': ['Go Developer', 'Backend Developer'],
        'golang': ['Go Developer', 'Backend Developer'],
        'c#': ['C# Developer', '.NET Developer'],
        '.net': ['.NET Developer', 'C# Developer'],
        'asp.net': ['.NET Developer', 'Backend Developer'],
        
        # Full Stack
        'full stack': ['Full Stack Developer'],
        'fullstack': ['Full Stack Developer'],
        'mern': ['Full Stack Developer', 'MERN Stack Developer'],
        'mean': ['Full Stack Developer', 'MEAN Stack Developer'],
        'lamp': ['Full Stack Developer', 'Web Developer'],
        
        # Mobile
        'ios': ['iOS Developer', 'Mobile Developer'],
        'android': ['Android Developer', 'Mobile Developer'],
        'react native': ['React Native Developer', 'Mobile Developer'],
        'flutter': ['Flutter Developer', 'Mobile Developer'],
        'swift': ['iOS Developer', 'Swift Developer'],
        'kotlin': ['Android Developer', 'Kotlin Developer'],
        'xamarin': ['Xamarin Developer', 'Mobile Developer'],
        
        # Data & ML
        'machine learning': ['Machine Learning Engineer', 'Data Scientist', 'AI Engineer'],
        'ml': ['Machine Learning Engineer', 'Data Scientist'],
        'data science': ['Data Scientist', 'Data Analyst', 'ML Engineer'],
        'deep learning': ['Deep Learning Engineer', 'ML Engineer', 'AI Engineer'],
        'tensorflow': ['ML Engineer', 'AI Engineer', 'Data Scientist'],
        'pytorch': ['ML Engineer', 'AI Engineer', 'Data Scientist'],
        'keras': ['ML Engineer', 'Data Scientist'],
        'scikit-learn': ['ML Engineer', 'Data Scientist'],
        'nlp': ['NLP Engineer', 'ML Engineer', 'AI Engineer'],
        'computer vision': ['Computer Vision Engineer', 'ML Engineer'],
        'sql': ['Data Analyst', 'Database Developer', 'Data Engineer'],
        'pandas': ['Data Analyst', 'Data Scientist', 'Data Engineer'],
        'numpy': ['Data Scientist', 'Data Analyst'],
        'tableau': ['Data Analyst', 'BI Analyst'],
        'power bi': ['Data Analyst', 'BI Analyst'],
        'excel': ['Data Analyst', 'Business Analyst'],
        'r': ['Data Scientist', 'Data Analyst'],
        'spark': ['Data Engineer', 'Big Data Engineer'],
        'hadoop': ['Data Engineer', 'Big Data Engineer'],
        'etl': ['Data Engineer', 'ETL Developer'],
        
        # DevOps & Cloud
        'aws': ['AWS Engineer', 'Cloud Engineer', 'DevOps Engineer'],
        'azure': ['Azure Engineer', 'Cloud Engineer', 'DevOps Engineer'],
        'gcp': ['GCP Engineer', 'Cloud Engineer', 'DevOps Engineer'],
        'google cloud': ['GCP Engineer', 'Cloud Engineer'],
        'docker': ['DevOps Engineer', 'Platform Engineer', 'Cloud Engineer'],
        'kubernetes': ['DevOps Engineer', 'K8s Engineer', 'Cloud Engineer'],
        'k8s': ['DevOps Engineer', 'Kubernetes Engineer'],
        'jenkins': ['DevOps Engineer', 'CI/CD Engineer'],
        'terraform': ['DevOps Engineer', 'Infrastructure Engineer'],
        'ansible': ['DevOps Engineer', 'Infrastructure Engineer'],
        'ci/cd': ['DevOps Engineer', 'Platform Engineer'],
        'linux': ['DevOps Engineer', 'System Administrator'],
        'devops': ['DevOps Engineer'],
        
        # Design
        'figma': ['UI/UX Designer', 'Product Designer', 'UI Designer'],
        'sketch': ['UI/UX Designer', 'Product Designer'],
        'adobe xd': ['UI/UX Designer', 'Product Designer'],
        'photoshop': ['Graphic Designer', 'UI Designer'],
        'illustrator': ['Graphic Designer', 'Designer'],
        'ui/ux': ['UI/UX Designer', 'Product Designer'],
        'wireframing': ['UI/UX Designer', 'Product Designer'],
        'prototyping': ['UI/UX Designer', 'Product Designer'],
        
        # Database
        'mongodb': ['Database Developer', 'Backend Developer', 'Full Stack Developer'],
        'postgresql': ['Database Developer', 'Backend Developer', 'Data Engineer'],
        'mysql': ['Database Developer', 'Backend Developer'],
        'redis': ['Backend Developer', 'Database Developer'],
        'elasticsearch': ['Backend Developer', 'Search Engineer'],
        'dynamodb': ['AWS Developer', 'Backend Developer'],
        
        # Testing & QA
        'selenium': ['QA Engineer', 'Automation Engineer'],
        'pytest': ['QA Engineer', 'Python Developer'],
        'jest': ['Frontend Developer', 'QA Engineer'],
        'cypress': ['QA Engineer', 'Frontend Developer'],
        
        # Other
        'git': ['Software Engineer', 'Developer'],
        'agile': ['Scrum Master', 'Project Manager'],
        'scrum': ['Scrum Master', 'Agile Coach'],
        'jira': ['Project Manager', 'Scrum Master'],
    }
    
    roles = []
    for skill in skills:
        skill_lower = skill.lower().strip()
        for key, role_list in skill_to_role_map.items():
            if key in skill_lower or skill_lower in key:
                roles.extend(role_list)
    
    return list(set(roles))


def filter_skills_by_category(skills, category):
    """
    Filter user skills that are relevant to the selected job category
    """
    category_skill_map = {
        'Software Engineering': [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 
            'vue', 'node', 'django', 'flask', 'spring', 'c++', 'c#', 'go', 
            'ruby', 'php', 'html', 'css', 'express', 'laravel', 'rails',
            'next.js', 'nuxt', 'swift', 'kotlin', 'ios', 'android'
        ],
        'Data Science & Analytics': [
            'python', 'r', 'sql', 'pandas', 'numpy', 'tableau', 'power bi',
            'excel', 'statistics', 'data analysis', 'etl', 'spark', 'hadoop',
            'postgres', 'mysql', 'mongodb'
        ],
        'AI & Machine Learning': [
            'python', 'tensorflow', 'pytorch', 'keras', 'machine learning',
            'deep learning', 'nlp', 'computer vision', 'ml', 'ai',
            'scikit-learn', 'pandas', 'numpy'
        ],
        'DevOps & Cloud': [
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd',
            'terraform', 'ansible', 'linux', 'devops', 'k8s', 'git'
        ],
        'Design & Creative': [
            'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
            'ui/ux', 'wireframing', 'prototyping', 'design'
        ],
        'Product & Management': [
            'agile', 'scrum', 'jira', 'product management', 'project management',
            'roadmap', 'stakeholder', 'requirements'
        ],
        'Quality & Testing': [
            'selenium', 'pytest', 'jest', 'cypress', 'qa', 'testing',
            'automation', 'test automation'
        ],
        'Cybersecurity': [
            'security', 'penetration testing', 'ethical hacking', 'infosec',
            'cybersecurity', 'vulnerability', 'firewall', 'encryption'
        ],
        'Database': [
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'oracle',
            'database', 'dba', 'dynamodb', 'elasticsearch'
        ],
    }
    
    relevant_keywords = category_skill_map.get(category, [])
    filtered = []
    
    for skill in skills:
        skill_lower = skill.lower().strip()
        if any(keyword in skill_lower or skill_lower in keyword 
               for keyword in relevant_keywords):
            filtered.append(skill)
    
    return filtered


def create_job_key(job):
    """
    Create unique key for job deduplication (more lenient)
    """
    title = job.get('title', '').lower().strip()
    company = job.get('company', '').lower().strip()
    location = job.get('location', '').lower().strip()
    
    # Normalize title by removing common words
    title_normalized = title.replace('senior', '').replace('junior', '').replace('lead', '')
    title_normalized = title_normalized.replace('principal', '').replace('staff', '')
    title_normalized = ' '.join(title_normalized.split())
    
    # Use first 50 chars of title + company (more lenient than before)
    return f"{title_normalized[:50]}|{company[:30]}"


def add_skill_match_scores(jobs, user_skills):
    """
    Add skill match scores to jobs for better ranking
    """
    user_skills_lower = [s.lower().strip() for s in user_skills]
    user_skills_set = set(user_skills_lower)
    
    # Also create variations of user skills
    user_skills_variations = set()
    for skill in user_skills_lower:
        user_skills_variations.update(get_skill_variations(skill))
    
    for job in jobs:
        job_skills = job.get('skills_required', [])
        if job_skills:
            job_skills_lower = [s.lower().strip() for s in job_skills]
            job_skills_set = set(job_skills_lower)
            
            # Also create variations of job skills
            job_skills_variations = set()
            for skill in job_skills_lower:
                job_skills_variations.update(get_skill_variations(skill))
            
            # Calculate match percentage (exact + variations)
            exact_matches = len(user_skills_set & job_skills_set)
            variation_matches = len(user_skills_variations & job_skills_variations)
            
            total_matches = exact_matches + (variation_matches * 0.5)  # Weight variations less
            total = len(job_skills_lower)
            
            match_score = (total_matches / total * 100) if total > 0 else 0
            match_score = min(100, match_score)  # Cap at 100%
            
            job['skill_match_score'] = match_score
            job['matched_skills'] = list(user_skills_set & job_skills_set)
        else:
            job['skill_match_score'] = 0
            job['matched_skills'] = []
    
    return jobs


def get_skill_variations(skill):
    """
    Get variations of a skill name for better matching
    """
    skill_lower = skill.lower().strip()
    
    variations_map = {
        'javascript': ['js', 'javascript', 'java script'],
        'js': ['js', 'javascript'],
        'typescript': ['ts', 'typescript'],
        'ts': ['ts', 'typescript'],
        'reactjs': ['react', 'reactjs', 'react.js'],
        'react': ['react', 'reactjs', 'react.js'],
        'angular': ['angular', 'angularjs', 'angular.js'],
        'vuejs': ['vue', 'vuejs', 'vue.js'],
        'vue': ['vue', 'vuejs', 'vue.js'],
        'nodejs': ['node', 'nodejs', 'node.js'],
        'node': ['node', 'nodejs', 'node.js'],
        'node.js': ['node', 'nodejs', 'node.js'],
        'python': ['python', 'py'],
        'py': ['python', 'py'],
        'machine learning': ['ml', 'machine learning', 'machinelearning'],
        'ml': ['ml', 'machine learning'],
        'artificial intelligence': ['ai', 'artificial intelligence'],
        'ai': ['ai', 'artificial intelligence'],
        'amazon web services': ['aws', 'amazon web services'],
        'aws': ['aws', 'amazon web services'],
        'google cloud platform': ['gcp', 'google cloud'],
        'gcp': ['gcp', 'google cloud platform', 'google cloud'],
        'microsoft azure': ['azure', 'microsoft azure'],
        'azure': ['azure', 'microsoft azure'],
        'kubernetes': ['k8s', 'kubernetes'],
        'k8s': ['k8s', 'kubernetes'],
        'c++': ['cpp', 'c++', 'cplusplus'],
        'c#': ['csharp', 'c#'],
        'postgresql': ['postgres', 'postgresql'],
        'postgres': ['postgres', 'postgresql'],
    }
    
    for key, values in variations_map.items():
        if skill_lower in values or skill_lower == key:
            return values
    
    return [skill_lower]


def sort_jobs_by_relevance(jobs):
    """
    Sort jobs by relevance (skill match, then by date)
    """
    # Separate internal and external
    internal = [j for j in jobs if j.get('source') != 'external']
    external = [j for j in jobs if j.get('source') == 'external']
    
    # Sort internal by skill match score and date
    internal_sorted = sorted(internal, 
                            key=lambda x: (x.get('skill_match_score', 0), 
                                         x.get('created_at', '')), 
                            reverse=True)
    
    # Sort external by skill match score
    external_sorted = sorted(external, 
                            key=lambda x: x.get('skill_match_score', 0), 
                            reverse=True)
    
    # Interleave: show internal first, then external
    return internal_sorted + external_sorted


def get_related_job_profiles(search_term):
    """
    Get related job profiles based on search term
    Returns a list of job profiles that match the category or are related
    """
    search_term_lower = search_term.lower()
    related_profiles = []
    
    # If search term is a category, return all subcategories
    for category, subcategories in JOB_CATEGORIES.items():
        if search_term_lower in category.lower():
            related_profiles.extend(subcategories)
            return related_profiles
    
    # If search term is a subcategory, find its category and return related ones
    for category, subcategories in JOB_CATEGORIES.items():
        for subcategory in subcategories:
            if search_term_lower in subcategory.lower():
                # Add the exact match first
                related_profiles.append(subcategory)
                # Add other profiles from the same category
                related_profiles.extend([s for s in subcategories if s != subcategory])
                return related_profiles[:10]
    
    # If no exact match, do fuzzy matching based on keywords
    keyword_mapping = {
        'software': JOB_CATEGORIES['Software Engineering'],
        'developer': JOB_CATEGORIES['Software Engineering'],
        'engineer': JOB_CATEGORIES['Software Engineering'] + JOB_CATEGORIES['DevOps & Cloud'],
        'data': JOB_CATEGORIES['Data Science & Analytics'],
        'analyst': JOB_CATEGORIES['Data Science & Analytics'],
        'scientist': JOB_CATEGORIES['Data Science & Analytics'],
        'machine learning': JOB_CATEGORIES['AI & Machine Learning'],
        'ai': JOB_CATEGORIES['AI & Machine Learning'],
        'ml': JOB_CATEGORIES['AI & Machine Learning'],
        'devops': JOB_CATEGORIES['DevOps & Cloud'],
        'cloud': JOB_CATEGORIES['DevOps & Cloud'],
        'design': JOB_CATEGORIES['Design & Creative'],
        'ui': JOB_CATEGORIES['Design & Creative'],
        'ux': JOB_CATEGORIES['Design & Creative'],
        'product': JOB_CATEGORIES['Product & Management'],
        'manager': JOB_CATEGORIES['Product & Management'],
        'qa': JOB_CATEGORIES['Quality & Testing'],
        'test': JOB_CATEGORIES['Quality & Testing'],
        'security': JOB_CATEGORIES['Cybersecurity'],
        'database': JOB_CATEGORIES['Database'],
    }
    
    # Check keywords
    for keyword, profiles in keyword_mapping.items():
        if keyword in search_term_lower:
            related_profiles.extend(profiles)
            return list(set(related_profiles))[:10]
    
    # If still no match, return the search term itself
    return [search_term]


def extract_keywords_from_query(query):
    """
    Extract keywords from job query for better search matching
    Returns list of keywords that can be used for additional searches
    """
    if query == "All Job Types":
        return []
    
    query_lower = query.lower()
    keywords = []
    
    # Check if query contains any skills
    for skill in ['python', 'java', 'javascript', 'react', 'angular', 'vue', 
                  'node', 'aws', 'docker', 'kubernetes']:
        if skill in query_lower:
            keywords.append(skill)
    
    return keywords


def match_user_skills_to_jobs(user_skills, job_skills_required):
    """
    Calculate match percentage between user skills and job requirements
    Returns percentage (0-100)
    """
    if not user_skills or not job_skills_required:
        return 0
    
    user_skills_lower = [skill.lower().strip() for skill in user_skills]
    job_skills_lower = [skill.lower().strip() for skill in job_skills_required]
    
    matched_skills = len(set(user_skills_lower) & set(job_skills_lower))
    total_required = len(job_skills_lower)
    
    if total_required == 0:
        return 0
    
    return int((matched_skills / total_required) * 100)


def normalize_job_title(title):
    """
    Normalize job title for better matching
    """
    title_lower = title.lower().strip()
    
    # Remove common prefixes/suffixes
    patterns_to_remove = [
        r'\b(senior|sr|junior|jr|lead|principal|staff|entry level|mid level)\b',
        r'\b(i|ii|iii|iv|v|1|2|3|4|5)\b',
        r'\([^)]*\)',  # Remove parentheses content
    ]
    
    for pattern in patterns_to_remove:
        title_lower = re.sub(pattern, '', title_lower)
    
    # Clean up extra spaces
    title_lower = ' '.join(title_lower.split())
    
    return title_lower