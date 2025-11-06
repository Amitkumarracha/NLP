"""
Mental health conversational chatbot service
Provides empathetic, therapeutic responses with crisis detection
"""
import random
from services.text_service import analyze_text_emotion

# Mental health keywords and patterns for detection
MENTAL_HEALTH_PATTERNS = {
    'depression': ['depressed', 'hopeless', 'worthless', 'nothing matters'],
    'anxiety': ['anxious', 'panic', 'worried', 'scared', 'nervous', 'stressed'],
    'loneliness': ['alone', 'lonely', 'isolated', 'no one', 'nobody'],
    'self_harm': ['hurt myself', 'end it', 'suicide', 'kill myself'],
    'improvement': ['better', 'improving', 'good', 'happy', 'grateful'],
    'seeking_help': ['help', 'support', 'talk', 'listen'],
    'sleep': ['sleep', 'insomnia', 'tired', 'exhausted', 'can\'t sleep'],
    'relationships': ['friend', 'family', 'relationship', 'partner', 'conflict'],
}

# Emotion-specific therapeutic responses
THERAPEUTIC_RESPONSES = {
    'angry': [
        "I can feel your frustration coming through. Anger is often protecting us from other feelings - sometimes hurt, fear, or disappointment. What do you think is underneath this anger?",
        "I hear your anger. It's a valid emotion. What would help you feel more in control right now?",
        "Anger can be a signal that something important needs attention. What matters most to you in this situation?"
    ],
    'sad': [
        "Sadness deserves space. It's okay to feel this way. Sometimes acknowledging our pain is the first step to healing. Would you like to share what's making you sad?",
        "I'm sitting with you in this sadness. You don't have to carry it alone. What's weighing heaviest on your heart?",
        "Your sadness is valid. Even in dark moments, remember that feelings are temporary. What usually brings you even small comfort?"
    ],
    'fearful': [
        "Fear is trying to protect you, but sometimes it overreacts. Let's acknowledge it without letting it control us. What specific worry is most present for you right now?",
        "I understand you're feeling scared. Let's ground you in the present moment. Can you tell me 3 things you can see right now?",
        "Anxiety can feel overwhelming, but you're safe with me. What would help you feel more secure?"
    ],
    'happy': [
        "I love that you're experiencing joy! These moments are precious. What about this makes you happy? Let's savor it together.",
        "Your happiness is wonderful to witness! How can you carry some of this positive energy forward?",
        "This joy is beautiful. What does it feel like in your body right now?"
    ],
    'calm': [
        "You seem at peace. That's beautiful. How can I support you today?",
        "I appreciate your calm energy. What's helping you feel centered right now?",
        "This peaceful moment is valuable. What would you like to explore?"
    ],
    'neutral': [
        "I'm here with you. Sometimes just being present is enough. What's on your mind right now?",
        "I'm listening. What would you like to talk about?",
        "How are you really feeling right now? It's okay if you're not sure."
    ],
    'surprised': [
        "Something unexpected happened! How are you processing this surprise?",
        "I can hear the surprise in your words. Take your time - what's going through your mind?",
        "Surprises can be disorienting. What do you need right now?"
    ],
    'disgust': [
        "I sense you're uncomfortable with something. Your boundaries matter. What's bothering you?",
        "That reaction makes sense. Let's talk through what you're feeling.",
        "Sometimes disgust is our body's way of saying 'this isn't right for me.' What doesn't feel aligned?"
    ]
}

def detect_crisis_language(message: str):
    """
    Detect if message contains crisis/self-harm language
    
    Args:
        message: User's message
    
    Returns:
        Boolean indicating if crisis language detected
    """
    message_lower = message.lower()
    return any(word in message_lower for word in MENTAL_HEALTH_PATTERNS['self_harm'])

def generate_crisis_response():
    """
    Generate immediate crisis intervention response
    
    Returns:
        Crisis support message with helpline
    """
    return (
        "I'm really concerned about what you're sharing. Your life matters, and there are people who want to help. "
        "Please reach out to a crisis helpline immediately:\n"
        "• National Suicide Prevention Lifeline: 988\n"
        "• Crisis Text Line: Text HOME to 741741\n"
        "Would you like to talk about what's making you feel this way? I'm here, but professional support is crucial."
    )

def detect_mental_health_topic(message: str):
    """
    Detect specific mental health topics in message
    
    Args:
        message: User's message
    
    Returns:
        Topic name or None
    """
    message_lower = message.lower()
    
    for topic, keywords in MENTAL_HEALTH_PATTERNS.items():
        if any(word in message_lower for word in keywords):
            return topic
    
    return None

def generate_topic_response(topic: str):
    """
    Generate response based on detected mental health topic
    
    Args:
        topic: Detected mental health topic
    
    Returns:
        Appropriate response string or None
    """
    topic_responses = {
        'depression': [
            "I hear you, and those feelings are valid. Depression can make everything feel heavy. What's been weighing on you the most?",
            "Thank you for sharing this with me. Depression is challenging, but you're not alone. Small steps count - have you been able to do anything for yourself today?",
            "It takes courage to express these feelings. What usually helps you feel even slightly better?"
        ],
        'anxiety': [
            "Anxiety can feel overwhelming, but you're safe right now. Let's try grounding: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste. What triggered these anxious feelings?",
            "I understand you're feeling anxious. Let's slow down together. Can you take three deep breaths with me?",
            "Anxiety is trying to protect you, but sometimes it goes into overdrive. What's your biggest worry right now?"
        ],
        'loneliness': [
            "Feeling isolated is really painful. I want you to know that I'm here, and you matter. Have you been able to connect with anyone recently, even briefly?",
            "Loneliness can feel so heavy. You're not alone in this conversation. What kind of connection are you craving?",
            "I hear how isolating this feels. Even small connections can help - is there someone you could reach out to today?"
        ],
        'improvement': [
            "That's wonderful to hear! Progress isn't always linear, but celebrating these moments is important. What do you think contributed to feeling this way?",
            "I'm so glad you're experiencing improvement! What's been helping you move forward?",
            "This positive change is worth acknowledging. How can you nurture this progress?"
        ],
        'sleep': [
            "Sleep struggles can affect everything. Have you tried a bedtime routine? Some people find success with: no screens 1 hour before bed, cool dark room, and deep breathing. What's your sleep environment like?",
            "Insomnia is exhausting. What's been keeping you awake - physical discomfort or racing thoughts?",
            "Sleep issues often connect to stress or routine. What time do you usually try to sleep?"
        ],
        'relationships': [
            "Relationships can be complex. What's happening that's bringing this up for you?",
            "Connection with others matters so much. Tell me more about what's going on.",
            "Relationship challenges are difficult. How is this affecting you?"
        ]
    }
    
    responses = topic_responses.get(topic)
    if responses:
        return random.choice(responses)
    
    return None

def generate_emotion_based_response(emotion: str):
    """
    Generate response based on detected emotion
    
    Args:
        emotion: Detected emotion
    
    Returns:
        Response string
    """
    responses = THERAPEUTIC_RESPONSES.get(emotion, THERAPEUTIC_RESPONSES['neutral'])
    return random.choice(responses)

def generate_keyword_response(message: str):
    """
    Generate response based on specific keywords
    
    Args:
        message: User's message
    
    Returns:
        Response string or None
    """
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['help', 'struggling', 'can\'t']):
        return "I hear that you're struggling. You're brave for reaching out. What specifically is challenging you right now?"
    
    elif any(word in message_lower for word in ['anxious', 'worried', 'nervous']):
        return "Anxiety can feel overwhelming. Try this: Take 3 deep breaths with me. Inhale... hold... exhale. How do you feel now?"
    
    elif any(word in message_lower for word in ['better', 'good', 'great', 'fine']):
        return "I'm glad to hear that! What's contributing to you feeling this way?"
    
    elif any(word in message_lower for word in ['tired', 'exhausted', 'drained']):
        return "It sounds like you need some rest and self-care. Have you been taking breaks for yourself?"
    
    return None

def generate_chat_response(user_message: str, emotion_context: str = "neutral"):
    """
    Main function to generate empathetic chat response
    
    Args:
        user_message: User's input message
        emotion_context: Current emotion context
    
    Returns:
        Tuple of (response, detected_emotion, confidence)
    """
    # Detect emotion in user's message
    detected_emotion, confidence = analyze_text_emotion(user_message)
    
    if not detected_emotion:
        detected_emotion = emotion_context
        confidence = 0.5
    
    # Priority 1: Crisis detection
    if detect_crisis_language(user_message):
        response = generate_crisis_response()
        return response, detected_emotion, confidence
    
    # Priority 2: Mental health topic detection
    topic = detect_mental_health_topic(user_message)
    if topic and topic != 'self_harm':  # Already handled above
        topic_response = generate_topic_response(topic)
        if topic_response:
            return topic_response, detected_emotion, confidence
    
    # Priority 3: Keyword-based responses
    keyword_response = generate_keyword_response(user_message)
    if keyword_response:
        return keyword_response, detected_emotion, confidence
    
    # Priority 4: Emotion-based responses
    response = generate_emotion_based_response(detected_emotion)
    return response, detected_emotion, confidence
