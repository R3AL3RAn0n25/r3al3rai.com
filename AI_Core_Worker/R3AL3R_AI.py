"""
R3ÆLƎR AI: Complete Enhanced Framework (FIXED & PRODUCTION-READY)
Main orchestrator with proper imports, shutdown handling, and robustness
"""

import time
import threading
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import os
import sys
import hashlib

# === CORE COMPONENT IMPORTS (MUST BE AT TOP!) ===
from AI_Core_Worker.core import Core
from knowledge_base import KnowledgeBase
from AI_Core_Worker.security_manager import SecurityManager
from AI_Core_Worker.memory_manager import MemoryManager
from math_reasoning_enhancement import MathReasoningEnhancer
from voice_assistant import VoiceAssistant
from system_agent import SystemAgent

# === OTHER PROJECT IMPORTS ===
from AI_Core_Worker.intelligence_layer import get_intelligence_layer
from AI_Core_Worker.self_hosted_storage_facility import StorageFacility
from AI_Core_Worker.knowledge_api import app as knowledge_app
import AI_Core_Worker as ai_module
from prompts import R3AELERPrompts

# Optional advanced AI modules (graceful fallback)
try:
    from activity_tracker import ActivityTracker
    from personalization_engine import PersonalizationEngine
    from recommendation_engine import RecommendationEngine
    from self_learning_engine import SelfLearningEngine
    from evolution_engine import EvolutionEngine
    AI_MODULES_AVAILABLE = True
except ImportError as e:
    logging.getLogger(__name__).warning(f"Advanced AI modules not available: {e}")
    AI_MODULES_AVAILABLE = False

# === Logging Setup ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("R3ÆLƎR_AI")

class R3AL3R_AI:
    """
    Fixed & Robust R3ÆLƎR AI Orchestrator
    """

    def __init__(self):
        self.components = {}
        self.threads: List[threading.Thread] = []
        self.running = False
        self._stop_event = threading.Event()  # For graceful shutdown
        self.agent = SystemAgent()
        self.memory = MemoryManager()
        self.evolution = EvolutionEngine()
        self.voice = None
        try:
            self.voice = VoiceAssistant(self)      # Pass the whole instance
            self.voice.start()
        except Exception as e:
            logger.warning(f"Voice assistant not available: {e}")
            self.voice = None

        # Initialize all components safely
        self._init_storage()
        self._init_core()
        self._init_intelligence()
        self._init_knowledge()
        self._init_security()
        self._init_memory()
        self._init_math_enhancement()

        logger.info("R3ÆLƎR AI initialized successfully with all components")

    def _init_storage(self):
        try:
            self.components['storage'] = StorageFacility()
            logger.info("StorageFacility initialized")
        except Exception as e:
            logger.error(f"Failed to initialize StorageFacility: {e}")
            self.components['storage'] = None

    def _init_core(self):
        try:
            self.components['core'] = Core()
            logger.info("Core component initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Core: {e}")

    def _init_intelligence(self):
        try:
            self.components['intelligence'] = get_intelligence_layer()
            logger.info("Intelligence layer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Intelligence Layer: {e}")

    def _init_knowledge(self):
        try:
            # Pass storage if available
            storage = self.components.get('storage')
            self.components['knowledge'] = KnowledgeBase(storage_facility=storage)
            logger.info("KnowledgeBase initialized")
        except Exception as e:
            logger.error(f"Failed to initialize KnowledgeBase: {e}")

    def _init_security(self):
        try:
            self.components['security'] = SecurityManager()
            logger.info("SecurityManager initialized")
        except Exception as e:
            logger.error(f"Failed to initialize SecurityManager: {e}")

    def _init_memory(self):
        try:
            self.components['memory'] = MemoryManager()
            logger.info("MemoryManager initialized")
        except Exception as e:
            logger.error(f"Failed to initialize MemoryManager: {e}")

    def _init_math_enhancement(self):
        try:
            storage = self.components.get('storage')
            self.components['math_enhancement'] = MathReasoningEnhancer(storage_facility=storage)
            logger.info("MathReasoningEnhancer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize MathReasoningEnhancer: {e}")

    def start(self):
        if self.running:
            logger.warning("R3ÆLƎR AI is already running")
            return

        self.running = True
        self._stop_event.clear()
        self.threads = []  # Reset thread list

        logger.info("Starting R3ÆLƎR AI system...")

        # Core processing loop
        if self.components.get('core'):
            t = threading.Thread(target=self._run_core, name="CoreLoop", daemon=False)
            t.start()
            self.threads.append(t)

        # Intelligence background processing
        if self.components.get('intelligence'):
            t = threading.Thread(target=self._run_intelligence, name="IntelligenceLoop", daemon=False)
            t.start()
            self.threads.append(t)

        # Knowledge API (Flask) with graceful shutdown
        t = threading.Thread(target=self._run_knowledge_api, name="KnowledgeAPI", daemon=False)
        t.start()
        self.threads.append(t)

        logger.info("R3ÆLƎR AI system started successfully")

    def stop(self):
        if not self.running:
            return

        logger.info("Stopping R3ÆLƎR AI system...")
        self.running = False
        self._stop_event.set()

        # Wait for threads to finish
        for t in self.threads:
            t.join(timeout=10)

        logger.info("R3ÆLƎR AI system stopped gracefully")

    def _run_core(self):
        while not self._stop_event.is_set():
            try:
                self.components['core'].process()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Core processing error: {e}")
                time.sleep(5)

    def _run_intelligence(self):
        while not self._stop_event.is_set():
            try:
                intel = self.components.get('intelligence')
                if intel and hasattr(intel, 'background_task'):
                    intel.background_task()
                time.sleep(15)
            except Exception as e:
                logger.error(f"Intelligence loop error: {e}")
                time.sleep(10)

    def __del__(self):
        self.stop()

    def _run_knowledge_api(self):
        """Run Flask API with proper shutdown support"""
        try:
            from werkzeug.serving import make_server
            from contextlib import closing

            server = make_server('0.0.0.0', 5004, knowledge_app, threaded=True)
            ctx = (server,)

            def run_server():
                try:
                    server.serve_forever()
                except:
                    pass

            api_thread = threading.Thread(target=run_server, name="FlaskServer")
            api_thread.start()

            # Wait for shutdown signal
            while not self._stop_event.is_set():
                time.sleep(1)

            logger.info("Shutting down Knowledge API...")
            server.shutdown()
            api_thread.join(timeout=5)

        except Exception as e:
            logger.error(f"Knowledge API failed: {e}")

        try:
            # 1. Security validation
            security = self.components.get('security')
            if security and not security.validate_request(query, user_id):
                return {"error": "Request blocked by security policy"}

            # 2. Intent
            intel = self.components.get('intelligence')
            intent = intel.classify_intent(query) if intel else "general"

            # 3. Memory context
            memory = self.components.get('memory')
            context = memory.get_context(user_id, query) if memory else ""

            # 4. Knowledge search
            kb = self.components.get('knowledge')
            knowledge_results = kb.search(query, user_id) if kb else []

            # 5. External aggregation
            external_data = intel.aggregate_external_data(query) if intel else []

            # 6. Generate response
            core = self.components.get('core')
            if not core:
                return {"error": "Core AI engine not available"}

            response = core.generate_response(
                query=query,
                intent={"intent": intent, "confidence": 0.85},
                context=context,
                knowledge=knowledge_results,
                external_data=external_data,
                user_id=user_id
            )

            # 7. Math enhancement (smarter trigger)
            math_enhancer = self.components.get('math_enhancement')
            if math_enhancer and self._is_math_query(query):
                enhanced = math_enhancer.enhance_mathematical_reasoning(query)
                if enhanced.get('enhanced_reasoning'):
                    response += f"\n\nMathematical Solution:\n{enhanced['enhanced_reasoning']}"

            # 8. Store in memory
            if memory:
                memory.store_interaction(user_id, query, response)

            return {
                "response": response,
                "intent": intent,
                "knowledge_used": len(knowledge_results),
                "external_sources": len(external_data),
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Query processing failed: {e}", exc_info=True)
            return {"error": "Internal processing error", "details": str(e)}

    def _is_math_query(self, query: str) -> bool:
        """Smarter math detection"""
        lower = query.lower()
        math_signals = [
            'solve ', 'calculate ', 'what is ', 'find x', 'equation', 'prove that',
            '=', 'x=', 'y=', '+', '-', '*', '/', '^', '∫', '√', 'log(', 'sin(', 'cos('
        ]
        return any(sig in lower for sig in math_signals if sig in lower)

    def get_system_status(self) -> Dict[str, Any]:
        status = {
            "system": "R3ÆLƎR AI",
            "running": self.running,
            "uptime_seconds": time.time() - getattr(self, '_start_time', time.time()),
            "components": {},
            "timestamp": datetime.now().isoformat()
        }
        for name, comp in self.components.items():
            try:
                if comp and hasattr(comp, 'get_status'):
                    status["components"][name] = comp.get_status()
                else:
                    status["components"][name] = "active" if comp else "missing"
            except Exception as e:
                status["components"][name] = f"error: {e}"
        return status

    def optimize_system(self):
        logger.info("Running system optimization...")
        for name, comp in self.components.items():
            if comp and hasattr(comp, 'optimize'):
                try:
                    comp.optimize() # Call optimize method if exists    
                except Exception as e:
                    logger.error(f"Optimization failed for {name}: {e}")
        logger.info("System optimization completed")

    def get_component(self, name: str):
        return self.components.get(name)
    
    def process_query(self, query: str) -> str:
        """Voice entry point — uses your full real brain"""
        query = query.lower().strip()

        # === SYSTEM AGENT COMMANDS (list files, git, etc.) ===
        if query.startswith("list files"):
            path = query.replace("list files", "").strip() or "."
            try:
                files = os.listdir(path)
                return f"{len(files)} items in folder: {', '.join(files[:12])}..."
            except Exception as e:
                return f"Access error: {e}"

        if "git status" in query:
            result = os.popen("git status --short").read()
            return f"Git status:\n{result or 'Clean working tree'}"

        # === YOUR REAL CORE AI WITH ALL REQUIRED ARGS ===
        core = self.components.get('core')
        if core and hasattr(core, 'generate_response'):
            # Pull real context, knowledge, external data
            context = ""
            knowledge = []
            external_data = []

            if self.components.get('memory'):
                context = self.components['memory'].get_context("voice_user", query)

            if self.components.get('knowledge'):
                knowledge = self.components['knowledge'].search(query, "voice_user")

            if self.components.get('intelligence'):
                external_data = self.components['intelligence'].aggregate_external_data(query)

            result = core.generate_response(
                query=query,
                user_id="voice_user",
                intent="general",
                context=context,
                knowledge=knowledge,
                external_data=external_data
            )

            if isinstance(result, dict):
                return result.get("response", "I'm thinking...")
            return str(result)

        # Final fallback
        return "R3AL3RAI online and ready."

if __name__ == "__main__":
    ai = R3AL3R_AI()           # Creates the full system
    ai.start()                  # Starts Flask APIs + core loop + voice (JARVIS mode)
    
    print("R3AL3RAI fully online — say 'Riller' + command")
    
    try:
        while True:
            time.sleep(1)       # Keeps the script alive
    except KeyboardInterrupt:
        print("\nShutting down R3AL3RAI...")
        ai.stop()               # Graceful shutdown of everything