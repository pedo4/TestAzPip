def is_logged_in(session):
    if 'auth_token' in session and session['auth_token'] == 'mytoken':
        return True
    else:
        return False
