from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AIConversation, AIMessage
from .services import get_ai_response
from dashboard.models import Activity


@login_required
def ai_chat(request, pk=None):
    conversations = AIConversation.objects.filter(user=request.user)

    conversation = None
    if pk:
        conversation = get_object_or_404(
            AIConversation, pk=pk, user=request.user
        )

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()

        if prompt:
            if conversation is None:
                conversation = AIConversation.objects.create(
                    user=request.user,
                    title=prompt[:50]
                )

            
            history_messages = list(conversation.messages.all())

            AIMessage.objects.create(
                conversation=conversation,
                role=AIMessage.Role.USER,
                content=prompt
            )

            try:
                answer = get_ai_response(prompt, history_messages=history_messages)
            except Exception as e:
                answer = " Sorry, the AI is unavailable right now. Please try again."
                print("AI ERROR:", e)

            AIMessage.objects.create(
                conversation=conversation,
                role=AIMessage.Role.ASSISTANT,
                content=answer
            )

            Activity.objects.create(
                user=request.user,
                action=f"Asked AI: {prompt[:40]}"
            )

            return redirect('ai_conversation', pk=conversation.pk)

        return redirect('ai_chat')

    chat_messages = conversation.messages.all() if conversation else []

    return render(request, 'ai_assistant/chat.html', {
        'conversations': conversations,
        'conversation': conversation,
        'chat_messages': chat_messages,
    })


@login_required
def conversation_delete(request, pk):
    conversation = get_object_or_404(
        AIConversation, pk=pk, user=request.user
    )
    conversation.delete()
    messages.success(request, "Conversation deleted.")
    return redirect('ai_chat')