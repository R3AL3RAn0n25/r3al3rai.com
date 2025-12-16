-- Active: 1764340338903@@127.0.0.1@5432@r3aler_ai@user_unit
#!/usr/bin/env python3
"""
R3ÆLƎR AI - Social Media Deployment Script
Deploys demo to GitHub Pages or similar for public sharing
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def deploy_to_github_pages():
    """Deploy demo to GitHub Pages for public access"""

    project_root = Path(__file__).parent
    demo_dir = project_root / "demo-deploy"
    build_dir = project_root / "docs"  # GitHub Pages serves from docs/

    print("🚀 R3ÆLƎR AI - Social Media Deployment")
    print("=" * 50)

    # Check if demo files exist
    if not demo_dir.exists():
        print("❌ Demo directory not found!")
        return False

    # Create docs directory for GitHub Pages
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()

    # Copy demo files
    print("📋 Copying demo files...")
    for file in demo_dir.glob("*"):
        if file.is_file():
            shutil.copy2(file, build_dir / file.name)

    # Create index.html redirect to demo
    index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="0; url=r3aler_ai_live_demo.html">
    <title>R3ÆLƎR AI Live Demo - Redirecting...</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }
        .container {
            max-width: 600px;
            padding: 40px;
        }
        h1 {
            font-size: 3em;
            background: linear-gradient(45deg, #00d4ff, #0099cc, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
        }
        p {
            font-size: 1.2em;
            margin-bottom: 30px;
        }
        .loading {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 3px solid #333;
            border-radius: 50%;
            border-top-color: #00d4ff;
            animation: spin 1s ease-in-out infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>R3ÆLƎR AI</h1>
        <p>Initializing Live Interactive Demo...</p>
        <div class="loading"></div>
        <p style="font-size: 0.9em; margin-top: 20px; opacity: 0.8;">
            If you are not redirected automatically,<br>
            <a href="r3aler_ai_live_demo.html" style="color: #00d4ff;">click here to access the demo</a>
        </p>
    </div>
</body>
</html>"""

    with open(build_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

    print("✅ Demo files prepared for GitHub Pages")
    print("\n📝 Next Steps:")
    print("1. Commit and push the 'docs' folder to your GitHub repository")
    print("2. Enable GitHub Pages in repository settings:")
    print("   - Go to Settings → Pages")
    print("   - Source: 'Deploy from a branch'")
    print("   - Branch: main, Folder: /docs")
    print("3. Your demo will be available at: https://[username].github.io/[repo-name]/")
    print("\n🔗 Share this URL on social media!")
    print("\n💡 Pro Tip: Use a custom domain for a more professional look")

    return True

def create_social_media_package():
    """Create a ZIP file with promotional materials"""

    project_root = Path(__file__).parent
    package_dir = project_root / "social_media_package"

    print("\n📦 Creating Social Media Package...")

    # Create package directory
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()

    # Copy promotional files
    files_to_copy = [
        "SOCIAL_MEDIA_PROMOTION_GUIDE.md",
        "READY_TO_POST_CONTENT.md",
        "DEMO_README.md",
        "README.md"
    ]

    for file in files_to_copy:
        src = project_root / file
        if src.exists():
            shutil.copy2(src, package_dir / file)

    # Create a simple HTML landing page for sharing
    landing_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>R3ÆLƎR AI - Self-Evolving Artificial Intelligence</title>
    <meta name="description" content="Experience R3ÆLƎR AI - a revolutionary self-evolving artificial intelligence system that adapts and learns in real-time.">
    <meta property="og:title" content="R3ÆLƎR AI - Self-Evolving Artificial Intelligence">
    <meta property="og:description" content="The AI that evolves itself. Experience real-time adaptation, multi-domain intelligence, and integrated cybersecurity tools.">
    <meta property="og:image" content="https://your-demo-url.com/preview-image.png">
    <meta property="og:url" content="https://your-demo-url.com">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="R3ÆLƎR AI - Self-Evolving AI">
    <meta name="twitter:description" content="Experience the future of AI that adapts and evolves in real-time.">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            margin: 0;
            padding: 20px;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            font-size: 3em;
            background: linear-gradient(45deg, #00d4ff, #0099cc, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
        }
        .tagline {
            font-size: 1.5em;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        .demo-btn {
            display: inline-block;
            background: linear-gradient(45deg, #00d4ff, #0099cc);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 1.2em;
            font-weight: bold;
            margin: 20px 0;
            transition: transform 0.2s;
        }
        .demo-btn:hover {
            transform: scale(1.05);
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
            text-align: left;
        }
        .feature {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(0, 212, 255, 0.2);
        }
        .social-links {
            margin: 40px 0;
        }
        .social-links a {
            color: #00d4ff;
            text-decoration: none;
            margin: 0 15px;
            font-size: 1.1em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>R3ÆLƎR AI</h1>
        <p class="tagline">Self-Evolving Artificial Intelligence That Adapts In Real-Time</p>

        <a href="r3aler_ai_live_demo.html" class="demo-btn">🚀 Experience the Live Demo</a>

        <div class="features">
            <div class="feature">
                <h3>🧠 Self-Learning</h3>
                <p>Continuously evolves and optimizes its algorithms based on real-time interactions and performance metrics.</p>
            </div>
            <div class="feature">
                <h3>🔬 Multi-Domain Intelligence</h3>
                <p>Integrated knowledge across physics, space engineering, cybersecurity, and cryptocurrency domains.</p>
            </div>
            <div class="feature">
                <h3>🛡️ Advanced Tools</h3>
                <p>Built-in BlackArch penetration testing suite and BitXtractor cryptocurrency analysis tools.</p>
            </div>
            <div class="feature">
                <h3>⚡ Real-Time Adaptation</h3>
                <p>Adapts responses and behavior patterns during active conversations for personalized interactions.</p>
            </div>
        </div>

        <div class="social-links">
            <a href="https://twitter.com/R3AL3RAI" target="_blank">🐦 Twitter</a>
            <a href="https://github.com/R3AL3RAn0n25/r3al3rai.com" target="_blank">💻 GitHub</a>
            <a href="https://www.linkedin.com/in/r3al3rai" target="_blank">💼 LinkedIn</a>
        </div>

        <p style="opacity: 0.7; font-size: 0.9em;">
            Experience the future of AI - where intelligence evolves, adapts, and grows with every interaction.
        </p>
    </div>
</body>
</html>"""

    with open(package_dir / "landing_page.html", "w", encoding="utf-8") as f:
        f.write(landing_html)

    # Create ZIP file
    zip_name = "R3AL3R_AI_Social_Media_Package"
    shutil.make_archive(zip_name, 'zip', package_dir)

    print(f"✅ Social media package created: {zip_name}.zip")
    print("📁 Contents:")
    for file in package_dir.glob("*"):
        print(f"   - {file.name}")

    return True

def main():
    print("R3ÆLƎR AI - Social Media Deployment Tool")
    print("=" * 50)

    while True:
        print("\nChoose an option:")
        print("1. Deploy demo to GitHub Pages")
        print("2. Create social media content package")
        print("3. Do both")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            deploy_to_github_pages()
        elif choice == "2":
            create_social_media_package()
        elif choice == "3":
            deploy_to_github_pages()
            create_social_media_package()
        elif choice == "4":
            print("Goodbye! 🚀")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()