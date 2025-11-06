/**
 * LocalStorage utility for persistent state management
 * Handles user data, conversation history, and emotion results
 */

const STORAGE_KEYS = {
  USER_PROFILE: 'beyondWords_userProfile',
  SURVEY_DATA: 'beyondWords_surveyData',
  CONVERSATION_HISTORY: 'beyondWords_conversations',
  EMOTION_RESULTS: 'beyondWords_emotionResults',
  LAST_SESSION: 'beyondWords_lastSession'
};

/**
 * Save user profile data
 * @param {Object} profile - User profile data (email, name, etc.)
 */
export const saveUserProfile = (profile) => {
  try {
    localStorage.setItem(STORAGE_KEYS.USER_PROFILE, JSON.stringify({
      ...profile,
      updatedAt: new Date().toISOString()
    }));
    return true;
  } catch (error) {
    console.error('Failed to save user profile:', error);
    return false;
  }
};

/**
 * Get user profile data
 * @returns {Object|null} User profile or null
 */
export const getUserProfile = () => {
  try {
    const data = localStorage.getItem(STORAGE_KEYS.USER_PROFILE);
    return data ? JSON.parse(data) : null;
  } catch (error) {
    console.error('Failed to get user profile:', error);
    return null;
  }
};

/**
 * Save survey/questionnaire data
 * @param {Object} surveyData - Survey responses (gender, sleep, dayQuality, etc.)
 */
export const saveSurveyData = (surveyData) => {
  try {
    localStorage.setItem(STORAGE_KEYS.SURVEY_DATA, JSON.stringify({
      ...surveyData,
      completedAt: new Date().toISOString()
    }));
    return true;
  } catch (error) {
    console.error('Failed to save survey data:', error);
    return false;
  }
};

/**
 * Get survey data
 * @returns {Object|null} Survey data or null
 */
export const getSurveyData = () => {
  try {
    const data = localStorage.getItem(STORAGE_KEYS.SURVEY_DATA);
    return data ? JSON.parse(data) : null;
  } catch (error) {
    console.error('Failed to get survey data:', error);
    return null;
  }
};

/**
 * Add a conversation to history
 * @param {Object} conversation - Conversation object
 */
export const addConversation = (conversation) => {
  try {
    const history = getConversationHistory();
    const newConversation = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      ...conversation
    };
    
    history.unshift(newConversation);
    
    // Keep only last 100 conversations
    const trimmedHistory = history.slice(0, 100);
    
    localStorage.setItem(STORAGE_KEYS.CONVERSATION_HISTORY, JSON.stringify(trimmedHistory));
    return newConversation;
  } catch (error) {
    console.error('Failed to add conversation:', error);
    return null;
  }
};

/**
 * Get conversation history
 * @param {number} limit - Number of conversations to return
 * @returns {Array} Array of conversations
 */
export const getConversationHistory = (limit = null) => {
  try {
    const data = localStorage.getItem(STORAGE_KEYS.CONVERSATION_HISTORY);
    const history = data ? JSON.parse(data) : [];
    return limit ? history.slice(0, limit) : history;
  } catch (error) {
    console.error('Failed to get conversation history:', error);
    return [];
  }
};

/**
 * Clear conversation history
 */
export const clearConversationHistory = () => {
  try {
    localStorage.removeItem(STORAGE_KEYS.CONVERSATION_HISTORY);
    return true;
  } catch (error) {
    console.error('Failed to clear conversation history:', error);
    return false;
  }
};

/**
 * Save emotion detection result
 * @param {Object} emotionResult - Emotion analysis result
 */
export const saveEmotionResult = (emotionResult) => {
  try {
    const results = getEmotionResults();
    const newResult = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      ...emotionResult
    };
    
    results.unshift(newResult);
    
    // Keep only last 50 results
    const trimmedResults = results.slice(0, 50);
    
    localStorage.setItem(STORAGE_KEYS.EMOTION_RESULTS, JSON.stringify(trimmedResults));
    return newResult;
  } catch (error) {
    console.error('Failed to save emotion result:', error);
    return null;
  }
};

/**
 * Get emotion results history
 * @param {number} limit - Number of results to return
 * @returns {Array} Array of emotion results
 */
export const getEmotionResults = (limit = null) => {
  try {
    const data = localStorage.getItem(STORAGE_KEYS.EMOTION_RESULTS);
    const results = data ? JSON.parse(data) : [];
    return limit ? results.slice(0, limit) : results;
  } catch (error) {
    console.error('Failed to get emotion results:', error);
    return [];
  }
};

/**
 * Get emotion statistics
 * @returns {Object} Statistics about emotion distribution
 */
export const getEmotionStatistics = () => {
  try {
    const results = getEmotionResults();
    
    if (results.length === 0) {
      return {
        total: 0,
        distribution: {},
        mostCommon: null,
        averageConfidence: 0
      };
    }
    
    const distribution = {};
    let totalConfidence = 0;
    
    results.forEach(result => {
      const emotion = result.final_emotion || result.emotion;
      const confidence = result.final_confidence || result.confidence || 0;
      
      distribution[emotion] = (distribution[emotion] || 0) + 1;
      totalConfidence += confidence;
    });
    
    const mostCommon = Object.keys(distribution).reduce((a, b) => 
      distribution[a] > distribution[b] ? a : b
    );
    
    return {
      total: results.length,
      distribution,
      mostCommon,
      averageConfidence: totalConfidence / results.length
    };
  } catch (error) {
    console.error('Failed to get emotion statistics:', error);
    return {
      total: 0,
      distribution: {},
      mostCommon: null,
      averageConfidence: 0
    };
  }
};

/**
 * Save session data (current state)
 * @param {Object} sessionData - Current session data
 */
export const saveSession = (sessionData) => {
  try {
    localStorage.setItem(STORAGE_KEYS.LAST_SESSION, JSON.stringify({
      ...sessionData,
      savedAt: new Date().toISOString()
    }));
    return true;
  } catch (error) {
    console.error('Failed to save session:', error);
    return false;
  }
};

/**
 * Get last session data
 * @returns {Object|null} Session data or null
 */
export const getSession = () => {
  try {
    const data = localStorage.getItem(STORAGE_KEYS.LAST_SESSION);
    return data ? JSON.parse(data) : null;
  } catch (error) {
    console.error('Failed to get session:', error);
    return null;
  }
};

/**
 * Clear all stored data
 */
export const clearAllData = () => {
  try {
    Object.values(STORAGE_KEYS).forEach(key => {
      localStorage.removeItem(key);
    });
    return true;
  } catch (error) {
    console.error('Failed to clear all data:', error);
    return false;
  }
};

/**
 * Export all data for backup
 * @returns {Object} All stored data
 */
export const exportAllData = () => {
  try {
    return {
      userProfile: getUserProfile(),
      surveyData: getSurveyData(),
      conversations: getConversationHistory(),
      emotionResults: getEmotionResults(),
      lastSession: getSession(),
      exportedAt: new Date().toISOString()
    };
  } catch (error) {
    console.error('Failed to export data:', error);
    return null;
  }
};

/**
 * Import data from backup
 * @param {Object} data - Data to import
 */
export const importData = (data) => {
  try {
    if (data.userProfile) {
      saveUserProfile(data.userProfile);
    }
    if (data.surveyData) {
      saveSurveyData(data.surveyData);
    }
    if (data.conversations) {
      localStorage.setItem(STORAGE_KEYS.CONVERSATION_HISTORY, JSON.stringify(data.conversations));
    }
    if (data.emotionResults) {
      localStorage.setItem(STORAGE_KEYS.EMOTION_RESULTS, JSON.stringify(data.emotionResults));
    }
    if (data.lastSession) {
      saveSession(data.lastSession);
    }
    return true;
  } catch (error) {
    console.error('Failed to import data:', error);
    return false;
  }
};

export default {
  saveUserProfile,
  getUserProfile,
  saveSurveyData,
  getSurveyData,
  addConversation,
  getConversationHistory,
  clearConversationHistory,
  saveEmotionResult,
  getEmotionResults,
  getEmotionStatistics,
  saveSession,
  getSession,
  clearAllData,
  exportAllData,
  importData
};
