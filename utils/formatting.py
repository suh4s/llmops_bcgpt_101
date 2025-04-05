"""
Formatting Module - Handles text formatting and display utilities.
"""

def format_template_text(text: str) -> str:
    """Format template text for table display with proper wrapping."""
    text = text.replace("\n", " ")
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= 60:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return "<br>".join(lines) 