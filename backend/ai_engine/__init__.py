"""
AI Neural Signal Intelligence Engine
Provides trained deep learning and feature-based Automatic Modulation Classification (AMC),
blind parameter estimation, and cloud inference connectors.
"""

from .features import extract_signal_features, FEATURE_NAMES
from .model import SignalAIModel, load_or_train_default_model
from .inference import analyze_signal_with_ai, chat_with_ai_copilot

__all__ = [
    "extract_signal_features",
    "FEATURE_NAMES",
    "SignalAIModel",
    "load_or_train_default_model",
    "analyze_signal_with_ai",
    "chat_with_ai_copilot",
]
