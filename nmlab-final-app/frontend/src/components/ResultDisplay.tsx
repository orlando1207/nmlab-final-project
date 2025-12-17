/**
 * 結果顯示元件
 */
import { PersonCard } from './PersonCard';
import type { RecognitionResult } from '../types';

interface ResultDisplayProps {
  result: RecognitionResult | null;
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

  return (
    <div className="mt-8">
      <div className="mb-4 text-center">
        <h3 className="text-xl font-semibold text-gray-800 mb-2">識別結果</h3>
        <p className="text-sm text-gray-600">
          Probe ID: <span className="font-mono">{result.probe_id}</span> → Gallery ID:{' '}
          <span className="font-mono">{result.gallery_id}</span>
        </p>
      </div>
      <PersonCard personInfo={result.person_info} />
    </div>
  );
};

