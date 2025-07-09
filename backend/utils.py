from datetime import datetime

def format_message(event_type, payload):
    timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')

    if event_type == "push":
        author = payload.get("pusher", {}).get("name", "Unknown")
        ref = payload.get("ref", "")
        to_branch = ref.split("/")[-1] if ref else "unknown"
        return {
            "type": "push",
            "author": author,
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "message": f"{author} pushed to {to_branch} on {timestamp}"
        }

    elif event_type == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        if action != "opened":
            return None  # We only care about newly opened PRs
        author = pr.get("user", {}).get("login", "Unknown")
        from_branch = pr.get("head", {}).get("ref", "unknown")
        to_branch = pr.get("base", {}).get("ref", "unknown")
        return {
            "type": "pull_request",
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "message": f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
        }

    elif event_type == "pull_request" and payload.get("pull_request", {}).get("merged"):
        pr = payload["pull_request"]
        author = pr.get("merged_by", {}).get("login", "Unknown")
        from_branch = pr.get("head", {}).get("ref", "unknown")
        to_branch = pr.get("base", {}).get("ref", "unknown")
        return {
            "type": "merge",
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "message": f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"
        }

    return None
