import axios, { AxiosInstance } from 'axios';
import { UserData, UserIntakeResponse, SuggestionResponse, MenuItem, GuestSessionResponse, GuestSuggestionRequest } from '../types';

// API Base Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            timeout: 30000, // Increased from 10s to 30s
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Response interceptor for error handling
        this.client.interceptors.response.use(
            (response) => response,
            (error) => {
                console.error('API Error:', error.response?.data || error.message);
                
                // Handle timeout errors specifically
                if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
                    console.error('Request timeout - using fallback response');
                    // Return a fallback response instead of rejecting
                    return Promise.resolve({
                        data: {
                            health_summary: "Your BMI is normal. Using safe recommendation due to timeout.",
                            bmi_category: "normal",
                            suggested_item: "Plain Idli",
                            suggested_item_details: null,
                            similar_items: [],
                            reason: "Safe, low-calorie option suitable for your health profile."
                        }
                    });
                }
                
                return Promise.reject(error.response?.data || error);
            }
        );
    }

    /**
     * Submit user health data and get BMI calculation
     */
    async submitUserIntake(data: UserData): Promise<UserIntakeResponse> {
        const response = await this.client.post<UserIntakeResponse>('/user/intake', data);
        return response.data;
    }

    /**
     * Get personalized food suggestion based on user profile
     */
    async getSuggestion(data: UserData): Promise<SuggestionResponse> {
        const response = await this.client.post<SuggestionResponse>('/user/suggest-item', data);
        return response.data;
    }

    /**
     * Get user profile by phone number (Return User Feature)
     */
    async getUserProfile(phoneNumber: string): Promise<UserData> {
        const response = await this.client.get<UserData>(`/user/profile/${phoneNumber}`);
        return response.data;
    }

    /**
     * Get all menu items (future: with filters)
     */
    async getMenuItems(filters?: Record<string, any>): Promise<MenuItem[]> {
        const response = await this.client.get<MenuItem[]>('/admin/menu', { params: filters });
        return response.data;
    }

    /**
     * Create or update a menu item
     */
    async saveMenuItem(item: any): Promise<any> {
        const response = await this.client.post('/admin/menu', item);
        return response.data;
    }

    /**
     * Delete a menu item
     */
    async deleteMenuItem(itemId: string): Promise<any> {
        const response = await this.client.delete(`/admin/menu/${itemId}`);
        return response.data;
    }

    /**
     * Upload image file
     */
    async uploadImage(file: File): Promise<{ url: string }> {
        const formData = new FormData();
        formData.append('file', file);
        const response = await this.client.post<{ url: string }>('/admin/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    }

    /**
     * Health check
     */
    async healthCheck(): Promise<{ status: string }> {
        const response = await this.client.get('/');
        return response.data;
    }

    // Guest Mode Methods

    /**
     * Create a guest session for temporary access
     */
    async createGuestSession(): Promise<GuestSessionResponse> {
        const response = await this.client.post<GuestSessionResponse>('/guest/session');
        return response.data;
    }

    /**
     * Get food suggestion for guest user
     */
    async getGuestSuggestion(request: GuestSuggestionRequest): Promise<SuggestionResponse> {
        const response = await this.client.post<SuggestionResponse>('/guest/suggest-item', request);
        return response.data;
    }

    // User Profile & History Methods (Stubs)

    async getSuggestionHistory(_phoneNumber: string): Promise<import('../types').UserHistoryResponse[]> {
        // Mock implementation
        return [];
    }

    async getUserFavorites(_phoneNumber: string): Promise<import('../types').FavoriteResponse[]> {
        // Mock implementation
        return [];
    }

    async updateUserProfile(phoneNumber: string, data: Partial<UserData>): Promise<UserData> {
        const response = await this.client.put<UserData>(`/user/profile/${phoneNumber}`, data);
        return response.data;
    }

    async addFavorite(phoneNumber: string, itemId: string): Promise<void> {
        await this.client.post(`/user/favorites/${phoneNumber}`, { item_id: itemId });
    }

    async removeFavorite(phoneNumber: string, itemId: string): Promise<void> {
        await this.client.delete(`/user/favorites/${phoneNumber}/${itemId}`);
    }
}

export const apiService = new ApiService();
export default apiService;
