def ensure_valid_markdown(text: str) -> str:
    """
    Closes all open markdown tags in accumulated text to ensure that a 
    parsing error is not raised by Telegram for basic markdown V1 tags.
    Handles *, _, `, ```, ~.
    Note: Telegram's Markdown V1 primarily supports *, _, `, ```. ~ might not render.
    This function is a best-effort sanitizer.
    """
    # Define tags: single char (paired), multi-char (paired)
    # Telegram Markdown V1 primarily uses *, _, ` for inline.
    # ``` for pre-formatted blocks.
    # ~ for strikethrough is common but not always standard for TG MD V1.
    # We will treat * and _ similarly for balancing.

    # Using a list for the stack to handle different tag types.
    # Each element could be the tag itself (e.g., '*', '```').
    stack = []
    result = []
    i = 0
    n = len(text)

    while i < n:
        char = text[i]
        processed_char = False

        # Check for multi-character tags first (e.g., ```)
        if text[i:i+3] == '```':
            tag = '```'
            if stack and stack[-1] == tag: # Closing an open tag
                stack.pop()
            else: # Opening a new tag
                stack.append(tag)
            result.append(tag)
            i += 3
            processed_char = True

        # Check for single-character tags (e.g., *, _, `, ~)
        # For simplicity, we assume * and _ are not used for different emphasis levels simultaneously
        # in a way that would confuse this simple balancer.
        elif char in ['*', '_', '`', '~']:
            tag = char
            if stack and stack[-1] == tag: # Closing an open tag
                stack.pop()
            else: # Opening a new tag
                stack.append(tag)
            result.append(tag)
            i += 1
            processed_char = True

        if not processed_char:
            result.append(char)
            i += 1

    # Close any remaining open tags
    while stack:
        open_tag = stack.pop()
        result.append(open_tag) # Append the closing tag

    return "".join(result)
