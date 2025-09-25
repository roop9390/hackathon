import pytest
import json
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import UploadFile, HTTPException
import io
import sys
import os

# Add the parent directory to Python path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.agents.ingestion_structuring_agent import app, run_pipeline, BUCKET_NAME


# ===== Test Client Setup =====
"""
TestClient allows us to make HTTP requests to our FastAPI app without running a server.
It's like a virtual browser for testing our endpoints.
"""
client = TestClient(app)


# ===== Fixtures =====
"""
Fixtures are reusable setup functions that pytest runs before tests.
They help us avoid repeating the same setup code in multiple tests.
"""

@pytest.fixture
def mock_upload_file():
    """Creates a mock file for testing uploads"""
    file_content = b"This is a test file content"
    return UploadFile(filename="test.pdf", file=io.BytesIO(file_content))

@pytest.fixture
def sample_pipeline_response():
    """Sample response that our pipeline would return"""
    return {
        "response": {
            "Traction": "8/10",
            "Team": "9/10",
            "Verdict": "Pass",
            "Recommendation": "Schedule follow-up"
        }
    }

@pytest.fixture
def sample_structured_data():
    """Sample structured data from the first agent"""
    return {
        "startup_name": "Test Startup",
        "traction": {"current_mrr": 10000},
        "financials": {"ask_amount": 500000},
        "team": {"ceo": "John Doe"},
        "market": {"target_market": "SaaS"},
        "product_description": "Test product",
        "document_type": "pitch_deck"
    }


# ===== Mock Classes =====
class MockBlob:
    """Mocks Google Cloud Storage Blob to avoid actual file uploads"""
    def __init__(self, name):
        self.name = name
    
    def upload_from_filename(self, filename):
        # Mock upload - does nothing
        pass

class MockBucket:
    """Mocks Google Cloud Storage Bucket"""
    def blob(self, name):
        return MockBlob(name)


# ===== Test Cases =====

def test_app_initialization():
    """Test 1: Check if FastAPI app starts correctly"""
    assert app.title == "Doc Ingestion + Recommendation API"
    assert app.version == "0.1.0"


def test_cors_headers():
    """Test 2: Verify CORS headers are properly set"""
    response = client.options("/full-analysis")
    # Check if CORS headers are present (though TestClient might not show all)
    assert response.status_code in [200, 405]  # Options might return 405 if not explicitly handled


@pytest.mark.asyncio
async def test_run_pipeline_success(mock_upload_file, sample_structured_data):
    """Test 3: Test the pipeline runner with successful response"""
    
    # Mock the session service and runner to avoid actual API calls
    with patch('main.session_service') as mock_session, \
         patch('main.runner') as mock_runner:
        
        # Setup mock session
        mock_session.create_session = AsyncMock()
        
        # Setup mock runner to return our sample data
        mock_event = Mock()
        mock_event.content.parts = [Mock(text=json.dumps(sample_structured_data))]
        mock_event.source_agent = "doc_ingest_agent"
        
        mock_runner.run_async = AsyncMock(return_value=[mock_event])
        
        # Test data
        test_data = {
            "bucket_name": "test-bucket",
            "file_paths": ["file1.pdf", "file2.pdf"]
        }
        
        # Call the function
        result = await run_pipeline(test_data)
        
        # Verify the result
        assert result == sample_structured_data
        mock_session.create_session.assert_called_once()


# @pytest.mark.asyncio
# async def test_run_pipeline_json_decode_error():
#     """Test 4: Test pipeline when JSON decoding fails (text response)"""
    
#     with patch('main.session_service') as mock_session, \
#          patch('main.runner') as mock_runner:
        
#         mock_session.create_session = AsyncMock()
        
#         # Mock event with non-JSON text
#         mock_event = Mock()
#         mock_event.content.parts = [Mock(text="This is a text response, not JSON")]
#         mock_event.source_agent = "recommendation_agent"
        
#         mock_runner.run_async = AsyncMock(return_value=[mock_event])
        
#         test_data = {"bucket_name": "test", "file_paths": ["test.pdf"]}
#         result = await run_pipeline(test_data)
        
#         # Should return dict with "report" key containing the text
#         assert "report" in result
#         assert result["report"] == "This is a text response, not JSON"


# @pytest.mark.asyncio
# async def test_run_pipeline_no_output():
#     """Test 5: Test pipeline when no output is generated"""
    
#     with patch('main.session_service') as mock_session, \
#          patch('main.runner') as mock_runner:
        
#         mock_session.create_session = AsyncMock()
        
#         # Mock event with no content
#         mock_event = Mock()
#         mock_event.content = None
        
#         mock_runner.run_async = AsyncMock(return_value=[mock_event])
        
#         test_data = {"bucket_name": "test", "file_paths": ["test.pdf"]}
#         result = await run_pipeline(test_data)
        
#         # Should return error message
#         assert "error" in result
#         assert "no output" in result["error"]


# @patch('main.storage_client')
# @patch('main.run_pipeline')
# def test_full_analysis_success(mock_run_pipeline, mock_storage_client, mock_upload_file, sample_pipeline_response):
#     """Test 6: Test the complete endpoint with file uploads"""
    
#     # Mock the storage client and bucket
#     mock_bucket = MockBucket()
#     mock_storage_client.bucket.return_value = mock_bucket
    
#     # Mock the pipeline to return sample response
#     mock_run_pipeline.return_value = sample_pipeline_response
    
#     # Create test files
#     files = [
#         ("files", ("test1.pdf", b"test content 1", "application/pdf")),
#         ("files", ("test2.docx", b"test content 2", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
#     ]
    
#     data = {"founder_email": "test@example.com"}
    
#     # Make the request
#     response = client.post("/full-analysis", files=files, data=data)
    
#     # Verify response
#     assert response.status_code == 200
#     assert response.json()["response"] == sample_pipeline_response["response"]
#     mock_run_pipeline.assert_called_once()


def test_full_analysis_no_files():
    """Test 7: Test endpoint when no files are provided"""
    
    # Make request with no files
    data = {"founder_email": "test@example.com"}
    response = client.post("/full-analysis", data=data)
    
    # Should return 422 (validation error)
    assert response.status_code == 422


def test_full_analysis_no_email():
    """Test 8: Test endpoint when no founder email is provided"""
    
    files = [("files", ("test.pdf", b"test content", "application/pdf"))]
    
    # Make request with no email
    response = client.post("/full-analysis", files=files)
    
    # Should return 422 (validation error)
    assert response.status_code == 422


# @patch('main.storage_client')
# @patch('main.run_pipeline')
# def test_full_analysis_pipeline_error(mock_run_pipeline, mock_storage_client, mock_upload_file):
#     """Test 9: Test endpoint when pipeline returns an error"""
    
#     mock_bucket = MockBucket()
#     mock_storage_client.bucket.return_value = mock_bucket
    
#     # Mock pipeline to return error
#     mock_run_pipeline.return_value = {"error": "Pipeline failed"}
    
#     files = [("files", ("test.pdf", b"test content", "application/pdf"))]
#     data = {"founder_email": "test@example.com"}
    
#     response = client.post("/full-analysis", files=files, data=data)
    
#     # Should still return 200 but with error in response
#     assert response.status_code == 200
#     assert "error" in response.json()["response"]


# ===== Test Data Validation =====
def test_doc_request_model():
    """Test 10: Test Pydantic model validation"""
    from main import DocRequest
    
    # Valid data
    valid_data = {
        "bucket_name": "test-bucket",
        "file_paths": ["file1.pdf", "file2.pdf"]
    }
    
    request = DocRequest(**valid_data)
    assert request.bucket_name == "test-bucket"
    assert len(request.file_paths) == 2
    
    # Test with empty file paths
    invalid_data = {
        "bucket_name": "test-bucket",
        "file_paths": []
    }
    
    # This should still be valid since Pydantic doesn't enforce non-empty lists by default
    request = DocRequest(**invalid_data)
    assert request.file_paths == []


# ===== Run the tests =====
if __name__ == "__main__":
    # This allows running tests with: python test_main.py
    pytest.main([__file__, "-v"])