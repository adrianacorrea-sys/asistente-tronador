import os
import requests
import oracledb
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def test_oracle():
    print("\nTesting connection to Tronador (Oracle)...")
    try:
        conn = oracledb.connect(
            user=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=oracledb.makedsn(
                os.getenv("ORACLE_HOST"), 
                int(os.getenv("ORACLE_PORT")), 
                service_name=os.getenv("ORACLE_SERVICE_NAME")
            )
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM DUAL")
        result = cursor.fetchone()
        conn.close()
        print("OK Oracle: Connection successful")
        return True
    except Exception as e:
        print(f"FAIL Oracle: {e}")
        return False

def test_jira():
    print("\nTesting connection to Jira...")
    try:
        from src.services.jira import test_jira_connection
        success, message = test_jira_connection()
        if success:
            print(f"OK Jira: Connection successful (User: {message})")
            return True
        else:
            print(f"FAIL Jira: {message}")
            return False
    except Exception as e:
        print(f"FAIL Jira: {e}")
        return False

def test_github():
    print("\nTesting connection to GitHub...")
    try:
        url = f"https://api.github.com/repos/{os.getenv('GITHUB_REPO')}/contents"
        headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("OK GitHub: Connection successful")
            return True
        else:
            print(f"FAIL GitHub: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"FAIL GitHub: {e}")
        return False

def test_gemini():
    print("\nTesting connection to Gemini...")
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3-pro-preview')
        response = model.generate_content("Hello")
        print("OK Gemini: Connection successful")
        return True
    except Exception as e:
        print(f"FAIL Gemini: {e}")
        return False

if __name__ == "__main__":
    print("STARTING CONNECTION TESTS")
    print("=" * 40)
    
    results = {
        'Oracle': test_oracle(),
        'Jira': test_jira(),
        'GitHub': test_github(),
        'Gemini': test_gemini()
    }
    
    print("\n" + "=" * 40)
    print("SUMMARY:")
    for service, status in results.items():
        icon = "OK" if status else "FAIL"
        print(f"{icon} {service}: {'Alive' if status else 'Dead'}")
