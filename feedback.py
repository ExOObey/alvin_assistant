def collect_feedback(user, message, response):
    # Placeholder: Save feedback to a file or send to a server
    with open('feedback.log', 'a') as f:
        f.write(f"User: {user}\nMessage: {message}\nResponse: {response}\n---\n")
