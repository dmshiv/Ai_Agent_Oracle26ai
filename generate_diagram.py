#!/usr/bin/env python3
"""Generate AI Incident Copilot architecture diagram as PNG."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(16, 12), dpi=150)
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Colors
color_ui = '#ff6b6b'
color_backend = '#4ecdc4'
color_ai = '#ffe66d'
color_embedding = '#a8e6cf'
color_db = '#c7ceea'
color_data = '#ffd3b6'
color_tools = '#b5ead7'

def draw_box(ax, x, y, width, height, text, color, fontsize=10, fontweight='normal'):
    """Draw a rounded box with text."""
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                          boxstyle="round,pad=0.1", 
                          edgecolor='black', facecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, 
            fontweight=fontweight, wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, label='', style='->'):
    """Draw an arrow between two points."""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle=style, mutation_scale=20, 
                           linewidth=2, color='#333', zorder=-1)
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x + 0.2, mid_y + 0.2, label, fontsize=8, 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Title
ax.text(5, 11.5, '🚀 AI Incident Copilot — System Architecture', 
        ha='center', fontsize=18, fontweight='bold')

# ===== LAYER 1: USER INTERFACE (top) =====
ax.text(0.3, 10.7, '🖥️ User Interface', fontsize=11, fontweight='bold')
draw_box(ax, 1.5, 10.2, 2.5, 0.8, '🎨 Streamlit UI\nlocalhost:8501', color_ui, fontsize=9)

# ===== LAYER 2: BACKEND SERVICES =====
ax.text(0.3, 9.2, '⚙️ Backend Services', fontsize=11, fontweight='bold')
draw_box(ax, 1.5, 8.7, 2.2, 0.8, '🔌 FastAPI\nlocalhost:8000', color_backend, fontsize=9)
draw_box(ax, 4, 8.7, 2.2, 0.8, '🤖 LangChain\nAgent', color_backend, fontsize=9)

# ===== LAYER 3: AI & EMBEDDING =====
ax.text(0.3, 7.8, '🧠 AI & Embedding', fontsize=11, fontweight='bold')
draw_box(ax, 1.5, 7.3, 2.2, 0.8, '🦙 Ollama\nllama3.1:8b', color_ai, fontsize=9)
draw_box(ax, 4, 7.3, 2.2, 0.8, '📊 MiniLM-L6-v2\n384-dim vectors', color_embedding, fontsize=9)

# ===== LAYER 4: LANGCHAIN TOOLS =====
ax.text(0.3, 6.4, '🎯 LangChain Tools', fontsize=11, fontweight='bold')
draw_box(ax, 0.8, 5.5, 1.8, 0.6, '🔍 find_similar\nincidents', color_tools, fontsize=8)
draw_box(ax, 2.8, 5.5, 1.8, 0.6, '🔍 find_similar\nfiltered', color_tools, fontsize=8)
draw_box(ax, 4.8, 5.5, 1.8, 0.6, '📖 get_runbooks\nfor_incident', color_tools, fontsize=8)
draw_box(ax, 6.8, 5.5, 1.8, 0.6, '👤 get_service\nowner', color_tools, fontsize=8)

# ===== LAYER 5: VECTOR DATABASE =====
ax.text(0.3, 4.6, '🗄️ Vector Database', fontsize=11, fontweight='bold')
draw_box(ax, 2.5, 4, 3.5, 0.8, '🏛️ Oracle 26ai\nlocalhost:1521/FREEPDB1', color_db, fontsize=9)

# ===== LAYER 6: DATABASE COMPONENTS =====
ax.text(0.3, 3.2, '📊 Database Components', fontsize=11, fontweight='bold')
draw_box(ax, 0.8, 2.5, 1.6, 0.6, '📋 services\nincidents', color_db, fontsize=8)
draw_box(ax, 2.8, 2.5, 1.6, 0.6, '📋 runbooks\nincident_runbooks', color_db, fontsize=8)
draw_box(ax, 4.8, 2.5, 1.6, 0.6, '⚡ HNSW Indexes\nCOSINE distance', color_db, fontsize=8)

# ===== LAYER 7: DATA PIPELINE =====
ax.text(0.3, 1.6, '🔧 Data Pipeline', fontsize=11, fontweight='bold')
draw_box(ax, 0.8, 0.9, 1.8, 0.6, '🛠️ setup_db.sh\nUser & schema init', color_data, fontsize=8)
draw_box(ax, 3, 0.9, 1.8, 0.6, '🌱 seed.py\n50 incidents', color_data, fontsize=8)
draw_box(ax, 5.2, 0.9, 1.8, 0.6, '📊 15 runbooks\n20 services', color_data, fontsize=8)

# ===== RIGHT SIDE: DATA FLOW =====
# This will show the query flow
ax.text(7.5, 10.7, '📊 Query Flow', fontsize=11, fontweight='bold')

# Right side boxes
draw_box(ax, 8.5, 9.8, 2.2, 0.7, '1️⃣ User Query', '#e8e8e8', fontsize=9)
draw_box(ax, 8.5, 8.8, 2.2, 0.7, '2️⃣ Embed Query\n(MiniLM)', '#e8e8e8', fontsize=9)
draw_box(ax, 8.5, 7.8, 2.2, 0.7, '3️⃣ Vector Search\n(HNSW)', '#e8e8e8', fontsize=9)
draw_box(ax, 8.5, 6.8, 2.2, 0.7, '4️⃣ Filter & Join\n(SQL)', '#e8e8e8', fontsize=9)
draw_box(ax, 8.5, 5.8, 2.2, 0.7, '5️⃣ Call LLM\n(Ollama)', '#e8e8e8', fontsize=9)
draw_box(ax, 8.5, 4.8, 2.2, 0.7, '6️⃣ Synthesize\nResponse', '#e8e8e8', fontsize=9)
draw_box(ax, 8.5, 3.8, 2.2, 0.7, '7️⃣ Return Answer\n+ Reasoning', '#e8e8e8', fontsize=9)

# Query flow arrows
for i, (y_from, y_to) in enumerate([(9.8, 8.8), (8.8, 7.8), (7.8, 6.8), (6.8, 5.8), (5.8, 4.8), (4.8, 3.8)]):
    draw_arrow(ax, 8.5, y_from - 0.4, 8.5, y_to + 0.4)

# ===== CONNECTIONS (Main Flow) =====
# UI to API
draw_arrow(ax, 2.5, 9.9, 2, 9.1, 'Query')

# API to Agent
draw_arrow(ax, 2.7, 8.3, 3.3, 8.3)

# Agent to Ollama
draw_arrow(ax, 3.5, 8.3, 2.2, 7.7)

# Agent to Embedding
draw_arrow(ax, 4.2, 8.3, 4.2, 7.7)

# Agent to Tools
draw_arrow(ax, 4, 8.3, 1.5, 5.8)
draw_arrow(ax, 4, 8.3, 3.5, 5.8)
draw_arrow(ax, 4, 8.3, 5.5, 5.8)
draw_arrow(ax, 4, 8.3, 7.5, 5.8)

# Tools to Oracle
draw_arrow(ax, 1.5, 5.2, 1.5, 4.4)
draw_arrow(ax, 3.5, 5.2, 2.5, 4.4)
draw_arrow(ax, 5.5, 5.2, 2.8, 4.4)
draw_arrow(ax, 7.5, 5.2, 3.3, 4.4)

# Oracle to Components
draw_arrow(ax, 1.5, 3.9, 1.5, 2.8)
draw_arrow(ax, 2.5, 3.9, 2.5, 2.8)
draw_arrow(ax, 3.5, 3.9, 3.5, 2.8)

# Data pipeline to Oracle
draw_arrow(ax, 0.8, 1.2, 1.5, 3.6)
draw_arrow(ax, 3, 1.2, 2.5, 3.6)
draw_arrow(ax, 5.2, 1.2, 3.5, 3.6)

# Add legend at bottom
ax.text(0.5, -0.3, '💡 Key: Semantic search (vectors) + Relational queries (SQL) + Local LLM (Ollama) = Incident diagnosis', 
        fontsize=9, style='italic', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('/home/dom/Rahul_wagh_AI_Learn/Project_1/ai-incident-copilot/ARCHITECTURE_DIAGRAM.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
print("✅ Architecture diagram saved as ARCHITECTURE_DIAGRAM.png")
plt.close()

# Create a second simpler flow diagram
fig, ax = plt.subplots(1, 1, figsize=(14, 10), dpi=150)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(5, 9.5, '🔄 AI Incident Copilot — Data Flow', 
        ha='center', fontsize=16, fontweight='bold')

# Main flow
draw_box(ax, 5, 8.5, 3, 0.8, '👤 User asks\n"High latency in payments?"', '#ffcccc', fontsize=10, fontweight='bold')

draw_arrow(ax, 5, 8.1, 5, 7.5)
draw_box(ax, 5, 7, 3, 0.8, '📝 Streamlit UI captures query', '#ff9999', fontsize=10)

draw_arrow(ax, 5, 6.6, 5, 6)
draw_box(ax, 5, 5.5, 3, 0.8, '🔌 FastAPI receives request', '#4ecdc4', fontsize=10)

draw_arrow(ax, 5, 5.1, 5, 4.5)
draw_box(ax, 5, 4, 3, 0.8, '🤖 LangChain Agent decides:', '#95e1d3', fontsize=9)

# Branching tools
draw_arrow(ax, 4, 3.6, 1.5, 2.8)
draw_box(ax, 1, 2.2, 2, 0.8, '📊 Embed query\n(MiniLM)', '#a8e6cf', fontsize=8)

draw_arrow(ax, 5, 3.6, 5, 2.8)
draw_box(ax, 5, 2.2, 2, 0.8, '🔍 Vector search\n(HNSW index)', '#b5ead7', fontsize=8)

draw_arrow(ax, 6, 3.6, 8.5, 2.8)
draw_box(ax, 9, 2.2, 2, 0.8, '🔗 Join with\nrunbooks', '#c1cfe0', fontsize=8)

# All converge to Oracle
draw_arrow(ax, 1, 1.8, 4, 1.2)
draw_arrow(ax, 5, 1.8, 5, 1.2)
draw_arrow(ax, 9, 1.8, 6, 1.2)

draw_box(ax, 5, 0.5, 3.5, 0.8, '🏛️ Oracle 26ai returns results', '#c7ceea', fontsize=10, fontweight='bold')

# Response phase
draw_arrow(ax, 5, 0.1, 5, -0.5)
draw_box(ax, 5, -1.2, 3.5, 0.8, '🦙 Ollama (Llama 3.1) generates response', '#ffe66d', fontsize=10)

draw_arrow(ax, 5, -1.6, 5, -2.2)
draw_box(ax, 5, -2.9, 3.5, 0.8, '📖 Streamlit shows answer + sources', '#ff9999', fontsize=10, fontweight='bold')

# Add key stats
stats_text = '''📊 Demo Data:
• 50 Incidents
• 15 Runbooks
• 20 Services
• 107 Links'''

ax.text(0.5, 3, stats_text, fontsize=8, 
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

tech_text = '''⚙️ Tech Stack:
• Oracle 26ai (Vector DB)
• Llama 3.1 (Local LLM)
• MiniLM (Embeddings)
• FastAPI + Streamlit'''

ax.text(9.5, 3, tech_text, fontsize=8, ha='right',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))

plt.tight_layout()
plt.savefig('/home/dom/Rahul_wagh_AI_Learn/Project_1/ai-incident-copilot/DATA_FLOW_DIAGRAM.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
print("✅ Data flow diagram saved as DATA_FLOW_DIAGRAM.png")

print("\n✨ Both diagrams created successfully!")
print("📁 Files:")
print("  - ARCHITECTURE_DIAGRAM.png")
print("  - DATA_FLOW_DIAGRAM.png")
