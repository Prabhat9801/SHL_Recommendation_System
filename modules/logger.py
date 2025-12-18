"""
Logger Module
Centralized logging configuration with file writing
"""
import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(name: str, log_file: str = None, level=logging.INFO) -> logging.Logger:
    """
    Setup logger with console and file handlers
    
    Args:
        name: Logger name (usually __name__)
        log_file: Optional log file path
        level: Logging level
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use mode='a' for append, and set up immediate flushing
        file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        
        # Force immediate flush
        file_handler.flush = lambda: file_handler.stream.flush()
        
        logger.addHandler(file_handler)
    
    # Prevent propagation to avoid duplicate logs
    logger.propagate = False
    
    return logger

# Default logger for the application (with file logging enabled)
default_log_file = f"logs/shl_recommender_{datetime.now().strftime('%Y%m%d')}.log"
logger = setup_logger('shl_recommender', default_log_file)

# Also create a custom logging function that ensures file flush
def log_and_flush(logger, level, message):
    """Log message and immediately flush to file"""
    logger.log(level, message)
    # Flush all handlers
    for handler in logger.handlers:
        handler.flush()
