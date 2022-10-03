import os

import onesignal as onesignal_sdk

from django.db.models import Q

from target.models import Target
from contact.models import Chat


def send_match_notification(username='Someone', user_ids=None):
    if user_ids:
        onesignal_client = onesignal_sdk.Client(
            user_auth_key=os.getenv('ONESIGNAL_USER_AUTH_KEY'),
            app_auth_key=os.getenv('ONESIGNAL_APP_AUTH_KEY'),
            app_id=os.getenv('ONESIGNAL_APP_ID'))
        notification = onesignal_sdk.Notification(post_body={
            "contents": {"en": f"{username} has matched with you!"},
            "include_external_user_ids": user_ids,
        })
        try:
            onesignal_client.send_notification(notification)
        except onesignal_sdk.error.OneSignalError:
            print(f"Notification to {username} was not sent.")


def manage_target_chats(target):
    matches = list(target.get_matches().values_list('pk', flat=True))
    # Delete existing chat that doesn't match anymore
    Chat.objects.filter(
        Q(target_one=target) | Q(target_two=target)
    ).exclude(
        Q(target_one__in=matches) | Q(target_two__in=matches)
    ).delete()

    # Get targets which matches without existing chat
    targets_with_chat_qs = Chat.objects.filter(
        Q(target_one=target, target_two__in=matches) | Q(target_one__in=matches, target_two=target)
    ).values_list('target_one', 'target_two')
    targets_with_chat = [x[0] if x[0] is not target.id else x[1] for x in list(targets_with_chat_qs)]
    targets_without_chat = Target.objects.filter(pk__in=matches).exclude(pk__in=targets_with_chat)

    # Create chat for those matches without chat
    chat_list = []
    for t in targets_without_chat.iterator():
        chat_list.append(Chat(target_one=target, target_two=t))
    Chat.objects.bulk_create(chat_list)

    # Send match notifications
    user_ids = list(targets_without_chat.values_list('user', flat=True))
    send_match_notification(target.user.email, user_ids)
