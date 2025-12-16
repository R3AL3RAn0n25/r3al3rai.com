#!/usr/bin/env python3
"""
R3ÆLƎR Management System - Standalone Desktop Application
Local desktop interface for R3AL3R AI management without web dependencies
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import subprocess
import sys
import os
import json
import time
import logging
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
import webbrowser

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'AI_Core_Worker'))
sys.path.insert(0, os.path.join(current_dir, 'Tools'))

# Import R3AL3R components
try:
    from core import Core
    CORE_AVAILABLE = True
except ImportError:
    Core = None
    CORE_AVAILABLE = False

try:
    from AI_Core_Worker.enhanced_knowledge_api import intelligence
    INTELLIGENCE_AVAILABLE = True
except ImportError:
    intelligence = None
    INTELLIGENCE_AVAILABLE = False

try:
    from AI_Core_Worker.vector_engine import VectorEngine
    VECTOR_ENGINE_AVAILABLE = True
except ImportError:
    VectorEngine = None
    VECTOR_ENGINE_AVAILABLE = False

try:
    from Tools.tools.wallet_analyzer import WalletAnalyzer
    WALLET_ANALYZER_AVAILABLE = True
except ImportError:
    WalletAnalyzer = None
    WALLET_ANALYZER_AVAILABLE = False

try:
    from Tools.blackarch_tools_manager import BlackArchToolsManager
    BLACKARCH_AVAILABLE = True
except ImportError:
    BlackArchToolsManager = None
    BLACKARCH_AVAILABLE = False

class R3AL3RDesktopApp:
    """Main R3AL3R Management System Desktop Application"""

    def __init__(self, root):
        self.root = root
        self.root.title("R3ÆLƎR Management System v2.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')

        # Initialize components
        self.core = None
        self.vector_engine = None
        self.wallet_analyzer = None
        self.blackarch_manager = None
        self.db_connection = None

        # Setup logging
        self.setup_logging()

        # Create main interface
        self.create_main_interface()

        # Initialize components in background
        self.init_components_async()

    def setup_logging(self):
        """Setup logging for the application"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('r3aler_desktop.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def create_main_interface(self):
        """Create the main application interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create tabs
        self.create_dashboard_tab()
        self.create_ai_management_tab()
        self.create_knowledge_tab()
        self.create_wallet_analysis_tab()
        self.create_blackarch_tab()
        self.create_database_tab()
        self.create_settings_tab()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("R3ÆLƎR Management System Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_dashboard_tab(self):
        """Create the main dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")

        # Title
        title_label = tk.Label(dashboard_frame, text="R3ÆLƎR Management System",
                              font=('Arial', 20, 'bold'), bg='#1a1a2e', fg='white')
        title_label.pack(pady=20)

        # System status section
        status_frame = ttk.LabelFrame(dashboard_frame, text="System Status")
        status_frame.pack(fill='x', padx=20, pady=10)

        # Status indicators
        self.ai_status = tk.Label(status_frame, text="AI Core: Initializing...",
                                 font=('Arial', 10), fg='orange')
        self.ai_status.pack(anchor='w', padx=10, pady=2)

        self.knowledge_status = tk.Label(status_frame, text="Knowledge API: Initializing...",
                                        font=('Arial', 10), fg='orange')
        self.knowledge_status.pack(anchor='w', padx=10, pady=2)

        self.database_status = tk.Label(status_frame, text="Database: Initializing...",
                                       font=('Arial', 10), fg='orange')
        self.database_status.pack(anchor='w', padx=10, pady=2)

        # Quick actions
        actions_frame = ttk.LabelFrame(dashboard_frame, text="Quick Actions")
        actions_frame.pack(fill='x', padx=20, pady=10)

        # Action buttons
        button_frame = ttk.Frame(actions_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Start AI Core", command=self.start_ai_core).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Start Knowledge API", command=self.start_knowledge_api).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Open Web Interface", command=self.open_web_interface).grid(row=0, column=2, padx=5, pady=5)

        # System info
        info_frame = ttk.LabelFrame(dashboard_frame, text="System Information")
        info_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.system_info_text = scrolledtext.ScrolledText(info_frame, height=15, width=80)
        self.system_info_text.pack(fill='both', expand=True, padx=10, pady=10)

        # Update system info
        self.update_system_info()

    def create_ai_management_tab(self):
        """Create AI management tab"""
        ai_frame = ttk.Frame(self.notebook)
        self.notebook.add(ai_frame, text="AI Management")

        # AI Control section
        control_frame = ttk.LabelFrame(ai_frame, text="AI Core Control")
        control_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(control_frame, text="Initialize AI Core", command=self.init_ai_core).pack(side='left', padx=5, pady=5)
        ttk.Button(control_frame, text="Test AI Response", command=self.test_ai_response).pack(side='left', padx=5, pady=5)
        ttk.Button(control_frame, text="Run Benchmarks", command=self.run_benchmarks).pack(side='left', padx=5, pady=5)

        # AI Query section
        query_frame = ttk.LabelFrame(ai_frame, text="AI Query Interface")
        query_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Query input
        ttk.Label(query_frame, text="Query:").pack(anchor='w', padx=10)
        self.ai_query_text = scrolledtext.ScrolledText(query_frame, height=5, width=80)
        self.ai_query_text.pack(fill='x', padx=10, pady=5)

        # Response output
        ttk.Label(query_frame, text="Response:").pack(anchor='w', padx=10)
        self.ai_response_text = scrolledtext.ScrolledText(query_frame, height=15, width=80)
        self.ai_response_text.pack(fill='both', expand=True, padx=10, pady=5)

        # Query button
        ttk.Button(query_frame, text="Submit Query", command=self.submit_ai_query).pack(pady=10)

    def create_knowledge_tab(self):
        """Create knowledge management tab"""
        knowledge_frame = ttk.Frame(self.notebook)
        self.notebook.add(knowledge_frame, text="Knowledge Base")

        # Search section
        search_frame = ttk.LabelFrame(knowledge_frame, text="Knowledge Search")
        search_frame.pack(fill='x', padx=20, pady=10)

        # Search input
        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(search_input_frame, text="Search Query:").pack(side='left')
        self.knowledge_query_var = tk.StringVar()
        ttk.Entry(search_input_frame, textvariable=self.knowledge_query_var, width=50).pack(side='left', padx=5)
        ttk.Button(search_input_frame, text="Search", command=self.search_knowledge).pack(side='left', padx=5)

        # Results section
        results_frame = ttk.LabelFrame(knowledge_frame, text="Search Results")
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.knowledge_results_text = scrolledtext.ScrolledText(results_frame, height=20, width=80)
        self.knowledge_results_text.pack(fill='both', expand=True, padx=10, pady=10)

        # Knowledge management
        manage_frame = ttk.LabelFrame(knowledge_frame, text="Knowledge Management")
        manage_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(manage_frame, text="Add Knowledge", command=self.add_knowledge).pack(side='left', padx=5, pady=5)
        ttk.Button(manage_frame, text="Import Dataset", command=self.import_dataset).pack(side='left', padx=5, pady=5)
        ttk.Button(manage_frame, text="Export Knowledge", command=self.export_knowledge).pack(side='left', padx=5, pady=5)

    def create_wallet_analysis_tab(self):
        """Create wallet analysis tab"""
        wallet_frame = ttk.Frame(self.notebook)
        self.notebook.add(wallet_frame, text="Wallet Analysis")

        # Wallet input section
        input_frame = ttk.LabelFrame(wallet_frame, text="Wallet Analysis Input")
        input_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(input_frame, text="Wallet Address/File:").pack(anchor='w', padx=10, pady=5)
        self.wallet_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.wallet_input_var, width=60).pack(fill='x', padx=10, pady=5)

        button_frame = ttk.Frame(input_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Browse File", command=self.browse_wallet_file).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Analyze Address", command=self.analyze_wallet_address).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Extract Keys", command=self.extract_wallet_keys).pack(side='left', padx=5)

        # Results section
        results_frame = ttk.LabelFrame(wallet_frame, text="Analysis Results")
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.wallet_results_text = scrolledtext.ScrolledText(results_frame, height=20, width=80)
        self.wallet_results_text.pack(fill='both', expand=True, padx=10, pady=10)

    def create_blackarch_tab(self):
        """Create BlackArch tools tab"""
        blackarch_frame = ttk.Frame(self.notebook)
        self.notebook.add(blackarch_frame, text="BlackArch Tools")

        # Tools management
        tools_frame = ttk.LabelFrame(blackarch_frame, text="Tool Management")
        tools_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(tools_frame, text="Initialize BlackArch", command=self.init_blackarch).pack(side='left', padx=5, pady=5)
        ttk.Button(tools_frame, text="Update Tools", command=self.update_blackarch_tools).pack(side='left', padx=5, pady=5)
        ttk.Button(tools_frame, text="Launch Web Interface", command=self.launch_blackarch_web).pack(side='left', padx=5, pady=5)

        # Available tools list
        list_frame = ttk.LabelFrame(blackarch_frame, text="Available Tools")
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Tools listbox
        self.tools_listbox = tk.Listbox(list_frame, height=15, width=50)
        self.tools_listbox.pack(fill='both', expand=True, padx=10, pady=10)

        # Tool actions
        actions_frame = ttk.Frame(list_frame)
        actions_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(actions_frame, text="Execute Selected Tool", command=self.execute_selected_tool).pack(side='left', padx=5)
        ttk.Button(actions_frame, text="View Tool Info", command=self.view_tool_info).pack(side='left', padx=5)

        # Tool output
        output_frame = ttk.LabelFrame(blackarch_frame, text="Tool Output")
        output_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.tool_output_text = scrolledtext.ScrolledText(output_frame, height=10, width=80)
        self.tool_output_text.pack(fill='both', expand=True, padx=10, pady=10)

    def create_database_tab(self):
        """Create database management tab"""
        db_frame = ttk.Frame(self.notebook)
        self.notebook.add(db_frame, text="Database")

        # Connection section
        conn_frame = ttk.LabelFrame(db_frame, text="Database Connection")
        conn_frame.pack(fill='x', padx=20, pady=10)

        # Connection inputs
        conn_input_frame = ttk.Frame(conn_frame)
        conn_input_frame.pack(pady=10)

        ttk.Label(conn_input_frame, text="Host:").grid(row=0, column=0, padx=5, pady=2)
        self.db_host_var = tk.StringVar(value="localhost")
        ttk.Entry(conn_input_frame, textvariable=self.db_host_var, width=20).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(conn_input_frame, text="Port:").grid(row=1, column=0, padx=5, pady=2)
        self.db_port_var = tk.StringVar(value="5432")
        ttk.Entry(conn_input_frame, textvariable=self.db_port_var, width=20).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(conn_input_frame, text="Database:").grid(row=2, column=0, padx=5, pady=2)
        self.db_name_var = tk.StringVar(value="r3aler_ai")
        ttk.Entry(conn_input_frame, textvariable=self.db_name_var, width=20).grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(conn_input_frame, text="User:").grid(row=3, column=0, padx=5, pady=2)
        self.db_user_var = tk.StringVar(value="r3aler_user_2025")
        ttk.Entry(conn_input_frame, textvariable=self.db_user_var, width=20).grid(row=3, column=1, padx=5, pady=2)

        ttk.Label(conn_input_frame, text="Password:").grid(row=4, column=0, padx=5, pady=2)
        self.db_pass_var = tk.StringVar()
        ttk.Entry(conn_input_frame, textvariable=self.db_pass_var, width=20, show="*").grid(row=4, column=1, padx=5, pady=2)

        ttk.Button(conn_input_frame, text="Connect", command=self.connect_database).grid(row=5, column=0, columnspan=2, pady=10)

        # Query section
        query_frame = ttk.LabelFrame(db_frame, text="Database Query")
        query_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Query input
        ttk.Label(query_frame, text="SQL Query:").pack(anchor='w', padx=10)
        self.db_query_text = scrolledtext.ScrolledText(query_frame, height=8, width=80)
        self.db_query_text.pack(fill='x', padx=10, pady=5)

        # Query buttons
        button_frame = ttk.Frame(query_frame)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Execute Query", command=self.execute_query).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Show Tables", command=self.show_tables).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Backup Database", command=self.backup_database).pack(side='left', padx=5)

        # Results section
        results_frame = ttk.LabelFrame(db_frame, text="Query Results")
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.db_results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.db_results_text.pack(fill='both', expand=True, padx=10, pady=10)

    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")

        # API Settings
        api_frame = ttk.LabelFrame(settings_frame, text="API Configuration")
        api_frame.pack(fill='x', padx=20, pady=10)

        # API settings inputs
        settings_input_frame = ttk.Frame(api_frame)
        settings_input_frame.pack(pady=10)

        ttk.Label(settings_input_frame, text="Storage Facility URL:").grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.storage_url_var = tk.StringVar(value="http://localhost:5003")
        ttk.Entry(settings_input_frame, textvariable=self.storage_url_var, width=40).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(settings_input_frame, text="Knowledge API URL:").grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.knowledge_url_var = tk.StringVar(value="http://localhost:5001")
        ttk.Entry(settings_input_frame, textvariable=self.knowledge_url_var, width=40).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(settings_input_frame, text="Enhanced API Port:").grid(row=2, column=0, padx=5, pady=2, sticky='e')
        self.enhanced_port_var = tk.StringVar(value="5010")
        ttk.Entry(settings_input_frame, textvariable=self.enhanced_port_var, width=40).grid(row=2, column=1, padx=5, pady=2)

        # Save settings button
        ttk.Button(settings_input_frame, text="Save Settings", command=self.save_settings).grid(row=3, column=0, columnspan=2, pady=10)

        # System actions
        actions_frame = ttk.LabelFrame(settings_frame, text="System Actions")
        actions_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(actions_frame, text="Check System Health", command=self.check_system_health).pack(side='left', padx=5, pady=5)
        ttk.Button(actions_frame, text="View Logs", command=self.view_logs).pack(side='left', padx=5, pady=5)
        ttk.Button(actions_frame, text="Restart Services", command=self.restart_services).pack(side='left', padx=5, pady=5)

        # About section
        about_frame = ttk.LabelFrame(settings_frame, text="About")
        about_frame.pack(fill='both', expand=True, padx=20, pady=10)

        about_text = """R3ÆLƎR Management System v2.0

A comprehensive AI-powered management system featuring:

• Advanced AI Core with quantum-inspired algorithms
• Intelligent Knowledge Base with vector search
• Cryptocurrency wallet analysis tools
• BlackArch security tools integration
• PostgreSQL database management
• User authentication and security
• Real-time monitoring and analytics

Built for the future of AI-driven management."""

        about_label = tk.Label(about_frame, text=about_text, justify='left', font=('Arial', 10))
        about_label.pack(padx=20, pady=20)

    # ========== FUNCTIONALITY METHODS ==========

    def init_components_async(self):
        """Initialize components in background thread"""
        def init_worker():
            try:
                # Initialize AI Core
                self.status_var.set("Initializing AI Core...")
                if CORE_AVAILABLE:
                    self.core = Core()
                    self.ai_status.config(text="AI Core: Ready", fg='green')
                else:
                    self.ai_status.config(text="AI Core: Not Available", fg='orange')

                # Initialize Vector Engine
                if VECTOR_ENGINE_AVAILABLE:
                    self.vector_engine = VectorEngine()
                    self.knowledge_status.config(text="Knowledge API: Ready", fg='green')
                else:
                    self.knowledge_status.config(text="Knowledge API: Not Available", fg='orange')

                # Initialize Wallet Analyzer
                if WALLET_ANALYZER_AVAILABLE:
                    self.wallet_analyzer = WalletAnalyzer()
                    self.logger.info("Wallet Analyzer initialized")
                else:
                    self.logger.warning("Wallet Analyzer not available")

                # Initialize BlackArch Manager
                if BLACKARCH_AVAILABLE:
                    self.blackarch_manager = BlackArchToolsManager()
                    self.update_tools_list()
                else:
                    self.logger.warning("BlackArch Manager not available")

                # Try database connection
                self.connect_database()
                self.database_status.config(text="Database: Connected", fg='green')

                self.status_var.set("All systems initialized successfully")

            except Exception as e:
                self.logger.error(f"Component initialization error: {e}")
                self.status_var.set(f"Initialization error: {str(e)}")

        threading.Thread(target=init_worker, daemon=True).start()

    def update_system_info(self):
        """Update system information display"""
        info = f"""R3ÆLƎR Management System - System Information
{'='*50}

Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Python Version: {sys.version}
Working Directory: {os.getcwd()}

System Components:
• AI Core: {'Ready' if self.core else 'Not Initialized'}
• Knowledge API: {'Ready' if self.vector_engine else 'Not Initialized'}
• Wallet Analyzer: {'Ready' if self.wallet_analyzer else 'Not Initialized'}
• BlackArch Tools: {'Ready' if self.blackarch_manager else 'Not Initialized'}
• Database: {'Connected' if self.db_connection else 'Not Connected'}

Available Features:
• AI-powered query processing
• Intelligent knowledge search
• Cryptocurrency wallet analysis
• Security tools integration
• Database management
• User authentication

For more information, visit the documentation or use the help system."""
        self.system_info_text.delete(1.0, tk.END)
        self.system_info_text.insert(tk.END, info)

    # AI Management Methods
    def init_ai_core(self):
        """Initialize AI Core"""
        if not CORE_AVAILABLE:
            messagebox.showerror("Error", "AI Core component not available")
            return

        try:
            if not self.core:
                self.core = Core()
            self.ai_status.config(text="AI Core: Ready", fg='green')
            messagebox.showinfo("Success", "AI Core initialized successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize AI Core: {str(e)}")

    def test_ai_response(self):
        """Test AI response"""
        if not CORE_AVAILABLE or not self.core:
            messagebox.showerror("Error", "AI Core not initialized")
            return

        # Simple test query
        test_query = "Hello, can you introduce yourself?"
        try:
            response = self.core.process_query(test_query)
            self.ai_response_text.delete(1.0, tk.END)
            self.ai_response_text.insert(tk.END, f"Query: {test_query}\n\nResponse: {response}")
        except Exception as e:
            messagebox.showerror("Error", f"AI test failed: {str(e)}")

    def submit_ai_query(self):
        """Submit AI query"""
        if not CORE_AVAILABLE or not self.core:
            messagebox.showerror("Error", "AI Core not initialized")
            return

        query = self.ai_query_text.get(1.0, tk.END).strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a query")
            return

        try:
            self.status_var.set("Processing AI query...")
            response = self.core.process_query(query)
            self.ai_response_text.delete(1.0, tk.END)
            self.ai_response_text.insert(tk.END, f"Query: {query}\n\nResponse:\n{response}")
            self.status_var.set("AI query completed")
        except Exception as e:
            messagebox.showerror("Error", f"AI query failed: {str(e)}")
            self.status_var.set("AI query failed")

    # Knowledge Management Methods
    def search_knowledge(self):
        """Search knowledge base"""
        query = self.knowledge_query_var.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query")
            return

        try:
            self.status_var.set("Searching knowledge base...")
            if self.vector_engine:
                results = self.vector_engine.hybrid_search(query, "knowledge", 10)
            else:
                # Fallback to basic search
                results = {"results": f"Basic search for: {query}"}

            self.knowledge_results_text.delete(1.0, tk.END)
            self.knowledge_results_text.insert(tk.END, json.dumps(results, indent=2))
            self.status_var.set("Knowledge search completed")
        except Exception as e:
            messagebox.showerror("Error", f"Knowledge search failed: {str(e)}")

    # Wallet Analysis Methods
    def browse_wallet_file(self):
        """Browse for wallet file"""
        filename = filedialog.askopenfilename(
            title="Select Wallet File",
            filetypes=[("All files", "*.*"), ("Wallet files", "*.dat;*.wallet")]
        )
        if filename:
            self.wallet_input_var.set(filename)

    def analyze_wallet_address(self):
        """Analyze wallet address"""
        address = self.wallet_input_var.get().strip()
        if not address:
            messagebox.showwarning("Warning", "Please enter a wallet address")
            return

        try:
            self.status_var.set("Analyzing wallet address...")
            if self.wallet_analyzer:
                results = self.wallet_analyzer.analyze_address(address)
            else:
                results = {"error": "Wallet analyzer not available"}

            self.wallet_results_text.delete(1.0, tk.END)
            self.wallet_results_text.insert(tk.END, json.dumps(results, indent=2))
            self.status_var.set("Wallet analysis completed")
        except Exception as e:
            messagebox.showerror("Error", f"Wallet analysis failed: {str(e)}")

    # BlackArch Methods
    def update_tools_list(self):
        """Update BlackArch tools list"""
        if self.blackarch_manager:
            try:
                tools = self.blackarch_manager.get_available_tools()
                self.tools_listbox.delete(0, tk.END)
                for tool in tools[:50]:  # Limit to 50 for performance
                    self.tools_listbox.insert(tk.END, tool.get('name', 'Unknown'))
            except Exception as e:
                self.logger.error(f"Failed to update tools list: {e}")

    # Database Methods
    def connect_database(self):
        """Connect to database"""
        try:
            if self.db_connection:
                self.db_connection.close()

            self.db_connection = psycopg2.connect(
                host=self.db_host_var.get(),
                port=self.db_port_var.get(),
                database=self.db_name_var.get(),
                user=self.db_user_var.get(),
                password=self.db_pass_var.get()
            )
            self.database_status.config(text="Database: Connected", fg='green')
            messagebox.showinfo("Success", "Database connected successfully")
        except Exception as e:
            self.database_status.config(text="Database: Connection Failed", fg='red')
            messagebox.showerror("Error", f"Database connection failed: {str(e)}")

    def execute_query(self):
        """Execute database query"""
        if not self.db_connection:
            messagebox.showerror("Error", "Database not connected")
            return

        query = self.db_query_text.get(1.0, tk.END).strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a query")
            return

        try:
            cursor = self.db_connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                self.db_results_text.delete(1.0, tk.END)
                self.db_results_text.insert(tk.END, json.dumps(results, indent=2))
            else:
                self.db_connection.commit()
                self.db_results_text.delete(1.0, tk.END)
                self.db_results_text.insert(tk.END, f"Query executed successfully. Rows affected: {cursor.rowcount}")

            cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Query execution failed: {str(e)}")

    # Placeholder methods for buttons that need implementation
    def run_benchmarks(self):
        messagebox.showinfo("Info", "Benchmark functionality coming soon")

    def add_knowledge(self):
        messagebox.showinfo("Info", "Add knowledge functionality coming soon")

    def import_dataset(self):
        messagebox.showinfo("Info", "Import dataset functionality coming soon")

    def export_knowledge(self):
        messagebox.showinfo("Info", "Export knowledge functionality coming soon")

    def extract_wallet_keys(self):
        messagebox.showinfo("Info", "Key extraction functionality coming soon")

    def init_blackarch(self):
        messagebox.showinfo("Info", "BlackArch initialization coming soon")

    def update_blackarch_tools(self):
        messagebox.showinfo("Info", "BlackArch update functionality coming soon")

    def launch_blackarch_web(self):
        messagebox.showinfo("Info", "BlackArch web interface coming soon")

    def execute_selected_tool(self):
        messagebox.showinfo("Info", "Tool execution functionality coming soon")

    def view_tool_info(self):
        messagebox.showinfo("Info", "Tool info functionality coming soon")

    def show_tables(self):
        messagebox.showinfo("Info", "Show tables functionality coming soon")

    def backup_database(self):
        messagebox.showinfo("Info", "Database backup functionality coming soon")

    def save_settings(self):
        messagebox.showinfo("Info", "Settings save functionality coming soon")

    def check_system_health(self):
        messagebox.showinfo("Info", "System health check coming soon")

    def view_logs(self):
        messagebox.showinfo("Info", "Log viewer coming soon")

    def restart_services(self):
        messagebox.showinfo("Info", "Service restart functionality coming soon")

    def start_ai_core(self):
        messagebox.showinfo("Info", "AI Core start functionality coming soon")

    def start_knowledge_api(self):
        messagebox.showinfo("Info", "Knowledge API start functionality coming soon")

    def open_web_interface(self):
        """Open web interface in browser"""
        try:
            webbrowser.open("http://localhost:3000")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open web interface: {str(e)}")


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = R3AL3RDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()