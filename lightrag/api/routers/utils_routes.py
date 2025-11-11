"""
This module contains utility routes for the LightRAG API.
"""

import traceback
from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Dict, List, Literal, Optional
from lightrag.ragmanager import RAGManager
from lightrag.utils import logger
from lightrag.api.utils_api import get_combined_auth_dependency
from ..config import global_args

# Create API router
router = APIRouter(
    prefix="/utils",
    tags=["utils"],
    responses={404: {"description": "Not found"}},
)

#这里的rag是lightRAG的实例，要使用RAGAnything的实例，需要从RAGManager.get_rag()中获取
def create_utils_router(rag, api_key: Optional[str] = None):
    """
    Create and configure the utils router.
    
    Args:
        api_key: Optional API key for authentication
        
    Returns:
        APIRouter: Configured utility routes
    """
    # Get authentication dependency with api_key
    combined_auth = get_combined_auth_dependency(api_key)
    
    @router.get(
        "/test",
        response_model=Dict[str, Any],
        dependencies=[Depends(combined_auth)],
    )
    async def test_endpoint() -> Dict[str, Any]:
        """
        Test endpoint for utility routes.
        
        This is a simple test endpoint that returns a success message.
        
        Returns:
            Dict[str, Any]: A dictionary containing a success message
            
        Raises:
            HTTPException: If an error occurs (500)
        """
        try:
            return {
                "status": "success",
                "message": "Utility routes are working correctly",
                "info": "This is a test endpoint for utility functions"
            }
        except Exception as e:
            logger.error(f"Error in test endpoint: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))
    
    return router
