import os
import github
from google import genai

try:
    # 1. Setup SDK
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # 2. Setup GitHub Auth
    auth = github.Auth.Token(os.getenv("GITHUB_TOKEN"))
    gh = github.Github(auth=auth)
    repo = gh.get_repo(os.getenv("GITHUB_REPOSITORY"))

    # 3. Get the latest issue
    issues = repo.get_issues(state='open')
    if issues.totalCount > 0:
        issue = issues[0]
        user_input = issue.body or "Hello"

        # 4. Generate response with 2.5 Flash
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=user_input
        )

        # 5. Post comment and close issue
        issue.create_comment(f"### OMNI-ULTRA (Gemini 2.5) Response\n\n{response.text}")
        issue.edit(state='closed')
        print("Success: 2.5 Agent responded.")
    else:
        print("No open issues.")

except Exception as e:
    print(f"Error occurred: {e}")
    exit(1)
