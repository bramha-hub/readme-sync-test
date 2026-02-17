/**
 * Example JavaScript module to demonstrate README-Sync.
 * 
 * This module contains sample functions that will be parsed.
 */

/**
 * Calculate factorial of a number
 * @param {number} n - The number to calculate factorial for
 * @returns {number} The factorial of n
 */
export function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

/**
 * Fetch data from an API endpoint
 * @param {string} endpoint - API endpoint URL
 * @param {Object} options - Request options
 * @returns {Promise<Object>} Response data
 */
export async function fetchData(endpoint, options = {}) {
  const response = await fetch(endpoint, options);
  return response.json();
}

/**
 * User management class
 */
export class UserManager {
  constructor(apiUrl) {
    this.apiUrl = apiUrl;
    this.users = new Map();
  }

  /**
   * Get user by ID
   * @param {string} userId - User identifier
   * @returns {Promise<Object>} User object
   */
  async getUser(userId) {
    if (this.users.has(userId)) {
      return this.users.get(userId);
    }
    
    const user = await fetchData(`${this.apiUrl}/users/${userId}`);
    this.users.set(userId, user);
    return user;
  }

  /**
   * Create a new user
   * @param {Object} userData - User data
   * @returns {Promise<Object>} Created user
   */
  async createUser(userData) {
    const user = await fetchData(`${this.apiUrl}/users`, {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    this.users.set(user.id, user);
    return user;
  }
}

/**
 * Utility function to format dates
 * @param {Date} date - Date to format
 * @param {string} format - Format string
 * @returns {string} Formatted date
 */
export const formatDate = (date, format = 'YYYY-MM-DD') => {
  // Implementation here
  return date.toISOString().split('T')[0];
};
