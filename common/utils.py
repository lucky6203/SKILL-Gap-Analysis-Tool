# small helper utils
import uuid

def opaque_id(prefix="id") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"
