/**
 * 個人資訊卡片元件
 */
import { useState } from 'react';
import type { PersonInfo } from '../types';

interface PersonCardProps {
  personInfo: PersonInfo;
}

export const PersonCard: React.FC<PersonCardProps> = ({ personInfo }) => {
  const [imageError, setImageError] = useState(false);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-md mx-auto">
      <div className="flex flex-col items-center">
        {/* 照片 */}
        <div className="w-32 h-32 bg-gray-200 rounded-full mb-4 flex items-center justify-center overflow-hidden">
          {personInfo.photo && !imageError ? (
            <img
              src={personInfo.photo}
              alt={personInfo.name}
              className="w-full h-full object-cover"
              onError={() => setImageError(true)}
            />
          ) : (
            <svg
              className="w-16 h-16 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
          )}
        </div>

        {/* 姓名 */}
        <h2 className="text-2xl font-bold text-gray-800 mb-2">{personInfo.name}</h2>

        {/* 其他資訊 */}
        <div className="w-full space-y-2 mt-4">
          {personInfo.student_id && (
            <div className="flex justify-between items-center py-2 border-b border-gray-200">
              <span className="text-gray-600 font-medium">學號:</span>
              <span className="text-gray-800">{personInfo.student_id}</span>
            </div>
          )}

          {personInfo.department && (
            <div className="flex justify-between items-center py-2 border-b border-gray-200">
              <span className="text-gray-600 font-medium">系所:</span>
              <span className="text-gray-800">{personInfo.department}</span>
            </div>
          )}

          {personInfo.email && (
            <div className="flex justify-between items-center py-2 border-b border-gray-200">
              <span className="text-gray-600 font-medium">Email:</span>
              <span className="text-gray-800">{personInfo.email}</span>
            </div>
          )}

          <div className="flex justify-between items-center py-2">
            <span className="text-gray-600 font-medium">ID:</span>
            <span className="text-gray-800 font-mono text-sm">{personInfo.id}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

