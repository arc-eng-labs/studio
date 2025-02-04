import json
import logging

import arcane
import requests
from arcane.engine import ArcaneEngine
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from github import Github, GithubException

from repositories.models import BookmarkedRepo
from repositories.views import render_with_repositories
from studio.decorators import needs_api_key
from studio.github import get_github_token
from .models import PullRequestDescription
from .prompts import emoji_prompt, structure_prompt, style_prompt, PR_DESCRIPTION

logger = logging.getLogger(__name__)

def home(request):
    if not request.user.is_authenticated:
        return render(request, "pr_manager_preview.html", {
            "active_tab": "pull-request-manager",
        })
    return redirect("view_pull_request", owner=None, repo=None, pr_number=0)


@login_required
@needs_api_key
def view_pull_request(request, owner=None, repo=None, pr_number=0, api_key=None):
    if not owner or owner == 'None':
        first_bookmark = BookmarkedRepo.objects.first()
        if first_bookmark:
            owner = first_bookmark.owner
            repo = first_bookmark.repo_name
            return redirect('view_pull_request', owner=owner, repo=repo, pr_number=pr_number)
        else:
            return redirect('repositories:repo_overview')
    github_token = get_github_token(request)
    selected_pr = None
    if not owner or not repo:
        prs = []
    else:
        try:
            g = Github(github_token)
            github_repo = g.get_repo(f"{owner}/{repo}")
        except GithubException as e:
            if e.status == 401:
                # Log user out
                return redirect("user_logout")
            return render(request, "error.html", {"error": str(e)})
        prs = github_repo.get_pulls(state='open')

        if prs.totalCount == 0:
            return render_with_repositories(request, "view_pull_request.html", {
                "prs": None,
                "selected_pr": 0,
                "diff_data": "",
                "active_tab": "pull-request-manager",
            }, owner, repo)
        selected_pr = prs[0]
        for pr in prs:
            if pr.number == pr_number:
                selected_pr = pr
                break

    # Load the diff data for the selected PR
    url = f"https://{github_token}:x-oauth-basic@api.github.com/repos/{owner}/{repo}/pulls/{selected_pr.number}"
    headers = {
        "Accept": "application/vnd.github.diff"
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        return render(request, "error.html", {
            "error": f"Failed to load diff data: {response.text}"
        })
    diff_data = response.text

    # Check if there is a description for this PR
    description = PullRequestDescription.objects.filter(repo__owner=owner, repo__repo_name=repo, user=request.user, pr_number=selected_pr.number).first()
    task = None
    if description and not description.description:
        task = ArcaneEngine(api_key).get_task(description.task_id)
        if task.status == 'completed':
            description.description = task.result
            description.save()

    return render_with_repositories(request, "view_pull_request.html", {
        "prs": prs,
        "selected_pr": selected_pr,
        "diff_data": diff_data,
        "task": task,
        "description": description,
        "pr_description": description.description if description else "",
        "active_tab": "pull-request-manager",
    }, owner, repo)


@login_required
@require_POST
@needs_api_key
def generate_description(request, api_key):
    pr_number = request.POST.get('pr_number')
    owner = request.POST.get('owner')
    repo = request.POST.get('repo')
    emojis = request.POST.get('emojis')
    content_size = request.POST.get('content_size')
    structure = request.POST.get('structure')
    additional_instructions = request.POST.get('additional_instructions', '')
    add_emoji_to_title = request.POST.get('add_emoji_to_title', 'off') == 'on'

    engine = ArcaneEngine(api_key)
    prompt = PR_DESCRIPTION.format(
        pr_number=pr_number,
        structure=structure_prompt(structure),
        emoji_in_title="Include an emoji in the title." if add_emoji_to_title else "Do not include an emoji in the title.",
        additional_instructions=additional_instructions,
        emojis=emoji_prompt(emojis),
        style=style_prompt(content_size)
    )

    try:
        task = engine.create_task(f"{owner}/{repo}", prompt)
        # Create a new PullRequestDescription instance
        PullRequestDescription.objects.create(
            user=request.user,
            repo=BookmarkedRepo.objects.get(owner=owner, repo_name=repo),
            pr_number=pr_number,
            task_id=task.id
        )
    except arcane.exceptions.ApiException as e:
        logger.error(f"Failed to create task: {e}")
        msg = str(e)
        parsed_json = json.loads(e.body)
        if parsed_json.get('details'):
            msg = parsed_json.get('details')
        return render(request, "error.html", {
            "error": msg
        })

    return redirect(reverse('view_pull_request', args=(owner, repo, pr_number,)))


@login_required
@require_POST
def start_over(request):
    owner = request.POST.get('owner')
    repo = request.POST.get('repo')
    pr_number = request.POST.get('pr_number')
    PullRequestDescription.objects.filter(repo__owner=owner, repo__repo_name=repo, user=request.user, pr_number=pr_number).delete()
    return redirect('view_pull_request', owner=owner, repo=repo, pr_number=pr_number)