/**
 * TypeScript 類型定義
 */

export interface PersonInfo {
  gallery_id: string;
  person_id: string;
  name: string;
  photo_url?: string;
  Department?: string;
  Year_in_school?: string;
  // 向後兼容欄位
  id?: string;
  photo?: string;
  department?: string;
  student_id?: string;
  email?: string;
}

export interface RecognitionResult {
  probe_id: string;
  gallery_id: string;
  person_info: PersonInfo;
}

export interface RecognitionResponse {
  probe_id: string;
  processed_video_url: string;
  recognition_results: PersonInfo[];
  total_detected: number;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
}

