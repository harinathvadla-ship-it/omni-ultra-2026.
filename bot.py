import os
import github
import google.generativeai as genai

try:
    # Setup
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    gh = github.Github(os.getenv("GITHUB_TOKEN"))
    repo = gh.get_repo(os.getenv("GITHUB_REPOSITORY"))

    # Get the latest issue
    issues = repo.get_issues(state='open')
    if issues.totalCount > 0:
        issue = issues[0]
        user_input = issue.body or "Hello"

        # Talk to Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_input)

        # Reply and Close
        issue.create_comment(f"### OMNI-ULTRA Response\n\n{response.text}")
        issue.edit(state='closed')
        print("Success: Comment posted.")
    else:
        print("No open issues found.")

except Exception as e:
    print(f"Error occurred: {e}")
    exit(1)

