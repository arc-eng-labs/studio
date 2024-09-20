PR_DESCRIPTION = """
I've made some changes and opened a new PR: #{pr_number}.

I need a PR title and a description that summarizes these changes in short, concise bullet points.
The PR description will also be used as merge commit message, so it should be clear and informative.

Use the following guidelines:

## PR Title
- Start with a verb in the imperative mood (e.g., "Add", "Fix", "Update").
- Put an emoji at the beginning that reflects the nature of the changes

## PR Body

- At the very top, provide short paragraph summarizing the changes and their impact.
- Below, list the changes made in bullet points.
- Use bold text instead of sections/sub-sections to separate the bullet points into topics
- There should be no more than 3-4 topics
- Use the present tense and the active voice.
- Be specific - Include names, paths, identifiers, names, versions, etc
- Where possible, make file names/paths clickable using Markdown links. Use this format for the URL: `https://github.com/<github_project>/blob/<pr_branch>/<file_path>`


# Your task
Edit PR #{pr_number} title and description to reflect the changes made in this PR.
Respond only with a link to the PR.
"""
