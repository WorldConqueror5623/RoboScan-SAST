import re

def remove_comments(content):
    """
    Removes Solidity comments but preserves line numbers
    by replacing comments with empty lines/spaces.
    """
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    
    def _replacer(match):
        if match.group(2) is not None:
            # Calculate how many newlines were in the comment we just found
            num_newlines = match.group(2).count('\n')
            # Return that many newlines so line count stays in sync
            return "\n" * num_newlines 
        else:
            return match.group(1) # Keep strings
            
    return regex.sub(_replacer, content)

class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

def log(message, color=Colors.RESET):
    print(f"{color}{message}{Colors.RESET}")