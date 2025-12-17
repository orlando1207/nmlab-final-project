/**
 * 影片上傳元件
 */
import { useState, useRef } from 'react';
import { uploadVideo } from '../services/api';
import type { RecognitionResult } from '../types';

interface VideoUploadProps {
  onResult: (result: RecognitionResult) => void;
  onError: (error: string) => void;
}

export const VideoUpload: React.FC<VideoUploadProps> = ({ onResult, onError }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // 驗證檔案類型
      if (!file.name.toLowerCase().endsWith('.mp4')) {
        onError('僅支援 .mp4 格式的影片檔案');
        return;
      }
      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      onError('請先選擇影片檔案');
      return;
    }

    setIsUploading(true);
    try {
      const result = await uploadVideo(selectedFile);
      onResult(result);
      // 重置檔案選擇
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      onError(error instanceof Error ? error.message : '上傳失敗');
    } finally {
      setIsUploading(false);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();

    const file = e.dataTransfer.files?.[0];
    if (file) {
      if (!file.name.toLowerCase().endsWith('.mp4')) {
        onError('僅支援 .mp4 格式的影片檔案');
        return;
      }
      setSelectedFile(file);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".mp4"
          onChange={handleFileChange}
          className="hidden"
          id="video-upload"
          disabled={isUploading}
        />
        <label
          htmlFor="video-upload"
          className="cursor-pointer flex flex-col items-center"
        >
          <svg
            className="w-12 h-12 text-gray-400 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
          <span className="text-gray-600 mb-2">
            {selectedFile ? selectedFile.name : '點擊或拖曳影片檔案到此處'}
          </span>
          <span className="text-sm text-gray-400">僅支援 .mp4 格式</span>
        </label>
      </div>

      {selectedFile && (
        <div className="mt-4 flex justify-center">
          <button
            onClick={handleUpload}
            disabled={isUploading}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {isUploading ? '處理中...' : '上傳並識別'}
          </button>
        </div>
      )}

      {isUploading && (
        <div className="mt-4 text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">正在處理影片，請稍候...</p>
        </div>
      )}
    </div>
  );
};

