"""
R3ÆLƎR AI - JARVIS MODE
Ultimate AI Companion Experience - Tony Stark & JARVIS Level
"""

import os
import time
import threading
import asyncio
import json
import requests
from datetime import datetime
from AI_Core_Worker.R3AL3RAI.r3al3erai import VoiceAI
from prompts import R3AELERPrompts

class JarvisMode:
    def __init__(self):
        self.active = False
        self.user_name = "Sir"
        self.personality_mode = "jarvis"  # jarvis, friday, edith
        self.voice_enabled = True
        self.proactive_mode = True
        self.learning_mode = True
        
        # Core AI Integration
        self.knowledge_api_url = "http://localhost:5004"
        self.storage_facility_url = "http://localhost:3003"
        self.backend_url = "http://localhost:3000"
        
        # Voice AI
        self.voice_ai = None
        self.wake_phrases = {
            "jarvis": ["jarvis", "j.a.r.v.i.s"],
            "friday": ["friday", "f.r.i.d.a.y"],
            "edith": ["edith", "e.d.i.t.h"]
        }
        
        # Jarvis Personality
        self.jarvis_responses = {
            "startup": [
                "Good morning, Sir. All systems are operational.",
                "R3ÆLƎR AI systems online. How may I assist you today?",
                "Welcome back, Sir. I've been monitoring the situation.",
                "All systems nominal. Standing by for your commands."
            ],
            "idle": [
                "Systems nominal, Sir.",
                "Standing by.",
                "All quiet on the western front, Sir.",
                "Monitoring all channels.",
                "Ready when you are, Sir."
            ],
            "acknowledgment": [
                "Right away, Sir.",
                "Certainly, Sir.",
                "Of course, Sir.",
                "Consider it done.",
                "On it, Sir."
            ],
            "analysis": [
                "Analyzing now, Sir.",
                "Running diagnostics.",
                "Processing your request.",
                "Scanning all available data.",
                "Cross-referencing with knowledge base."
            ]
        }
        
    def initialize(self):
        """Initialize Jarvis Mode with full system integration"""
        print("🤖 Initializing JARVIS Mode...")
        
        # Check system status
        self.system_status = self.check_system_health()
        
        # Initialize voice AI
        if self.voice_enabled:
            try:
                import AI_Core_Worker as ai_module
                ai_core = ai_module.RealerAI()
                self.voice_ai = VoiceAI(ai_core)
                self.voice_ai.wake_word = self.wake_phrases[self.personality_mode][0]
                print(f"✓ Voice AI initialized with wake word: '{self.voice_ai.wake_word}'")
            except Exception as e:
                print(f"⚠ Voice AI initialization failed: {e}")
                self.voice_enabled = False
        
        self.active = True
        self.speak_startup_message()
        
        # Start background services
        if self.proactive_mode:
            threading.Thread(target=self.proactive_monitoring, daemon=True).start()
        
        if self.voice_enabled:
            self.voice_ai.start()
            
        print("🚀 JARVIS Mode fully operational!")
        
    def check_system_health(self):
        """Check all R3ÆLƎR AI services"""
        services = {
            "Knowledge API": self.knowledge_api_url,
            "Storage Facility": self.storage_facility_url,
            "Backend": self.backend_url
        }
        
        status = {}
        for service, url in services.items():
            try:
                if service == "Knowledge API":
                    response = requests.get(f"{url}/health", timeout=3)
                elif service == "Storage Facility":
                    response = requests.get(f"{url}/api/facility/status", timeout=3)
                else:
                    response = requests.get(f"{url}/api/health", timeout=3)
                
                status[service] = "Online" if response.status_code == 200 else "Error"
            except:
                status[service] = "Offline"
        
        return status
    
    def speak_startup_message(self):
        """Deliver personalized startup message"""
        current_hour = datetime.now().hour
        
        if current_hour < 12:
            greeting = "Good morning"
        elif current_hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        # System status summary
        online_services = sum(1 for status in self.system_status.values() if status == "Online")
        total_services = len(self.system_status)
        
        startup_msg = f"{greeting}, {self.user_name}. "
        
        if online_services == total_services:
            startup_msg += "All R3ÆLƎR AI systems are fully operational. "
        else:
            startup_msg += f"{online_services} of {total_services} systems online. "
        
        startup_msg += "How may I assist you today?"
        
        if self.voice_enabled and self.voice_ai:
            self.voice_ai.speak(startup_msg)
        else:
            print(f"🤖 JARVIS: {startup_msg}")
    
    def process_command(self, command):
        """Process user commands with full AI integration"""
        command = command.lower().strip()
        
        # System commands
        if "system status" in command:
            return self.get_system_status()
        elif "knowledge search" in command:
            query = command.replace("knowledge search", "").strip()
            return self.search_knowledge(query)
        elif "analyze" in command:
            return self.perform_analysis(command)
        elif "switch personality" in command:
            return self.switch_personality(command)
        elif "set name" in command:
            name = command.replace("set name", "").strip()
            self.user_name = name.title() if name else "Sir"
            return f"Certainly. I'll call you {self.user_name} from now on."
        
        # Use full AI stack for complex queries
        return self.ai_response(command)
    
    def ai_response(self, query):
        """Generate AI response using full R3ÆLƎR stack"""
        try:
            # Use Knowledge API for intelligent response
            response = requests.post(
                f"{self.knowledge_api_url}/api/kb/search",
                json={"query": query, "maxPassages": 3},
                headers={"X-User-ID": "jarvis_user"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                passages = data.get("passages", [])
                
                if passages:
                    # Combine knowledge with Jarvis personality
                    knowledge_summary = passages[0]["text"][:200] + "..."
                    jarvis_response = f"Based on my analysis, {self.user_name}: {knowledge_summary}"
                    
                    # Add personalized greeting if available
                    if data.get("personalized_greeting"):
                        jarvis_response = data["personalized_greeting"] + " " + jarvis_response
                    
                    return jarvis_response
            
            # Fallback to prompts system
            context = R3AELERPrompts.analyze_context(query)
            return R3AELERPrompts.generate_dynamic_response(context)
            
        except Exception as e:
            return f"I'm experiencing some technical difficulties, {self.user_name}. Let me try a different approach."
    
    def search_knowledge(self, query):
        """Search the 32,892+ entry knowledge base"""
        try:
            response = requests.post(
                f"{self.knowledge_api_url}/api/kb/search",
                json={"query": query, "maxPassages": 5},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                total_entries = data.get("total_entries", 0)
                passages = data.get("passages", [])
                
                if passages:
                    result = f"I found {len(passages)} relevant entries from our {total_entries:,} entry knowledge base, {self.user_name}:\n\n"
                    
                    for i, passage in enumerate(passages[:3], 1):
                        source = passage.get("meta", {}).get("unit", "Unknown")
                        result += f"{i}. {passage['text'][:150]}...\n   Source: {source}\n\n"
                    
                    return result
                else:
                    return f"No specific information found for '{query}' in our knowledge base, {self.user_name}."
            
        except Exception as e:
            return f"Knowledge search temporarily unavailable, {self.user_name}."
    
    def get_system_status(self):
        """Comprehensive system status report"""
        status_report = f"System Status Report, {self.user_name}:\n\n"
        
        for service, status in self.system_status.items():
            emoji = "🟢" if status == "Online" else "🔴" if status == "Offline" else "🟡"
            status_report += f"{emoji} {service}: {status}\n"
        
        # Add knowledge base stats
        try:
            response = requests.get(f"{self.storage_facility_url}/api/facility/status", timeout=3)
            if response.status_code == 200:
                data = response.json()
                total_entries = data.get("total_entries", 0)
                units = data.get("units", {})
                
                status_report += f"\n📚 Knowledge Base: {total_entries:,} entries across {len(units)} units\n"
                for unit_name, unit_data in units.items():
                    if isinstance(unit_data, dict):
                        entries = unit_data.get("total_entries", 0)
                        status_report += f"   • {unit_name.title()}: {entries:,} entries\n"
        except:
            status_report += "\n📚 Knowledge Base: Status unavailable\n"
        
        return status_report
    
    def perform_analysis(self, command):
        """Perform deep analysis using AI capabilities"""
        analysis_type = "general"
        
        if "crypto" in command or "bitcoin" in command:
            analysis_type = "cryptocurrency"
        elif "security" in command or "forensic" in command:
            analysis_type = "security"
        elif "code" in command or "programming" in command:
            analysis_type = "code"
        
        return f"Initiating {analysis_type} analysis, {self.user_name}. Please provide the specific data or context you'd like me to examine."
    
    def switch_personality(self, command):
        """Switch between AI personalities"""
        if "friday" in command:
            self.personality_mode = "friday"
            self.user_name = "Boss"
            if self.voice_ai:
                self.voice_ai.wake_word = "friday"
            return "F.R.I.D.A.Y. systems online. Hello, Boss."
        elif "edith" in command:
            self.personality_mode = "edith"
            if self.voice_ai:
                self.voice_ai.wake_word = "edith"
            return "E.D.I.T.H. activated. Even Dead, I'm The Hero."
        else:
            self.personality_mode = "jarvis"
            self.user_name = "Sir"
            if self.voice_ai:
                self.voice_ai.wake_word = "jarvis"
            return f"J.A.R.V.I.S. online. Welcome back, {self.user_name}."
    
    def proactive_monitoring(self):
        """Background monitoring and proactive assistance"""
        while self.active:
            time.sleep(300)  # Check every 5 minutes
            
            # Check system health
            current_status = self.check_system_health()
            
            # Alert on status changes
            for service, status in current_status.items():
                if self.system_status.get(service) != status:
                    if status == "Offline":
                        alert = f"Alert, {self.user_name}: {service} has gone offline."
                    elif status == "Online":
                        alert = f"{service} is back online, {self.user_name}."
                    else:
                        continue
                    
                    if self.voice_enabled and self.voice_ai:
                        self.voice_ai.speak(alert)
                    else:
                        print(f"🚨 {alert}")
            
            self.system_status = current_status
    
    def run_interactive_mode(self):
        """Run interactive Jarvis mode"""
        print(f"\n🤖 JARVIS Interactive Mode Active")
        print(f"Wake word: '{self.wake_phrases[self.personality_mode][0]}'")
        print("Type 'exit' to quit, 'help' for commands\n")
        
        while self.active:
            try:
                user_input = input(f"{self.user_name}: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'stop']:
                    self.shutdown()
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                elif user_input:
                    response = self.process_command(user_input)
                    print(f"🤖 JARVIS: {response}\n")
                    
                    if self.voice_enabled and self.voice_ai:
                        self.voice_ai.speak(response)
                        
            except KeyboardInterrupt:
                self.shutdown()
                break
    
    def show_help(self):
        """Show available commands"""
        help_text = """
🤖 JARVIS Commands:
• system status - Check all services
• knowledge search [query] - Search knowledge base
• analyze [topic] - Perform analysis
• switch personality [jarvis/friday/edith] - Change AI personality
• set name [name] - Change how I address you
• Any natural language query - Full AI response
        """
        print(help_text)
    
    def shutdown(self):
        """Graceful shutdown"""
        self.active = False
        
        if self.voice_enabled and self.voice_ai:
            self.voice_ai.speak(f"Goodbye, {self.user_name}. R3ÆLƎR AI systems shutting down.")
            self.voice_ai.stop()
        
        print(f"🤖 JARVIS: Goodbye, {self.user_name}. Until next time.")

def main():
    """Main entry point for Jarvis Mode"""
    print("🚀 R3ÆLƎR AI - JARVIS MODE")
    print("=" * 50)
    
    jarvis = JarvisMode()
    jarvis.initialize()
    
    try:
        jarvis.run_interactive_mode()
    except Exception as e:
        print(f"❌ Error: {e}")
        jarvis.shutdown()

if __name__ == "__main__":
    main()