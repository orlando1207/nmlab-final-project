/**
 * 結果顯示元件
 */
import { PersonCard } from './PersonCard';
import { getProcessedVideoUrl } from '../services/api';
import type { RecognitionResponse } from '../types';

interface ResultDisplayProps {
  result: RecognitionResponse | null;
  error: string | null;
}

export const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, error }) => {
  if (error) {
    return (
      <div className="mt-8 p-4 bg-red-50 border border-red-200 rounded-lg">
        <div className="flex items-center">
          <svg
            className="w-5 h-5 text-red-600 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p className="text-red-800 font-medium">錯誤: {error}</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  // 從 URL 中提取檔案名稱
  const videoFilename = result.processed_video_url.split('/').pop() || '';
  const videoUrl = getProcessedVideoUrl(videoFilename);

  return (
    <div className="mt-8">
      <div className="mb-6 text-center">
        <h3 className="text-2xl font-bold text-gray-800 mb-2">識別結果</h3>
        <p className="text-sm text-gray-600">
          檢測到 <span className="font-semibold text-blue-600">{result.total_detected}</span> 個人
        </p>
      </div>

      {/* 影片和人物卡片並排顯示 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* 處理過的影片 - 左側 */}
        <div className="bg-white rounded-lg shadow-lg p-4 lg:p-6">
          <h4 className="text-lg font-semibold text-gray-800 mb-4">處理過的影片</h4>
          <div className="w-full">
            <video
              controls
              className="w-full rounded-lg max-h-[500px] object-contain"
              src={videoUrl}
            >
              您的瀏覽器不支援影片播放
            </video>
          </div>
        </div>

        {/* 識別結果列表 - 右側 */}
        <div className="bg-white rounded-lg shadow-lg p-4 lg:p-6">
          <h4 className="text-lg font-semibold text-gray-800 mb-4">
            識別到的人員 ({result.recognition_results.length})
          </h4>
          <div className="space-y-4 max-h-[500px] overflow-y-auto">
            {result.recognition_results.map((personInfo, index) => (
              <PersonCard 
                key={`${personInfo.gallery_id}-${personInfo.person_id}-${index}`} 
                personInfo={personInfo} 
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
