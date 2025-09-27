import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { FaFileUpload, FaSpinner, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';

const UploadTranscriptPage = () => {
  const { user } = useAuth();
  const [selectedFile, setSelectedFile] = useState(null);
  const [transcriptText, setTranscriptText] = useState('');
  const [error, setError] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check if the file is a text file or JSON file
      if (file.type === 'application/json' || file.type === 'text/plain' || file.name.endsWith('.txt') || file.name.endsWith('.json')) {
        setSelectedFile(file);
        setError('');
        
        // Read file content
        const reader = new FileReader();
        reader.onload = (event) => {
          setTranscriptText(event.target.result);
        };
        reader.readAsText(file);
      } else {
        setSelectedFile(null);
        setError('Error: Please upload a valid .txt or .json file.');
      }
    }
  };

  const handleTextChange = (e) => {
    setTranscriptText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!transcriptText.trim()) {
      setError('Please provide transcript text or upload a file.');
      return;
    }

    setIsUploading(true);
    setError('');
    setUploadStatus('uploading');

    try {
      const response = await fetch('/api/transcript/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          transcript_text: transcriptText,
          meeting_id: 'demo-meeting-001', // In real app, this would come from context
          file_name: selectedFile ? selectedFile.name : 'manual-input'
        }),
      });

      const result = await response.json();

      if (result.success) {
        setUploadStatus('success');
        setAnalysisResult(result.analysis_result);
        setTranscriptText('');
        setSelectedFile(null);
      } else {
        setUploadStatus('error');
        setError(result.error || 'Failed to analyze transcript');
      }
    } catch (err) {
      setUploadStatus('error');
      setError('Network error: ' + err.message);
    } finally {
      setIsUploading(false);
    }
  };

  const renderAnalysisResults = () => {
    if (!analysisResult) return null;

    const { key_topics, action_items, key_insights, sentiment_analysis, business_metrics } = analysisResult;

    return (
      <div className="analysis-results">
        <h3>📊 Analysis Results</h3>
        
        {/* Sentiment Analysis */}
        <div className="analysis-section">
          <h4>Sentiment Analysis</h4>
          <div className="sentiment-metrics">
            <div className="metric">
              <span className="metric-label">Overall Sentiment:</span>
              <span className={`metric-value sentiment-${sentiment_analysis?.overall_sentiment || 'neutral'}`}>
                {sentiment_analysis?.overall_sentiment || 'neutral'}
              </span>
            </div>
            <div className="metric">
              <span className="metric-label">Relationship Health:</span>
              <span className="metric-value">
                {Math.round((sentiment_analysis?.relationship_health_score || 0.5) * 100)}%
              </span>
            </div>
            <div className="metric">
              <span className="metric-label">Meeting Effectiveness:</span>
              <span className="metric-value">
                {Math.round((business_metrics?.meeting_effectiveness_score || 0.5) * 100)}%
              </span>
            </div>
          </div>
        </div>

        {/* Key Topics */}
        {key_topics && key_topics.length > 0 && (
          <div className="analysis-section">
            <h4>Key Topics Discussed</h4>
            <ul className="topics-list">
              {key_topics.map((topic, index) => (
                <li key={index} className={`topic-item priority-${topic.importance}`}>
                  <strong>{topic.topic}</strong>
                  <span className="topic-importance">({topic.importance})</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Action Items */}
        {action_items && action_items.length > 0 && (
          <div className="analysis-section">
            <h4>Action Items</h4>
            <div className="action-items-list">
              {action_items.map((item, index) => (
                <div key={index} className={`action-item priority-${item.priority}`}>
                  <div className="action-header">
                    <strong>{item.title}</strong>
                    <span className="action-priority">{item.priority}</span>
                  </div>
                  {item.description && <p className="action-description">{item.description}</p>}
                  {item.assigned_to && <p className="action-assigned">Assigned to: {item.assigned_to}</p>}
                  {item.due_date && <p className="action-due">Due: {item.due_date}</p>}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Key Insights */}
        {key_insights && key_insights.length > 0 && (
          <div className="analysis-section">
            <h4>Key Insights</h4>
            <div className="insights-list">
              {key_insights.map((insight, index) => (
                <div key={index} className={`insight-item impact-${insight.impact}`}>
                  <div className="insight-header">
                    <strong>{insight.insight}</strong>
                    <span className="insight-category">{insight.category}</span>
                  </div>
                  <span className="insight-impact">Impact: {insight.impact}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <>
      <header className="app-header">
        <h2 className="page-subtitle">Upload Meeting Transcript</h2>
      </header>
      <div className="upload-container">
        <form onSubmit={handleSubmit}>
          <p>Upload a transcript file or paste the transcript text below for AI-powered analysis.</p>
          
          {/* File Upload Section */}
          <div className="upload-section">
            <h4>Option 1: Upload File</h4>
            <input 
              type="file"
              id="file-upload"
              onChange={handleFileChange}
              accept=".txt,.json"
              style={{ display: 'none' }}
            />
            
            <label htmlFor="file-upload" className="button-secondary upload-label">
              <FaFileUpload />
              Choose File (.txt or .json)
            </label>
            
            {selectedFile && <p className="file-selected">Selected: <strong>{selectedFile.name}</strong></p>}
          </div>

          {/* Text Input Section */}
          <div className="text-input-section">
            <h4>Option 2: Paste Transcript Text</h4>
            <textarea
              value={transcriptText}
              onChange={handleTextChange}
              placeholder="Paste your meeting transcript here..."
              rows={10}
              className="transcript-textarea"
            />
          </div>
          
          {/* Error Display */}
          {error && (
            <div className="error-message">
              <FaExclamationTriangle />
              {error}
            </div>
          )}

          {/* Upload Status */}
          {uploadStatus === 'uploading' && (
            <div className="upload-status uploading">
              <FaSpinner className="spinning" />
              Analyzing transcript...
            </div>
          )}

          {uploadStatus === 'success' && (
            <div className="upload-status success">
              <FaCheckCircle />
              Transcript analyzed successfully!
            </div>
          )}

          {uploadStatus === 'error' && (
            <div className="upload-status error">
              <FaExclamationTriangle />
              Analysis failed
            </div>
          )}
          
          <button 
            type="submit" 
            className="button-primary" 
            disabled={!transcriptText.trim() || isUploading}
          >
            {isUploading ? 'Analyzing...' : 'Analyze Transcript'}
          </button>
        </form>

        {/* Analysis Results */}
        {analysisResult && renderAnalysisResults()}
      </div>
    </>
  );
};

export default UploadTranscriptPage;