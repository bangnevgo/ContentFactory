"""Approval workflow — manage content lifecycle."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from core.db import FactoryDB
from core.schemas import ContentStatus


class Approver:
    """Manage content approval workflow: draft → review → approved → scheduled."""

    def __init__(self, db=None):
        self.db = db or FactoryDB()

    def approve(self, content_id):
        """Approve content for scheduling."""
        row = self.db.query("SELECT * FROM content WHERE content_id = ?", [content_id])
        if not row:
            return None
        self.db.update_content(content_id, {"status": ContentStatus.APPROVED.value})
        return {"id": content_id, "topic": row[0]["topic"], "status": "approved"}

    def reject(self, content_id):
        """Reject back to draft."""
        row = self.db.query("SELECT * FROM content WHERE content_id = ?", [content_id])
        if not row:
            return None
        self.db.update_content(content_id, {"status": ContentStatus.DRAFT.value})
        return {"id": content_id, "topic": row[0]["topic"], "status": "draft"}

    def bulk_approve(self, content_ids):
        """Approve multiple content items."""
        approved = []
        for cid in content_ids:
            result = self.approve(cid)
            if result:
                approved.append(result)
        return approved

    def get_pending(self, status="draft"):
        """Get all pending content."""
        return self.db.query(
            "SELECT content_id, type, topic, status, created_at, LEFT(caption, 80) as preview "
            "FROM content WHERE status = ? ORDER BY created_at DESC",
            [status]
        )

    def get_for_scheduling(self):
        """Get all approved content ready to schedule."""
        return self.db.query(
            "SELECT content_id, type, topic, created_at, caption "
            "FROM content WHERE status = 'approved' ORDER BY updated_at DESC"
        )
