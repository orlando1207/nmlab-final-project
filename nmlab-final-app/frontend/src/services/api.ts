/**
 * API 服務層
 */
import axios from 'axios';
import type { RecognitionResult, PersonInfo } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 分鐘超時（處理影片可能需要時間）
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

/**
 * 上傳影片並進行識別
 */
export const uploadVideo = async (file: File): Promise<RecognitionResult> => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await apiClient.post<RecognitionResult>('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.code === 'ECONNREFUSED' || error.message.includes('ERR_CONNECTION_REFUSED')) {
        throw new Error('無法連接到後端服務，請確認後端服務已啟動（http://localhost:8000）');
      }
      throw new Error(
        error.response?.data?.detail || error.message || '上傳失敗'
      );
    }
    throw error;
  }
};

/**
 * 取得個人資訊
 */
export const getPersonInfo = async (personId: string): Promise<PersonInfo> => {
  try {
    const response = await apiClient.get<PersonInfo>(`/api/person/${personId}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        error.response?.data?.detail || error.message || '取得個人資訊失敗'
      );
    }
    throw error;
  }
};

/**
 * 健康檢查
 */
export const healthCheck = async (): Promise<{ status: string; message: string }> => {
  try {
    const response = await apiClient.get('/api/health');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.code === 'ECONNREFUSED' || error.message.includes('ERR_CONNECTION_REFUSED')) {
        throw new Error('無法連接到後端服務，請確認後端服務已啟動（http://localhost:8000）');
      }
      throw new Error(error.response?.data?.detail || error.message || '無法連接到後端服務');
    }
    throw new Error('無法連接到後端服務');
  }
};

