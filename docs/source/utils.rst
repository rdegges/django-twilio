Utils
-----


Manage Twilio Sub Accounts
--------------------------

Django twilio provides minimal (albeit useful) support for creating and closing Twilio sub accounts.

Using our utils module, you can create a twilio sub account for a particular user::

    from django_twilio.utils import create_sub_account, close_sub_account, close_sub_accounts_for_user
    from django_twilio.client import twilio_client

    from django.contrib.auth import get_user_model
    user = get_user_model().objects.get(id=user_id)

    # Creates a `Credential` model with the account_sid returned from the new sub account creation.
    credential_obj, _ = create_sub_account(user, twilio_client, friendly_name="New sub account")

    # Closes the sub account
    close_sub_account(credential_obj.account_sid, twilio_client)

    # Closes all sub accounts linked to a particular user (`Credential` instances are tied to a user)
    close_sub_accounts_for_user([user], twilio_client)


