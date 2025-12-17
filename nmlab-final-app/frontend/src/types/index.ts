/**
 * TypeScript 類型定義
 */

export interface PersonInfo {
  id: string;
  name: string;
  photo: string;
  department?: string;
  student_id?: string;
  email?: string;
}

export interface RecognitionResult {
  probe_id: string;
  gallery_id: string;
  person_info: PersonInfo;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
}

