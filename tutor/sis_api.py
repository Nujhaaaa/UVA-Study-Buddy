import requests

BASE_URL = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01"


def search_courses(query, term):
    query_parts = query.split()

    if len(query_parts) == 2 and query_parts[0].isalpha() and query_parts[1].isnumeric():
        url = f"{BASE_URL}&term={term}&subject={query_parts[0]}&catalog_nbr={query_parts[1]}"
    elif query.isnumeric():
        url = f"{BASE_URL}&term={term}&catalog_nbr={query}"
    elif query.isalpha() and len(query) <= 4:
        url = f"{BASE_URL}&term={term}&subject={query}"
    else:
        url = f"{BASE_URL}&term={term}&keyword={query}"

    response = requests.get(url)
    courses = response.json()

    unique_courses = []
    ids_seen = set()
    for course in courses:
        course_id = course.get("subject") + course.get("catalog_nbr")
        if course_id not in ids_seen:
            unique_courses.append(course)
            ids_seen.add(course_id)

    return unique_courses
