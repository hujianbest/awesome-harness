"""
Tests for KnowledgeIntegration module.

Tests the integration between KnowledgeStore and ExperienceIndex,
including cross-module retrieval, manual knowledge extraction, and
data consistency maintenance.
"""

import pytest
from datetime import datetime
from pathlib import Path

from garage_os.knowledge.knowledge_store import KnowledgeStore
from garage_os.knowledge.experience_index import ExperienceIndex
from garage_os.knowledge.integration import KnowledgeIntegration
from garage_os.storage.file_storage import FileStorage
from garage_os.types import (
    KnowledgeType,
    KnowledgeEntry,
    ExperienceRecord,
)


@pytest.fixture
def temp_storage(tmp_path):
    """Create a temporary FileStorage instance."""
    return FileStorage(tmp_path)


@pytest.fixture
def knowledge_store(temp_storage):
    """Create a KnowledgeStore instance with temporary storage."""
    return KnowledgeStore(temp_storage)


@pytest.fixture
def experience_index(temp_storage):
    """Create an ExperienceIndex instance with temporary storage."""
    return ExperienceIndex(temp_storage)


@pytest.fixture
def integration(knowledge_store, experience_index):
    """Create a KnowledgeIntegration instance."""
    return KnowledgeIntegration(knowledge_store, experience_index)


@pytest.fixture
def sample_decision():
    """Create a sample decision knowledge entry."""
    return KnowledgeEntry(
        id="decision-001",
        type=KnowledgeType.DECISION,
        topic="Use SQLAlchemy for ORM",
        date=datetime.now(),
        tags=["database", "orm", "sqlalchemy", "python"],
        content="# Decision\n\nWe decided to use SQLAlchemy for the ORM layer.",
        status="active",
        version=1,
    )


@pytest.fixture
def sample_pattern():
    """Create a sample pattern knowledge entry."""
    return KnowledgeEntry(
        id="pattern-001",
        type=KnowledgeType.PATTERN,
        topic="Repository Pattern for Data Access",
        date=datetime.now(),
        tags=["architecture", "design-pattern", "data-access"],
        content="# Repository Pattern\n\nSeparate data access logic from business logic.",
        status="active",
        version=1,
    )


@pytest.fixture
def sample_experience_record():
    """Create a sample experience record."""
    now = datetime.now()
    return ExperienceRecord(
        record_id="exp-001",
        task_type="database_layer_design",
        skill_ids=["python", "database-design"],
        tech_stack=["Python", "SQLAlchemy", "PostgreSQL"],
        domain="backend",
        problem_domain="data-access-layer",
        outcome="success",
        duration_seconds=3600,
        complexity="medium",
        session_id="session-123",
        artifacts=["artifact-db-layer"],
        key_patterns=["repository-pattern", "orm-integration"],
        lessons_learned=["Repository pattern helps testability"],
        pitfalls=["Direct ORM coupling in business logic"],
        recommendations=["Use repository abstraction"],
        created_at=now,
        updated_at=now,
    )


def test_find_related_knowledge_by_experience(
    integration,
    knowledge_store,
    experience_index,
    sample_decision,
    sample_pattern,
    sample_experience_record,
):
    """Test finding related knowledge based on experience record.

    Scenario: Given an experience record with specific tags and key patterns,
    when searching for related knowledge, then return matching decision/pattern entries.
    """
    # Store knowledge entries
    knowledge_store.store(sample_decision)
    knowledge_store.store(sample_pattern)

    # Store experience record
    experience_index.store(sample_experience_record)

    # Find related knowledge based on experience
    related = integration.find_related_knowledge("exp-001")

    # Verify results contain entries matching by tags and key patterns
    assert len(related) >= 1

    # Extract knowledge IDs for verification
    related_ids = {k.id for k in related}

    # Should find pattern matching "repository-pattern" key pattern
    assert "pattern-001" in related_ids

    # Should potentially find decision based on overlapping domain/tags
    # The decision has "python" tag, experience has "python" skill
    if "decision-001" in related_ids:
        decision = next(k for k in related if k.id == "decision-001")
        assert decision.type == KnowledgeType.DECISION


def test_find_related_knowledge_by_tags_and_keywords(
    integration,
    knowledge_store,
    experience_index,
):
    """Test finding related knowledge using multiple criteria.

    Scenario: Knowledge entries should match experience records by
    tags in knowledge entries and key_patterns/skills in experience records.
    """
    # Create knowledge with specific tags
    knowledge1 = KnowledgeEntry(
        id="k1",
        type=KnowledgeType.PATTERN,
        topic="Dependency Injection",
        date=datetime.now(),
        tags=["architecture", "dependency-injection", "di-container"],
        content="DI pattern for loose coupling",
    )

    knowledge2 = KnowledgeEntry(
        id="k2",
        type=KnowledgeType.DECISION,
        topic="Microservices Architecture",
        date=datetime.now(),
        tags=["architecture", "microservices", "distributed-systems"],
        content="Decision to use microservices",
    )

    knowledge_store.store(knowledge1)
    knowledge_store.store(knowledge2)

    # Create experience with matching key patterns
    experience = ExperienceRecord(
        record_id="exp-di",
        task_type="architecture_design",
        skill_ids=["architecture", "di-container"],
        tech_stack=["Python"],
        domain="backend",
        problem_domain="dependency-management",
        outcome="success",
        duration_seconds=2400,
        complexity="high",
        session_id="session-di",
        key_patterns=["dependency-injection"],
    )

    experience_index.store(experience)

    # Find related knowledge
    related = integration.find_related_knowledge("exp-di")

    # Should find knowledge1 matching by "dependency-injection"
    related_ids = {k.id for k in related}
    assert "k1" in related_ids


def test_find_related_knowledge_returns_empty_when_no_match(
    integration,
    experience_index,
):
    """Test that find_related_knowledge returns empty list when no matches found."""
    # Create experience without matching knowledge
    experience = ExperienceRecord(
        record_id="exp-no-match",
        task_type="ui_design",
        skill_ids=["css", "html"],
        tech_stack=["React"],
        domain="frontend",
        problem_domain="styling",
        outcome="success",
        duration_seconds=1800,
        complexity="low",
        session_id="session-ui",
        key_patterns=["css-grid"],
    )

    experience_index.store(experience)

    # Find related knowledge (should be empty)
    related = integration.find_related_knowledge("exp-no-match")
    assert related == []


def test_extract_from_session_flow(
    integration,
    knowledge_store,
    experience_index,
):
    """Test manual knowledge extraction from a completed session.

    Scenario: Create session → complete task → manually record experience →
    knowledge入库 to both experience index and knowledge store.
    """
    # Prepare session and experience data
    session_id = "session-complete-001"
    experience_data = {
        "task_type": "authentication_implementation",
        "skill_ids": ["security", "jwt"],
        "tech_stack": ["Python", "FastAPI", "JWT"],
        "domain": "security",
        "problem_domain": "authentication",
        "outcome": "success",
        "duration_seconds": 4800,
        "complexity": "high",
        "artifacts": ["auth-middleware"],
        "key_patterns": ["jwt-authentication", "middleware-pattern"],
        "lessons_learned": [
            "JWT validation should happen in middleware",
            "Token rotation improves security",
        ],
        "pitfalls": [
            "Initial implementation lacked token refresh",
        ],
        "recommendations": [
            "Implement refresh token rotation",
            "Use asymmetric keys for production",
        ],
    }

    # Extract knowledge from session
    result = integration.extract_from_session(session_id, experience_data)

    # Verify experience record was created
    assert result["experience_record_id"] is not None
    experience = experience_index.retrieve(result["experience_record_id"])
    assert experience is not None
    assert experience.session_id == session_id
    assert experience.task_type == "authentication_implementation"
    assert len(experience.lessons_learned) == 2

    # Verify knowledge entry was created
    assert result["knowledge_entry_id"] is not None
    knowledge = knowledge_store.retrieve(KnowledgeType.SOLUTION, result["knowledge_entry_id"])
    assert knowledge is not None
    assert knowledge.source_session == session_id
    assert "authentication" in knowledge.topic.lower() or "jwt" in knowledge.topic.lower()


def test_extract_from_session_creates_decision_type(
    integration,
    knowledge_store,
    experience_index,
):
    """Test that extract_from_session can create decision type knowledge entries."""
    session_id = "session-decision-001"
    experience_data = {
        "task_type": "technology_selection",
        "skill_ids": ["architecture"],
        "tech_stack": ["Python"],
        "domain": "architecture",
        "problem_domain": "orm-selection",
        "outcome": "success",
        "duration_seconds": 2400,
        "complexity": "medium",
        "key_patterns": ["technology-selection"],
        "knowledge_type": "decision",  # Specify decision type
        "decision_topic": "Use SQLAlchemy for ORM",
        "decision_rationale": "Mature ecosystem, async support, good typing",
    }

    result = integration.extract_from_session(session_id, experience_data)

    # Verify knowledge entry is DECISION type
    knowledge = knowledge_store.retrieve(KnowledgeType.DECISION, result["knowledge_entry_id"])
    assert knowledge is not None
    assert knowledge.type == KnowledgeType.DECISION
    assert "SQLAlchemy" in knowledge.topic


def test_extract_from_session_creates_pattern_type(
    integration,
    knowledge_store,
    experience_index,
):
    """Test that extract_from_session can create pattern type knowledge entries."""
    session_id = "session-pattern-001"
    experience_data = {
        "task_type": "refactoring",
        "skill_ids": ["refactoring", "design-patterns"],
        "tech_stack": ["Python"],
        "domain": "backend",
        "problem_domain": "error-handling",
        "outcome": "success",
        "duration_seconds": 3600,
        "complexity": "medium",
        "key_patterns": ["result-pattern"],
        "knowledge_type": "pattern",  # Specify pattern type
        "pattern_topic": "Result Pattern for Error Handling",
        "pattern_description": "Use Result type instead of exceptions for error propagation",
    }

    result = integration.extract_from_session(session_id, experience_data)

    # Verify knowledge entry is PATTERN type
    knowledge = knowledge_store.retrieve(KnowledgeType.PATTERN, result["knowledge_entry_id"])
    assert knowledge is not None
    assert knowledge.type == KnowledgeType.PATTERN
    assert "Result" in knowledge.topic or "Error" in knowledge.topic


def test_remove_knowledge_cascade_handles_experience_references(
    integration,
    knowledge_store,
    experience_index,
):
    """Test cascade deletion maintains consistency across modules.

    Scenario: When a knowledge entry is deleted, experience records that
    reference it should handle the reference gracefully.
    """
    # Create a knowledge entry
    knowledge = KnowledgeEntry(
        id="knowledge-to-delete",
        type=KnowledgeType.DECISION,
        topic="Delete Me Decision",
        date=datetime.now(),
        tags=["test"],
        content="This will be deleted",
    )
    knowledge_store.store(knowledge)

    # Create experience record referencing the knowledge (via related_tasks)
    experience = ExperienceRecord(
        record_id="exp-with-ref",
        task_type="test_task",
        skill_ids=["test"],
        tech_stack=["Python"],
        domain="test",
        problem_domain="test",
        outcome="success",
        duration_seconds=100,
        complexity="low",
        session_id="session-test",
        artifacts=["knowledge-to-delete"],  # Reference to knowledge
    )
    experience_index.store(experience)

    # Remove knowledge with cascade
    removed = integration.remove_knowledge_cascade(
        KnowledgeType.DECISION,
        "knowledge-to-delete",
    )

    # Verify knowledge was removed
    assert removed is True
    retrieved = knowledge_store.retrieve(KnowledgeType.DECISION, "knowledge-to-delete")
    assert retrieved is None

    # Verify experience record is still accessible
    experience_after = experience_index.retrieve("exp-with-ref")
    assert experience_after is not None

    # The reference handling depends on implementation:
    # - Option 1: Remove references from artifacts list
    # - Option 2: Mark as invalid but keep the record
    # We verify the record is still accessible, implementation details may vary


def test_remove_knowledge_cascade_nonexistent(
    integration,
):
    """Test cascade deletion with non-existent knowledge entry."""
    result = integration.remove_knowledge_cascade(
        KnowledgeType.DECISION,
        "non-existent-id",
    )
    assert result is False


def test_find_related_knowledge_nonexistent_experience(
    integration,
):
    """Test find_related_knowledge with non-existent experience record."""
    result = integration.find_related_knowledge("non-existent-exp")
    assert result == []


def test_integration_end_to_end_workflow(
    integration,
    knowledge_store,
    experience_index,
):
    """Test complete end-to-end integration workflow.

    Scenario: Complete workflow from session completion through
    knowledge extraction to related knowledge discovery.
    """
    # Step 1: Complete a session and extract knowledge
    session_id = "session-e2e-001"
    experience_data = {
        "task_type": "api_design",
        "skill_ids": ["api-design", "rest"],
        "tech_stack": ["FastAPI", "Pydantic"],
        "domain": "backend",
        "problem_domain": "api-validation",
        "outcome": "success",
        "duration_seconds": 3200,
        "complexity": "medium",
        "artifacts": ["api-validator"],
        "key_patterns": ["validation-pyramid", "pydantic-models"],
        "lessons_learned": [
            "Pydantic models provide excellent validation",
            "Layer validation: DB model → API model → Response model",
        ],
        "pitfalls": [
            "Initial implementation exposed internal models",
        ],
        "recommendations": [
            "Always use separate API models",
            "Implement validation at boundaries",
        ],
    }

    extract_result = integration.extract_from_session(session_id, experience_data)
    exp_id = extract_result["experience_record_id"]
    knowledge_id = extract_result["knowledge_entry_id"]

    # Step 2: Find related knowledge for the newly created experience
    related = integration.find_related_knowledge(exp_id)

    # Should at least find the knowledge we just created
    related_ids = {k.id for k in related}
    assert knowledge_id in related_ids

    # Step 3: Verify both records exist
    experience = experience_index.retrieve(exp_id)
    assert experience is not None

    knowledge = knowledge_store.retrieve(KnowledgeType.SOLUTION, knowledge_id)
    assert knowledge is not None

    # Step 4: Clean up with cascade
    removed = integration.remove_knowledge_cascade(KnowledgeType.SOLUTION, knowledge_id)
    assert removed is True
