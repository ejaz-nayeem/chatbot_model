# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, ChatMessage
from .serializers import ConversationSerializer, ChatMessageSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def start_chat(request):
    """
    Starts a new conversation with the user's first message.
    Auto-generates title from the first message.
    """
    user = request.data.get('user', 'guest')
    first_message = request.data.get('message', '')

    if not first_message:
        return Response({'error': 'Message is required.'}, status=400)

    # Create conversation with title from first message
    conv = Conversation.objects.create(user=user, title=first_message[:50])

    # Save user message
    ChatMessage.objects.create(
        conversation=conv,
        sender=user,
        message=first_message,
        is_bot=False
    )

    # Generate bot reply
    reply = "Hi! This is the beginning of your conversation."
    ChatMessage.objects.create(
        conversation=conv,
        sender='bot',
        message=reply,
        is_bot=True
    )

    return Response({'conversation_id': conv.id, 'reply': reply}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def add_singlechat(request, id):
    """
    Adds a new message (user or bot) to an existing conversation.
    """
    conversation = get_object_or_404(Conversation, id=id)
    sender = request.data.get('sender')
    message = request.data.get('message')
    #is_bot = request.data.get('is_bot', False)

    if not sender or not message:
        return Response({'error': 'Both sender and message are required.'}, status=400)

    ChatMessage.objects.create(
        conversation=conversation,
        sender=sender,
        message=message,
        is_bot=False
    )

    return Response({'success': f'Message added to conversation {id}.'}, status=201)


@api_view(['GET'])
def chatcontent(request, conv_id):
    """
    Returns a conversation with all its messages.
    """
    try:
        conv = Conversation.objects.get(id=conv_id)
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found.'}, status=404)

    serializer = ConversationSerializer(conv)
    return Response(serializer.data)

@api_view(['GET'])
def chatlist(request):
    
    titles = Conversation.objects.values_list('title', flat=True)
    return Response({'titles': list(titles)})

