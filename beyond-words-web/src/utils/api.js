/**
 * API Service for backend communication
 * Centralized API calls with error handling
 */

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

/**
 * Generic fetch wrapper with error handling
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Fetch options
 * @returns {Promise<Object>} Response data
 */
const apiFetch = async (endpoint, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
};

/**
 * Health check
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  return apiFetch('/health');
};

/**
 * Analyze emotion from text
 * @param {string} text - Text to analyze
 * @returns {Promise<Object>} Emotion analysis result
 */
export const analyzeText = async (text) => {
  return apiFetch('/analyze_text', {
    method: 'POST',
    body: JSON.stringify({ text }),
  });
};

/**
 * Chat with empathetic bot
 * @param {string} message - User message
 * @param {string} emotionContext - Current emotion context
 * @returns {Promise<Object>} Chat response
 */
export const sendChatMessage = async (message, emotionContext = 'neutral') => {
  return apiFetch('/chat', {
    method: 'POST',
    body: JSON.stringify({
      message,
      emotion_context: emotionContext,
    }),
  });
};

/**
 * Predict emotion from audio file
 * @param {File|Blob} audioFile - Audio file to analyze
 * @returns {Promise<Object>} Emotion prediction result
 */
export const predictEmotionFromAudio = async (audioFile) => {
  const formData = new FormData();
  formData.append('file', audioFile);

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      body: formData,
      // Don't set Content-Type header - browser will set it with boundary
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Audio prediction error:', error);
    throw error;
  }
};

/**
 * Store conversation in database
 * @param {Object} conversationData - Conversation data to store
 * @returns {Promise<Object>} Storage confirmation
 */
export const storeConversation = async (conversationData) => {
  const params = new URLSearchParams(conversationData);
  return apiFetch(`/store_conversation?${params}`, {
    method: 'POST',
  });
};

/**
 * Get conversation history for a user
 * @param {string} userId - User ID
 * @param {number} limit - Number of conversations to retrieve
 * @returns {Promise<Object>} Conversation history
 */
export const getConversationHistory = async (userId, limit = 50) => {
  return apiFetch(`/conversation_history/${userId}?limit=${limit}`);
};

/**
 * Get emotion analytics for a user
 * @param {string} userId - User ID
 * @returns {Promise<Object>} Emotion analytics
 */
export const getEmotionAnalytics = async (userId) => {
  return apiFetch(`/emotion_analytics/${userId}`);
};

/**
 * Combined function: Predict emotion and get chat response
 * @param {File|Blob} audioFile - Audio file
 * @returns {Promise<Object>} Combined result
 */
export const analyzeAudioAndGetResponse = async (audioFile) => {
  try {
    // Step 1: Get emotion prediction
    const emotionResult = await predictEmotionFromAudio(audioFile);
    
    // Step 2: Get chat response based on emotion
    const chatResult = await sendChatMessage(
      emotionResult.transcription || "I just shared my feelings through voice",
      emotionResult.final_emotion || emotionResult.emotion
    );
    
    return {
      emotion: emotionResult,
      chat: chatResult,
      combined: true
    };
  } catch (error) {
    console.error('Combined analysis error:', error);
    throw error;
  }
};

/**
 * Test backend connection
 * @returns {Promise<boolean>} Connection status
 */
export const testConnection = async () => {
  try {
    const result = await checkHealth();
    return result.status === 'ok';
  } catch (error) {
    return false;
  }
};

export default {
  checkHealth,
  analyzeText,
  sendChatMessage,
  predictEmotionFromAudio,
  storeConversation,
  getConversationHistory,
  getEmotionAnalytics,
  analyzeAudioAndGetResponse,
  testConnection,
};
