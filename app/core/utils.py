def now_iso():
    from datetime import datetime
    return datetime.now().isoformat() + "Z"
