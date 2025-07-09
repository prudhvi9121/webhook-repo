from datetime import datetime

def format_message(event_type, payload):
    timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')

    if event_type == "push":
        author = payload["pusher"]["name"]
        branch = payload["ref"].split("/")[-1]
        return {
            "type": "push",
            "author": author,
            "from_branch": None,
            "to_branch": branch,
            "timestamp": timestamp,
            "message": f"{author} pushed to {branch} on {timestamp}"
        }

    elif event_type == "pull_request":
        action = payload["action"]
        if action != "opened":
            return None  # Only process new PRs
        author = payload["pull_request"]["user"]["login"]
        from_branch = payload["pull_request"]["head"]["ref"]
        to_branch = payload["pull_request"]["base"]["ref"]
        return {
            "type": "pull_request",
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "message": f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
        }

    elif event_type == "pull_request" and payload.get("pull_request", {}).get("merged"):
        author = payload["pull_request"]["merged_by"]["login"]
        from_branch = payload["pull_request"]["head"]["ref"]
        to_branch = payload["pull_request"]["base"]["ref"]
        return {
            "type": "merge",
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "message": f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"
        }

    return None
