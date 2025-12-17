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

  // 處理照片 URL（支援多種欄位名稱）
  const photoUrl = personInfo.photo_url || personInfo.photo || '';
  const department = personInfo.Department || personInfo.department || '';
  const yearInSchool = personInfo.Year_in_school || personInfo.Year_in_school || '';

  return (
    <div className="bg-gray-50 rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow border border-gray-200">
      <div className="flex flex-row items-start gap-4">
        {/* 照片 */}
        <div className="w-20 h-20 bg-gray-200 rounded-full flex-shrink-0 flex items-center justify-center overflow-hidden">
          {photoUrl && !imageError ? (
            <img
              src={photoUrl}
              alt={personInfo.name}
              className="w-full h-full object-cover"
              onError={() => setImageError(true)}
            />
          ) : (
            <svg
              className="w-10 h-10 text-gray-400"
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

        {/* 資訊區域 */}
        <div className="flex-1 min-w-0">
          {/* 姓名 */}
          <h2 className="text-lg font-bold text-gray-800 mb-2">{personInfo.name}</h2>

          {/* 其他資訊 */}
          <div className="space-y-1.5">
            {department && (
              <div className="flex items-center gap-2">
                <span className="text-gray-600 text-sm">系所:</span>
                <span className="text-gray-800 text-sm">{department}</span>
              </div>
            )}

            {yearInSchool && (
              <div className="flex items-center gap-2">
                <span className="text-gray-600 text-sm">年級:</span>
                <span className="text-gray-800 text-sm">{yearInSchool}</span>
              </div>
            )}

            <div className="flex items-center gap-2 pt-1 border-t border-gray-200">
              <span className="text-gray-500 text-xs font-mono">{personInfo.gallery_id}/{personInfo.person_id}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
