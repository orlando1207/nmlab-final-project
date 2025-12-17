/**
 * 主應用程式元件
 */
import { useState } from 'react';
import { VideoUpload } from './components/VideoUpload';
import { ResultDisplay } from './components/ResultDisplay';
import type { RecognitionResponse } from './types';

function App() {
  const [result, setResult] = useState<RecognitionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleResult = (recognitionResponse: RecognitionResponse) => {
    setResult(recognitionResponse);
    setError(null);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* 標題 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            步態識別系統
          </h1>
          <p className="text-gray-600">Gait Recognition System</p>
        </div>

        {/* 上傳區域 */}
        <VideoUpload onResult={handleResult} onError={handleError} />

        {/* 結果顯示 */}
        <ResultDisplay result={result} error={error} />
      </div>
    </div>
  );
}

export default App;

