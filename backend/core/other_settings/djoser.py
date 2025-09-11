DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'PASSWORD_SET_CONFIRM_URL':
        'users/set_password_confirm/{uid}/{token}',  # path to confirm set password endpoint
    'EMAIL_SET_CONFIRM_URL':
        'users/set_email_confirm/{uid}/{token}',  # path to confirm set email endpoint
}