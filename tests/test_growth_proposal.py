from continuity.growth import GrowthEngine, GrowthError


def test_growth_engine_promotes_accepted_proposal():
    engine = GrowthEngine()
    proposal_id = engine.create_proposal("evidence:sess-1:step", "Improve prompt")
    result = engine.decide(proposal_id, "accepted")
    assert result["status"] == "promoted"


def test_growth_engine_rejects_unknown_decision():
    engine = GrowthEngine()
    proposal_id = engine.create_proposal("evidence:sess-1:step", "Improve prompt")
    try:
        engine.decide(proposal_id, "unknown")
    except GrowthError as exc:
        assert exc.code == "invalid_decision"
    else:
        raise AssertionError("expected invalid_decision")
